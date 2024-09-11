''' ==================================================================================================
identify = 'A_7.2'
This code creates the SPARC11b.rxn file to add SOM precursor so that it runs prep.exe and creates
saprc14_rev1.mod and SAPRC14_rev1.f files

written by Ali Akherati October 2018 Colorado State University
================================================================================================== '''

import numpy as np
#import pandas as pd
import pygsheets as pyg
import time
#import re
import os
import sys
import datetime as dt
from BG_sizedist import SD_smps
#from BG_sizedist import SD_smps, SD_nanosmps
from functions import closest
from matplotlib import pyplot as plt 
from netCDF4 import Dataset 
from scipy import signal
from experiment_setting import get_settings

# Clean ipython
# ====================================================================================================
#from IPython import get_ipython
#get_ipython().magic('reset -sf') 

startTime = time.time()

# ====================================================================================================
# Run the python script to run the actual model
# ====================================================================================================
#maxjobs = 100 # how many jobs you can run. For ozone, max is 16
#queue = 'defaultfaculty.q@@students'
queue = 'defaultfaculty.q'

#----------|+++++|----------
#5 character identifier
#identify = 'T275K' 
#identify = 'SOMts' #
#identify = 'Dbcal' #
#identify = 'Lkpar' #
#identify = 'HiNOx' #
#identify = 'Nkout' #
#identify = 'A_7.2' #
#identify = 'dbk_0' #
#identify = 'A_7.2' #
#identify = 'sm_OH' #
#identify = 'soaco' # kpar flat above 1000 nm
#identify = 'kpar3' # kpar interpolated from Sirmollo et al. 2021
#identify = 'sulfW' # kvap_on set to kpar for smallest particles 
#identify = '01HOM' # still no trimethylbenzene
#identify = '2xnh3' # 1% HOMS, no tmb, 10K ppt nh3
#identify = 'oldbs' 
identify = 'base?' 
#----------|+++++|----------

settings = get_settings(identify)

# ====================================================================================================
endtime = settings['endtime']        # Length of model run
aadt = settings['aadt']     # microphysics timestep [s]
nintern = 1   # frequency of printing values or number of internal microphysics steps

NOx = settings['NOx']               # NOx concentration for OH proxy #3
orgfrac_bg = settings['orgfrac_bg']        # Organic fraction of background aerosols  
nh3_ppt = settings['nh3_ppt']       # NH3 concentration [ppt]
OH_scale = settings['OH_scale']

start_t = dt.datetime(2022,8,1,11)
name = '%s%s%s'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2))
og_date = []
og_date.append(start_t)
for i in range(int(endtime[0]*3600/aadt)-1):
  og_date.append(og_date[-1] + dt.timedelta(seconds=aadt))
og_date = np.array(og_date)
utc_date = og_date + dt.timedelta(hours = 6)

density_bg = orgfrac_bg*1400.0+(1-orgfrac_bg)*1770 # [kg/m3]

# ====================================================================================================
# nucleation parameters
# ====================================================================================================
fion = settings['fion']           # Ion recombination coefficient [cm-3 s-]
org_nuc = settings['org_nuc']     # switch for organic nucleation [0 or 1]
inorg_nuc = settings['inorg_nuc'] # switch for inorganic nucleation [0 or 1]
iorg  = 456                       # SamO changed from 893
ibins = 40                        # number of bins
idiag = 2                         # number of diagnostic species including sulfate and ammonia (2)

# Some other parameters 
# ====================================================================================================
#           BNZ,   TOL,   XYL,    ISP,   TRP
#DLVP_v = '1.97 1.77 2.05 2.25 1.97 1.97 1.97' 
#DLVP_v = '2.075 1.966 1.755 2.245 1.571 1.571 1.571' # From Charles 
#DLVP_v = '1.813 1.419 1.567 2.245 1.586 1.586 1.586' # Bilsback et al. 2022 PWL only
DLVP_v = '1.582 1.550 1.571 2.245 1.503 1.503 1.503' # Bilsback et al. 2022 PWL+V2PWL+VWL


COAG =  settings['COAG']   # [0 or 1] the switch for On/Off coagulation
vwl  =  settings['vwl'] # [0 or 1] the switch for On/Off vapor wall loss
pwl  =  settings['pwl'] # [0 or 1] the switch for On/Off particle wall loss 

A = settings['A']    #nm/s

xk = np.zeros(ibins+1) 
xk[0]=1E-21*2**-10 
for k in range(1,ibins+1):
   xk[k] = xk[k-1]*2.
pdens=1400. # fixed density for simplicity
xkm=np.sqrt(xk[:-1]*xk[1:])
Dp=((6.*xkm/pdens/np.pi)**(1.0/3.0))*1E9 # [m] average particle diameter of bin
#Dp_lower=(6.*xk[:-1]/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin
#Dp_upper=(6.*xk[1:]/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin

#sys.exit('give up')
kpar = settings['kpar']
kpar = ''
for i in range(len(Dp)):
  if i < 11:
    #print('Dp[i]=',Dp[i])
    kpar = kpar + str(A/Dp[11])+' '
  else:
  #print(Dp[np.where(Dp>20.)[0][0]])
  #sys.exit()
  #kpar = kpar + str(float(0.00001440))+' '
  # Use this -----------------
  #if Dp[i] < 30:
  #  kpar = kpar + str(A/Dp[np.where(Dp>30)[0][0]])+' '
  #elif Dp[i]>1000:
  #  kpar = kpar + str(A/Dp[np.where(Dp>1000)[0][0]])+' '
  #else:
    kpar = kpar + str(A/Dp[i])+' '
  #---------------------------
  #kpar = kpar + str(9.108699918785293e-06)+' '

#print(kpar)
#sys.exit()
'''
#=====================================================================
# this is from estimates of pwl rates from Sirmollo et al. (2021)
# This didn't really work great so it should probably be deleted.
a1,a2,a3 = 1/5400,1/7380,1/3510
Y = np.array([a1,a2,a3])
X = np.array([60,300,2500])
Kpar_array = np.interp(Dp,X,Y)

for i in range(len(Dp)):
  kpar = kpar + str(Kpar_array[i]) + ' '

#=====================================================================
'''

#kpar = A/Dp
#sys.exit()

# ---------------------- 
#ke      = 0.0        # loss rate constant
#kw0     = 0.0        # loss rate constant 
kvap_on = settings['kvap_on']
#kvap_on = A/Dp[np.where(Dp>30)[0][0]]

alpha   = 1.0        # accommodation coefficient 
storg   = 0.025      # [N/m] surface tension
db     = [1.0E-20]  # particle-phase diffusion coefficient [m2/s] (could try 3.4e-15 from Charles) 
kc      = 0.0        # first-order loss rate of species in the particle phase [1/s]
# ---------------------- 
boxvol  = settings['boxvol'] # teflon [cm3] - [CalTech 24 m3, CSU 10 m3, CMU ?? m3]
stptemp    = 273.15  # STP temperature 
stppres = 101325.0   # STP pressure 
#temp = 298.0         # temperature in Kelvin
sfcpres = settings['sfcpres']

# directory information
# ====================================================================================================
script_directory = os.popen('pwd').read()[:-1]
src_directory = script_directory[:-(len('scripts'))] + 'src'
run_directory = script_directory[:-(len('scripts'))] + 'runs'  
gc = pyg.authorize(service_file='../inputs/som-tomas-9d97902effb8.json')

# Precursor scale factor
#=====================================================================================================
precscale = [1.0] 

# Background size distribution 
#=====================================================================================================
#Nobg1 = [50.0,100.0,150.0,200.0,250.0,300.0]
#Dpm_bg1 = 0.2
#sigma_bg1 = 1.5 


#Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = SD_smps(SMPS_sheetname,SMPS_lower,endtime,gc)
Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 100.0,0.02,1.5,0.0,0.2,1.5,0.0,0.3,1.5


f7 = open('aersol_injections','r')
f8 = open('../inputs/%s%s%s_%s_inject'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')

for line in f7.readlines():
  spl_line=line.split(' ')
  injection = float(spl_line[0])
  injec_Dp = float(spl_line[1])*10.0
  injec_sig = spl_line[2]
  dates = dt.datetime.strptime(spl_line[3]+' '+spl_line[4],'%Y-%m-%d %H:%M:%S')
  dates = dates - dt.timedelta(hours=1) #CDT -> CST
  
  if dates+dt.timedelta(seconds=10) >= og_date[0] and dates-dt.timedelta(seconds=10) <= og_date[-1]: #Comment out to not overwrite
  #if dates >= og_date[0] and dates <= og_date[-1]:
    f8.write('%s  %s  %s  %s\n'%(str(injection),str(injec_Dp),str(injec_sig),str(dates))) #Comment out to not overwrite
    #f8.write('%s  %s  %s  %s\n'%(str(0.0),str(injec_Dp),str(injec_sig),str(dates))) #Comment out to not overwrite

f7.close()
f8.close()
#sys.exit()

# Flow rate time series
#=====================================================================================================
iostat = 1
cntr = 0

f3 = open('../inputs/%s%s%s_%s_flows'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')
f4 = open('../inputs/%s%s%s_%s_OH'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')
f5 = open('../inputs/%s%s%s_%s_Temp'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')
f6 = open('../inputs/%s%s%s_%s_RH'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')

for v in range(len(og_date)):

  switchfile = '../inputs/TRACER_flow_switches/UCI_%s%s%s.cag'%(str(og_date[v].year).zfill(2)[2:],str(og_date[v].month).zfill(2),str(og_date[v].day).zfill(2))
  
  f1 = open(switchfile,'r')
  #year = int(switchfile[4:6])
  #month = int(switchfile[6:8])
  #day = int(switchfile[8:10])
  
  
  switch,dates,seconds =[],[],[]
  for line in f1.readlines():
    spl_line = line.split(',')
    switch.append(int(spl_line[-1]))
    dates.append(dt.datetime.strptime('%s:%s:%s '%(str(og_date[v].year).zfill(4),str(og_date[v].month).zfill(2),str(og_date[v].day).zfill(2))+spl_line[0][:-3],'%Y:%m:%d %H:%M:%S'))
    #     dates.append('%s:%s:%s'%(year,month,day)+spl_line[0])
  dates = np.array(dates) - dt.timedelta(hours=1) #Already in CDT? CDT -> CST
  for i in range(len(dates)):
    seconds.append((dates[i]-dates[0]).total_seconds())

  switch = np.array(switch)
  seconds = np.array(seconds)
  
  #aadt = 10
  #endtime = 10
  # length = int(endtime*3600/aadt)
  length = int((dates[-1]-dates[0]).total_seconds()/aadt)
  
  date = []
  date.append(dates[0])
  seconds2 = []
  seconds2.append(0)
  
  for i in np.arange(1,length,1):
    date.append(date[-1] + dt.timedelta(seconds=aadt))
    seconds2.append(seconds2[-1]+aadt)
                    
  date = np.array(date)
  seconds2 = np.array(seconds2)
  test = np.interp(seconds2,seconds,switch)
 
  for i in range(len(test)):
    if test[i] == 0.0 or test[i] == 1.0:
      test[i] = test[i]
    else:
      test[i] = test[i-1]
  
  indx = closest(date,og_date[v])
  test = np.array(test)
  
  #test = test[indx:indx+int(endtime[0]*3600/aadt)]
  #date = date[indx:indx+int(endtime[0]*3600/aadt)]
  
  #sys.exit()
  
  #f3 = open('../inputs/%s%s%s_flows'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2)),'w')
  #for i in range(len(test)):
  f3.write('%s   %s\n'%(str(555.0),str(test[indx]*250.0))) #Comment out to not overwrite
  #f3.write('%s, %s, %s\n'%(str(0.0),str(0.0),str(date[indx])))


  #f3.close()
  #sys.exit()

  #temp_date = og_date[v] + dt.timedelta(hours=6) #CST -> UTC
  indx_utc = closest(date,utc_date[v])
  #print(indx_utc,indx,date[indx_utc]+dt.timedelta(hours=6))
  #sys.exit()

  ohfid = Dataset('../inputs/SW_radiation/houskyrad60sM1.b1.%s%s%s.000000.cdf'%(str(og_date[v].year).zfill(4),str(og_date[v].month).zfill(2),str(og_date[v].day).zfill(2)),'r')

  time = np.array(ohfid.variables['time'])
  time_offset = np.array(ohfid.variables['time_offset'])
  #short_direct_normal = np.array(ohfid.variables['short_direct_normal'])
  down_short_hemisp = np.array(ohfid.variables['down_short_hemisp'])

  #print(time, seconds2)
  #print(len(date),len(seconds2),len(time),len(og_date),len(utc_date))
  #sys.exit()
  #interp_time = np.linspace(time[0],time[-1],length)
  #down_short_hemisp = signal.savgol_filter(down_short_hemisp,101,2)
  sw_rad = np.interp(seconds2,time,down_short_hemisp)

  if sw_rad[indx_utc]<0.001:
    sw_rad[indx_utc] = 0.001

  X = np.log10(NOx) - 0.195
  Y = sw_rad[indx_utc]/(1370*0.76)

  P1 = -0.014*X**6 + 0.0027*X**5 + 0.1713*X**4 - 0.0466*X**3 - 0.7893*X**2 - 0.1739*X + 6.9414
  P2 = (-1345*Y**3 + 4002*Y**2 - 471.8*Y + 42.72)*10**4

  writer = 0.82*10**(P1*np.log10(P2)/6.8)

  #writer = 3081.0*sw_rad[indx]**0.8397
  #if writer < 6.033E4:
  #  writer = 6.033E4
  #writer = 1000000.0
  f4.write('%s\n'%str(writer)) #Comment out to not overwrite
  #f4.write('%s\n'%10000000.0)

  metfid = Dataset('../inputs/TRACER_met/houmetM1.b1.%s%s%s.000000.cdf'%(str(utc_date[v].year).zfill(4),str(utc_date[v].month).zfill(2),str(utc_date[v].day).zfill(2)),'r')
  
  
  time = np.array(metfid.variables['time'])
  time_offset = np.array(metfid.variables['time_offset'])
  
  temp_date = []
  startT = dt.datetime(utc_date[v].year,utc_date[v].month,utc_date[v].day,0) - dt.timedelta(hours=6)
  for i in range(len(time_offset)):
    temp_date.append(startT+dt.timedelta(seconds=time_offset[i]))

  indx = closest(temp_date,og_date[v])

  temp_mean = np.array(metfid.variables['temp_mean'])
  rh_mean = np.array(metfid.variables['rh_mean'])

  temp = np.interp(seconds2,time,temp_mean)
  RH = np.interp(seconds2,time,rh_mean)
 
  f5.write('%s\n'%str(temp[indx]+273.15)) #Comment out to not overwrite
  #f5.write('%s\n'%str(275.0)) # In case we want to overide temperature
  f6.write('%s\n'%str(RH[indx]/100.0)) #Comment out to not overwrite
  #f5.write('%s\n'%str(300.0))
  #f6.write('%s\n'%str(0.6))

f3.close()
f4.close()
f5.close()
f6.close()

# OH concentrations
#=====================================================================================================
#a_oh = [1000000.0]

#f4 = open('../inputs/%s%s%s_OH'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2)),'w')
#for i in range(int(endtime[0]*3600/aadt)):
#f4.write('%s\n'%str(a_oh[0]))
#f4.close()

#sys.exit('Better luck next time')

# --- read input sheet --------------------------------------------------------------  
No1     = 0.0 #df_input.loc[df_input['variables']=='No_1', 'Manish_10_1.5e6']# [# cm-3] background 1st number conc.
Dpm1    = 80e-3 #df_input.loc[df_input['variables']=='Dpm_1', 'Manish_10_1.5e6'].iloc[0]*1.0e-3 # [microns] background 1st median diameter
sigma1  = 1.8 #df_input.loc[df_input['variables']=='sigma_1', 'Manish_10_1.5e6'].iloc[0]# 1st background sigma 
No2     = 0.0 #df_input.loc[df_input['variables']=='No_2', 'Manish_10_1.5e6'].iloc[0]# [# cm-3] background 2nd number conc.
Dpm2    = 80e-3 #df_input.loc[df_input['variables']=='Dpm_2', 'Manish_10_1.5e6'].iloc[0]*1.0e-3# [microns] background 2nd median diameter
sigma2  = 1.8 #df_input.loc[df_input['variables']=='sigma_2', 'Manish_10_1.5e6'].iloc[0]# 2nd background sigma 


nsomprec    = 7 # number of som precursors for parameterizations or SOM grids ***** 1 for now
somprecname = 'BNZSOMG TOLSOMG XYLSOMG ISPSOMG TRPSOMG IVOSOMG SVOSOMG' # som precursor parameterization's name
dlvp        = DLVP_v

seed_dens = 1.4 #df_input.loc[df_input['variables']=='POA density', 'AGU2019_F007'].iloc[0]*1.0e+3
poa_1stname = 'SVO_C10'
poa_1st_lenname = len(poa_1stname)

#===================================================================================
emiss_sheetname = 'Sheet1' 
gsh_emission_ML = gc.open('CS_NPF_testing')
df_emiss_ML = gsh_emission_ML.worksheet_by_title(title='%s'%emiss_sheetname).get_as_df()


#===================================================================================
 
index  = np.where(df_emiss_ML.iloc[:,0]!='')[0].shape[0] 
spname = df_emiss_ML['species'].iloc[:index]
g_ippm_ML = df_emiss_ML['gas_id'].iloc[:index]
p_frac = df_emiss_ML['pfrac_id'].iloc[:index] 

nspemiss = len(spname)
emiss_spname =  ''
emiss_ippm   =  ''
seed_frac    =  ''
 
for i in range(len(spname)):
  emiss_spname = emiss_spname + '%15s'%(spname.iloc[i])
  seed_frac =  seed_frac + '%15.5E'%(p_frac.iloc[i])
for i in range(len(spname)-1):
  #emiss_ippm = emiss_ippm + '%15.5E'%(g_ippm_ML.iloc[i+1])
  emiss_ippm = emiss_ippm + '0.00000E+00  '

#f9 = open('../inputs/raw_TRACER_SO2.txt','r')
f9 = open('../inputs/TRACER_SO2_MAQL2.txt','r')
SO2 = []
for line in f9.readlines():
  spl_line=line.split(',')
  so2_raw = float(spl_line[0]) #/1000.  #conversion to ppm is done in box.f 
  if so2_raw < 0.0:
    so2_raw = 0.0
  dates = dt.datetime.strptime(spl_line[1][0:-2],' %Y-%m-%d %H:%M:%S')
  #sys.exit()
  if dates >= og_date[0] and dates <= og_date[-1]:
    SO2.append(so2_raw)

    #if dates >= og_date[0] and dates <= og_date[-1]:
    #f8.write('%s  %s  %s  %s\n'%(str(injection),str(injec_Dp),str(injec_sig),str(dates)))

f9.close()

f10 = open('../inputs/TRACER_VOC_PTRMS.txt','r')
VOCs = []
for line in f10.readlines():
  spl_line=line.split('#')
  spl_line[1] = spl_line[1][:-2]

  #voc_raw = float(spl_line[0])/1000.  #ppm
  #if voc_raw < 0.0:
  #  voc_raw = 0.0

  dates = dt.datetime.strptime(spl_line[0],'%Y-%m-%d %H:%M:%S ')
  #sys.exit()
  if dates >= og_date[0] and dates <= og_date[-1]:
    VOCs.append(spl_line[1])

    #if dates >= og_date[0] and dates <= og_date[-1]:
    #f8.write('%s  %s  %s  %s\n'%(str(injection),str(injec_Dp),str(injec_sig),str(dates)))

f10.close()
#sys.exit()

f5 = open('../inputs/%s%s%s_%s_voc'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')

for i in range(int(endtime[0]*3600/aadt)):
  f5.write('%15.5E %s    0.00000E+00    0.00000E+00    0.00000E+00\n'%(SO2[i],VOCs[i]))
  #f5.write('%15.5E    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00\n'%(SO2[i]))
f5.close()


f11 = open('../inputs/TRACER_O3_MAQL2.txt','r')
O3 = []
for line in f11.readlines():
  spl_line=line.split(',')
  #spl_line[1] = spl_line[1][:-2]

  #voc_raw = float(spl_line[0])/1000.  #ppm
  #if voc_raw < 0.0:
  #  voc_raw = 0.0

  dates = dt.datetime.strptime(spl_line[1][:-2],' %Y-%m-%d %H:%M:%S')
  #sys.exit()
  if dates >= og_date[0] and dates <= og_date[-1]:
    O3.append(spl_line[0])
    #O3.append('0.0')

    #if dates >= og_date[0] and dates <= og_date[-1]:
    #f8.write('%s  %s  %s  %s\n'%(str(injection),str(injec_Dp),str(injec_sig),str(dates)))

f11.close()

f12 = open('../inputs/%s%s%s_%s_o3'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')

for i in range(int(endtime[0]*3600/aadt)):
  #f12.write('%15.5E, %s\n'%(SO2[i]))
  f12.write('%s\n'%str(O3[i]))
f12.close()

# Running 
# ====================================================================================================
print('General information for the following simulations')  
print('======================================================')
print('Simulation: %s'%name)            
print('inbins = %s'%ibins)
print('COAG = %s'%COAG)
print('boxvol = %s'%boxvol, '[cm3]')
print('alpha = %s'%alpha)
print('surface pressure = %s'%sfcpres, '[Pa]')
print('nh3_ppt = %s'%nh3_ppt)
# ====================================================================================================

#sys.exit('You suck at this!!!') 

ctr = 0
for NH3 in nh3_ppt:
  for tend in endtime:
    ctr+=1
    No_bg1 = str(float(Nobg1))
    No_bg2 = str(float(Nobg2))
    No_bg3 = str(float(Nobg3))
    
    rname = '%s_%s_vwl%1i_pwl%1i_hr%4.2e_nh3%s_orgfn%s_inorg%s_'%(name,identify,vwl,pwl,tend,NH3,org_nuc,inorg_nuc)

    index  = np.where(df_emiss_ML.iloc[:,0]!='')[0].shape[0] 
    spname = df_emiss_ML['species'].iloc[:index]
    g_ippm_ML = df_emiss_ML['gas_id'].iloc[:index]
    p_frac = df_emiss_ML['pfrac_id'].iloc[:index] 
    
    #nspemiss = len(spname)
    #emiss_spname =  ''
    #emiss_ippm   =  ''
    #seed_frac    =  ''
    # 
    #for i in range(len(spname)):
    #  emiss_spname = emiss_spname + '%15s'%(spname.iloc[i])
    #  seed_frac =    seed_frac + '%15.5E'%(p_frac.iloc[i])
    #  emiss_ippm = emiss_ippm + '%15.5E'%(g_ippm_ML.iloc[i]*scale)
     
    #print('%i - Simulation'%ctr)
    #print('---------------')
    #print('VWL = %s'%vwl)
    #print('PWL = %s'%pwl)
    #print('Db = %s [m2/s]'%db)
    #print('Kc = %s [1/s]'%kc)
    #print('ke = %s [1/s]'%ke)
    #print('OH = %s [molec/cm3]'%OH_conc)
    #print('No1 = %s [#/cm3]'%No1)
    #print('Dpm1 = %s [um]'%Dpm1)
    #print('sigma1 = %s'%sigma1)
    #print('No2 = %s [#/cm3]'%No2)
    #print('Dpm2 = %s [um]'%Dpm2)
    #print('sigma2 = %s'%sigma2)
    #print('time = %s [h]'%tend)
    #print('runname = %s'%rname)
    
    if os.path.exists('../runs/%s'%(rname)):
     os.system('rm -r ../runs/%s'%(rname))
      
    os.system('mkdir ../runs/%s'%(rname))
    os.system('cp ../src/box.exe ../runs/%s/'%(rname))
    os.system('cp ../src/saprc14_rev1.mod ../runs/%s/saprc14_rev1.mod'%(rname))
      
    f1 = open('../runs/%s/input'%(rname),'w')
    f1.write('%s\n'%rname)
    f1.write('%f\n'%aadt)
    f1.write('%i\n'%nintern)
    f1.write('%1i\n'%COAG)
    f1.write('%1i\n'%vwl)
    f1.write('%1i\n'%pwl)
    f1.write('%f\n'%kvap_on)
    f1.write('%s\n'%kpar)
    #f1.write('%e\n'%OH_conc) # ***
    #f1.write('%e\n'%b_oh) # ***
    #f1.write('%e\n'%bx_oh) # ***
    f1.write('%e\n'%OH_scale)
    f1.write('%15.4f\n'%fion)
    f1.write('%i\n'%org_nuc)
    f1.write('%i\n'%inorg_nuc)
    f1.write('%8.1e\n'%NH3)
    f1.write('%10.1f\n'%boxvol)
    f1.write('%5.2f\n'%tend) # ***
    f1.write('%8.5f\n'%alpha)
    f1.write('%8.5f\n'%db[0])
    f1.write('%f\n'%kc)
    f1.write('%8.5f\n'%storg)
#    f1.write('%8.5f\n'%temp)
#    f1.write('%8.5f\n'%RH)
    f1.write('%8.5f\n'%No1) # ***
    f1.write('%8.5f\n'%Dpm1) # ***
    f1.write('%8.5g\n'%sigma1)
    f1.write('%8.5f\n'%No2) # ***
    f1.write('%8.5f\n'%Dpm2) # ***
    f1.write('%8.5g\n'%sigma2)
    f1.write('%02i\n'%nsomprec)
    f1.write('%s\n'%somprecname)
    f1.write('%s\n'%dlvp)
    f1.write('%s\n'%poa_1stname)
    f1.write('%s\n'%poa_1st_lenname)
    f1.write('%03i\n'%nspemiss)
    f1.write('%s\n'%emiss_spname)
    f1.write('%15.5E %s\n'%(SO2[0],emiss_ippm))
    f1.write('%s\n'%seed_frac)
    f1.write('%s\n'%seed_dens)
    f1.write('%s\n'%No_bg1)
    f1.write('%s\n'%Dpm_bg1) 
    f1.write('%s\n'%sigma_bg1)
    f1.write('%s\n'%No_bg2)
    f1.write('%s\n'%Dpm_bg2) 
    f1.write('%s\n'%sigma_bg2)
    f1.write('%s\n'%No_bg3)
    f1.write('%s\n'%Dpm_bg3) 
    f1.write('%s\n'%sigma_bg3)
    f1.write('%8.5f\n'%density_bg)
    f1.write('%8.6f\n'%orgfrac_bg)
    #f1.write('%20.4f\n'%p_dilt1[0])
    #f1.write('%20.4f\n'%p_dilt2[0])
    #f1.write('%20.4f\n'%p_dilt3[0])
    #f1.write('%20.4f\n'%p_dilt4[0])
    f1.close()
    
    # info file
    # ---------------------------------------------------------
    if os.path.exists('../outputs/%s.input'%(rname)):
     print('YES - %s.input exists!'%(rname))
     os.system('rm ../outputs/%s*'%(rname))
    f2 = open('../outputs/%s.input'%rname,'w')
    f2.write('filename    = %s\n'%rname)
    #f2.write('parameterization: %s_%s\n'%(precursor,regime))
    f2.write('aadt        = %s\n'%aadt)
    f2.write('nintern     = %s\n'%nintern)
    f2.write('ibins       = %s\n'%ibins)
    f2.write('COAG        = %s\n'%COAG)
    f2.write('VWL         = %s\n'%vwl)
    f2.write('PWL         = %s\n'%pwl)
    f2.write('kvap_on          = %s [1/s]\n'%kvap_on)
    f2.write('kpar         = %s [1/s]\n'%kpar)
    f2.write('A           = %s [nm/s]\n'%A)
    #f2.write('OH eqn. = a_oh*exp(-1.*ax_oh*t) + b_oh*exp(-1.*bx_oh*t)\n') # ***
    #f2.write('OH_conc        = %s\n'%OH_conc) # ***
    #f2.write('ax_oh       = %s\n'%ax_oh) # ***
    #f2.write('b_oh        = %s\n'%b_oh) # ***
    #f2.write('bx_oh       = %s\n'%bx_oh) # ***
    f2.write('OH_scale    = %s\n'%OH_scale)
    f2.write('fion        = %s\n'%fion)
    f2.write('org_nuc     = %s\n'%org_nuc)
    f2.write('iorg_nuc    = %s\n'%inorg_nuc)
    f2.write('nh3_ppt     = %s\n'%NH3)
    f2.write('boxvol      = %s [cm3]\n'%boxvol)
    f2.write('endtime     = %s [hours]\n'%tend) # ***
    f2.write('alpha       = %s\n'%alpha)
    f2.write('Db          = %s [m2/s]\n'%db[0])
    f2.write('Kc          = %s [1/s]\n'%kc)
    f2.write('storg       = %s [N/m]\n'%storg)
#    f2.write('temperature = %s [K]\n'%temp)
    f2.write('No1         = %s [# cm-3]\n'%No1) # ***
    f2.write('Dpm1        = %s [um]\n'%Dpm1) # ***
    f2.write('Sigma1      = %s\n'%sigma1)
    f2.write('No2         = %s [# cm-3]\n'%No2) # ***
    f2.write('Dpm2        = %s [um]\n'%Dpm2) # ***
    f2.write('Sigma2      = %s\n'%sigma2)
    f2.write('nsomprec    = %s\n'%nsomprec)
    f2.write('somprecname = %s\n'%somprecname)
    f2.write('dlvp        = %s\n'%dlvp)
    f2.write('poa_1stname = %s\n'%poa_1stname)
    f2.write('poa_1st_len = %s\n'%poa_1st_lenname)
    f2.write('nspemiss    = %s\n'%nspemiss)
    f2.write('emiss_spname= %s\n'%emiss_spname)
    f2.write('emiss_ippm  = %s\n'%emiss_ippm)
    f2.write('seed_frac   = %s\n'%seed_frac)
    f2.write('seed_dens   = %s\n'%seed_dens)
    f2.write('No_bg1      = %s\n'%No_bg1)
    f2.write('Dpm_bg1     = %s\n'%Dpm_bg1) 
    f2.write('sigma_bg1   = %s\n'%sigma_bg1)
    f2.write('density_bg  = %s\n'%density_bg)
    f2.write('orgfrac_bg  = %s\n'%orgfrac_bg)
    #f2.write('p_dilt1     = %s\n'%p_dilt1[0])
    #f2.write('p_dilt2     = %s\n'%p_dilt2[0])
    #f2.write('p_dilt3     = %s\n'%p_dilt3[0])
    #f2.write('p_dilt4     = %s\n'%p_dilt4[0])
    
    f2.close()
    
    #sys.exit('Sucker')
    # ---------------------------------------------------------
    # ************************************************
    #c=os.popen('qstat').read()
    #b=re.findall('alia', c)
    #njobs=len(b)
    #print('b=',b)
    #print('njobs=',len(b))
    
    #while njobs >= maxjobs:
    #   os.system('sleep 5')
    #   c=os.popen('ps -u alia').read()
    #   b=re.findall('box.exe', c)
    #   njobs=len(b)
    # ************************************************
    
    #os.system('sleep 5')

    df4 = open('../inputs/raw_runme.sh', mode='r') # reading the default header file of TOMAS
    runme_line = []
    for i in df4.readlines():
     runme_line.append(i.strip('\n'))
     df4.close()
             
    ind1 = np.where(np.array(runme_line)=='cd run_direct')[0][0]
    runme_line[ind1] = 'cd %s/%s'%(run_directory, rname)
    
    ind2 = np.where(np.array(runme_line)=="echo 'rname'")[0][0]
    runme_line[ind2] = 'echo %s'%(rname)
    
    #ind3 = np.where(np.array(runme_line)=='./box.exe <input> /dev/null')[0][0]
    ind3 = np.where(np.array(runme_line)=='./box.exe <input> out')[0][0]
    #runme_line[ind3] = './box.exe <input> /dev/null'
    #runme_line[ind3] = './box.exe <input> %s.out'%(rname)
    runme_line[ind3] = './box.exe <input> out'
    
    #if os.path.exists('runme.sh'):
    #   os.system('rm runme.sh')
    
    runme_out = open('../runs/%s/runme.sh'%(rname), mode='w')
    for i in runme_line:
     runme_out.write(i)
     runme_out.write('\n')
    runme_out.close()

    #os.system('cd ../runs/%s/; qsub -cwd -V -pe MPI 1 -q %s ./runme.sh'%(rname, queue))
    os.system('cd ../runs/%s/; sbatch ./runme.sh'%(rname))

    #os.system('sleep 1')
      
#keep the compute node from logging out before each box.exe has finished
#test=2
#while test>=1:
#    c=os.popen('ps -u alia').read()
#    b=re.findall('box.exe', c)
#    test=len(b)
#    os.system('sleep 2')



