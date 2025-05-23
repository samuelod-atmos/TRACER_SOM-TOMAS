''' ==================================================================================================
This code creates the SPARC11b.rxn file to add SOM precursor so that it runs prep.exe and creates
saprc14_rev1.mod and SAPRC14_rev1.f files

written by Ali Akherati October 2018 Colorado State University

     -----------------------------------------------------------------
      SSSS    OOO   M    M     TTTTTTT   OOO   M    M     A      SSSS 
     S       O   O  MM  MM        T     O   O  MM  MM    A A    S    
      SSSS  O     O M MM M ===    T    O     O M MM M   A   A    SSSS 
          S  O   O  M    M        T     O   O  M    M  AAAAAAA       S
     SSSSS    OOO   M    M        T      OOO   M    M A       A SSSSS 
     -----------------------------------------------------------------
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
#identify = 'nwgrd' 
#identify = 'sommx' #
#identify = 'Dbcal' #
#identify = 'Fkpar' #
#identify = 'HiNOx' #
#identify = 'noinj' #
#identify = 'x1000' #
#identify = 'nopul' #
#identify = 'inx10' #
#identify = 'dbk_0' #
#identify = 'A_7.2' #
#identify = '1.5OH' #
#identify = 'soaco' # kpar flat above 1000 nm
#identify = 'kpar3' # kpar interpolated from Sirmollo et al. 2021
#identify = 'sulfW' # kvap_on set to kpar for smallest particles 
#identify = '01HOM' # still no trimethylbenzene
#identify = '2xnh3' # 1% HOMS, no tmb, 10K ppt nh3
#identify = 'A1e-2' 
#identify = '0_tmb' 
#identify = 'styre' 
#identify = 'mxout' 
#identify = 'HOM.3' 
#identify = 'smtOH' 
#identify = '2x_OH' 
#identify = 'HOMmx' 
#identify = 'nan_0' 
#identify = 'kvpon' 
#identify = 'kvp3x' 
#identify = 'kflat' 
#identify = 'splic' 
#identify = 'wiMDL' 
#identify = 'minOH' 
#identify = 'NPF_5'
#identify = 'sclOH'
#identify = 'sclfn'
#identify = 'GC_OH'
#identify = '300KT'
#identify = '0.7RH'
#identify = 'DP_O3' 
#identify = 'DP2O3' 
#identify = '100fn'
#identify = 'noHOM'
#identify = 'kp2.5'
identify = 'A2e-3' 
#identify = '1.8kp' 
#identify = 'y_mix' 
#identify = 'n_mix' 
#identify = 'cfrag' 
#identify = 'prfct' 
#identify = 'bigDp' 
#identify = 'debug' 
#----------|+++++|----------

settings = get_settings(identify)

# ====================================================================================================
endtime = settings['endtime']        # Length of model run
aadt = settings['aadt']     # microphysics timestep [s]
nintern = 1   # frequency of printing values or number of internal microphysics steps

NOx = settings['NOx']               # NOx concentration for OH proxy #3
orgfrac_bg = settings['orgfrac_bg']        # Organic fraction of background aerosols  
nh3_ppt = settings['nh3_ppt']       # NH3 concentration [ppt]
OH_scale = settings['OH_scale']     # multiplier for OH concentration
OH_proxy = 'Rad'
#OH_proxy = 'GC'
density_bg = orgfrac_bg*1400.0+(1-orgfrac_bg)*1770 # [kg/m3] - density of aerosol originally in the chamber

#start_t = dt.datetime(2022,8,6,1)  # start date [CST]
start_t = dt.datetime(2022,8,1,11)  # start date [CST]
name = '%s%s%s'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2))  # date string 

# make an array of dates for the simulation
og_date = []
og_date.append(start_t)  # begins at start date
for i in range(int(endtime*3600/aadt)-1):
  og_date.append(og_date[-1] + dt.timedelta(seconds=aadt))
og_date = np.array(og_date)
utc_date = og_date + dt.timedelta(hours = 6)

# ====================================================================================================
# nucleation parameters
# ====================================================================================================
fion = settings['fion']           # Ion recombination coefficient [cm-3 s-]
org_nuc = settings['org_nuc']     # switch for organic nucleation [0 or 1]
inorg_nuc = settings['inorg_nuc'] # switch for inorganic nucleation [0 or 1]
#iorg  = 456                       # SamO changed from 893
ibins = 40                        # number of bins
idiag = 2                         # number of diagnostic species including sulfate and ammonia (2)

fn_scale = settings['fn_scale']
T_switch = settings['T_switch']
RH_switch = settings['RH_switch']
HOM_switch = settings['HOM_switch']

# Some other parameters 
# ====================================================================================================
#           BNZ,   TOL,   XYL,    ISP,   TRP
#DLVP_v = '1.97 1.77 2.05 2.25 1.97 1.97 1.97' 
#DLVP_v = '2.075 1.966 1.755 2.245 1.571 1.571 1.571' # From Charles 
#DLVP_v = '1.813 1.419 1.567 2.245 1.586 1.586 1.586' # Bilsback et al. 2023 PWL only
DLVP_v = '1.582 1.550 1.571 2.245 1.503 1.503 1.503' # Bilsback et al. 2023 PWL+V2PWL+VWL

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
#kpar = settings['kpar']

kflat = 6.9e-5
#kflat = 1.3e-4

kpar = ''
for i in range(len(Dp)):
  #if i < 11:
  if i < 5:
  #  kpar = kpar + str(A/Dp[np.where(Dp>100.)[0][0]])+' '
    #print('Dp[i]=',Dp[i])
    kpar = kpar + str((A/Dp[4]+kflat))+' '
  #else:
  #print(Dp[np.where(Dp>20.)[0][0]])
  #sys.exit()
  #kpar = kpar + str(float(0.00001440))+' '
  # Use this -----------------
  #if Dp[i] < 30:
  #  kpar = kpar + str(A/Dp[np.where(Dp>30)[0][0]])+' '
  #elif Dp[i]>1000:
  #  kpar = kpar + str(A/Dp[np.where(Dp>1000)[0][0]])+' '
  else:
    kpar = kpar + str((A/Dp[i]+kflat))+' '
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
#kvap_on = settings['kvap_on']
kvap_on = (A/Dp[4]+kflat)
#kvap_on = A

alpha   = 1.0        # accommodation coefficient 
storg   = 0.025      # [N/m] surface tension
#dbk     = 1          # particle-phase diffusion coefficient [m2/s] (could try 3.4e-15 from Charles) 
dbk     = 1          # diffusivity switch [2 and 3 are constant values and 1 is dynamic]
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


# Background size distribution 
#=====================================================================================================
#Nobg1 = [50.0,100.0,150.0,200.0,250.0,300.0]
#Dpm_bg1 = 0.2
#sigma_bg1 = 1.5 

#Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = SD_smps(SMPS_sheetname,SMPS_lower,endtime,gc)

Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 4692.597952523227 , \
  0.032606184546552064 , \
  1.163217944787477 , \
  3915.9576072088835 , \
  0.028060107283775015 , \
  1.28985945295308 , \
  0.0 , \
  0.3 , \
  1.5

if identify == 'NPF_1':
  Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 312.42826868553936 , \
      0.02329662953234773 , \
      1.0649599346539054 , \
      38.35487507729456 , \
      0.02640771658732193 , \
      1.3401125033727537 , \
      0.0, \
      0.3, \
      1.5  

if identify == 'NPF_2':
  Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 189.51502908805983 , \
  0.04313120038228448 , \
  1.3153020124817678 , \
  12.438096648164896 , \
  0.1491972729419338 , \
  1.6040713737678909 , \
  0.0 , \
  0.3 , \
  1.5

# fits for 8:30 - 9:30 (right before the npf event)
#if identify == 'NPF_2':
#  Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 196.664304942216 , \
#  0.014762942595860376 , \
#  1.1760001657815107 , \
#  497.03970264192776 , \
#  0.07001171821852925 , \
#  2.849708564508544 , \
#  0.0 , \
#  0.3 , \
#  1.5
  
if identify == 'NPF_3':
  Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 267.2249323278466 , \
  0.0444653932822287 , \
  1.3094527937520826 , \
  98.76266503888515 , \
  0.048075394140407776 , \
  3.7118732548167994 , \
  0.0 , \
  0.3 , \
  1.5

if identify == 'NPF_4':
  Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 190.89347105722797 , \
  0.02283914889332486 , \
  1.0698440217747966 , \
  26.580541499201722 , \
  0.03376589229986022 , \
  1.0686101187055208 , \
  0.0 , \
  0.3 , \
  1.5

if identify == 'NPF_5':
  Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 250.87421986319873 , \
  0.02575347359917518 , \
  1.0672613599631353 , \
  71.08016841570203 , \
  0.030994237375203453 , \
  1.3765233673625767 , \
  0.0 , \
  0.3 , \
  1.5

#else:
#  Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 100.0,0.02,1.5,0.0,0.2,1.5,0.0,0.3,1.5
#if identify == 'NPF_6':
#  Nobg1,Dpm_bg1,sigma_bg1,Nobg2,Dpm_bg2,sigma_bg2,Nobg3,Dpm_bg3,sigma_bg3  = 


#===================================================================================
print('making aerosol injection file')
#f7 = open('aersol_injections','r')
f7 = open('inject_aerosol','r')

f8 = open('../inputs/timeseries/%s%s%s_%s_inject'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')
for line in f7.readlines():
  spl_line=line.split(' ')
  injection = float(spl_line[0])#*10.0
  injec_Dp = float(spl_line[1])#*10.0
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
print('making chamber flow file')
f3 = open('../inputs/timeseries/%s%s%s_%s_flows'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')
switchfile = open('../inputs/TRACER_flow_switches/Interp_flows.txt')

for line in switchfile.readlines():
  spl_line = line.split(',')
  
  dates = dt.datetime.strptime(spl_line[0],'%Y-%m-%d %H:%M:%S')
  switch = float(spl_line[1]) #/1000.  #conversion to ppm is done in box.f 
 
  if dates >= og_date[0] and dates <= og_date[-1]:
    #f3.write('%s   %s\n'%(str(555.0),str(0.0))) #Comment out to not overwrite
    f3.write('%s   %s\n'%(str(555.0),str(switch*250.0))) #Comment out to not overwrite

f3.close()
switchfile.close()
#sys.exit('Taylor approves')

#===================================================================================
print('making OH file')
f4 = open('../inputs/timeseries/%s%s%s_%s_OH'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')

if OH_proxy == 'Rad':
  
  radfid = open('../inputs/SW_radiation/Interp_radiation.txt')
  for line in radfid.readlines():
    spl_line=line.split(',')
    dates = dt.datetime.strptime(spl_line[0],'%Y-%m-%d %H:%M:%S')
    sw_rad = float(spl_line[1])
  
    if dates >= og_date[0] and dates <= og_date[-1]:
      if sw_rad<0.001:
        sw_rad = 0.001
    
      #X = np.log10(NOx) - 0.195
      #Y = sw_rad/(1370*0.76)
      #P1 = -0.014*X**6 + 0.0027*X**5 + 0.1713*X**4 - 0.0466*X**3 - 0.7893*X**2 - 0.1739*X + 6.9414
      #P2 = (-1345*Y**3 + 4002*Y**2 - 471.8*Y + 42.72)*10**4
      #writer = 0.82*10**(P1*np.log10(P2)/6.8)
  
      writer = 3081.0*sw_rad**0.8397
      if writer < 6.033e4:
        writer = 6.033e4
      
      writer = writer + 10.0*(writer - 6.033e4)
      #writer = writer + 10*(writer - 267332.0)
  
      if writer < 267332.0:
        writer = 267332.0
  
      
      f4.write('%s\n'%str(writer)) #Comment out to not overwrite
  
  radfid.close()

if OH_proxy == 'GC':
  
  oh_file = open('../inputs/GC_OH_Houston.txt','r')
  #OH = []
  for line in oh_file.readlines():
    spl_line=line.split(',')
    #spl_line[1] = spl_line[1][:-2]
    #voc_raw = float(spl_line[0])/1000.  #ppm
    #if voc_raw < 0.0:
    #  voc_raw = 0.0
  
    dates = dt.datetime.strptime(spl_line[0][:],'%Y-%m-%d %H:%M:%S')
    #sys.exit()
    if dates >= og_date[0] and dates <= og_date[-1]:
      #OH.append(spl_line[0])
      f4.write('%s'%str(spl_line[1])) #Comment out to not overwrite
  
  oh_file.close()
  

f4.close()

#===================================================================================
print('making temperature and RH files')
f5 = open('../inputs/timeseries/%s%s%s_%s_Temp'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')
f6 = open('../inputs/timeseries/%s%s%s_%s_RH'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')
metfid = open('../inputs/TRACER_met/Interp_dataset.txt')
for line in metfid.readlines():
  spl_line=line.split(',')
  dates = dt.datetime.strptime(spl_line[0],'%Y-%m-%d %H:%M:%S')
  temp = float(spl_line[1]) 
  RH = float(spl_line[2])

  if dates >= og_date[0] and dates <= og_date[-1]:
    #temperature.append(temp)
    #rel_hum.append(RH)
    #temp = 300.0
    #RH = 70.0
    f5.write('%s\n'%str(temp))
    f6.write('%s\n'%str(RH/100.0))


f5.close()
f6.close()
metfid.close()

#sys.exit('what do you know?')
    
# OH concentrations
#=====================================================================================================
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
#g_ippm_ML = df_emiss_ML['gas_id'].iloc[:index]
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

#f10 = open('../inputs/TRACER_VOC_PTRMS_nan2zero.txt','r')
#f10 = open('../inputs/TRACER_VOC_PTRMS_sty.txt','r')
#f10 = open('../inputs/TRACER_VOC_PTRMS_withMDL.txt','r')
#f10 = open('../inputs/TRACER_VOC_PTRMS.txt','r')
f10 = open('../inputs/TRACER_VOC_PTRMS_Splice.txt','r')
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

f5 = open('../inputs/timeseries/%s%s%s_%s_voc'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')

for i in range(int(endtime*3600/aadt)):
  f5.write('%15.5E %s    0.00000E+00    0.00000E+00    0.00000E+00\n'%(SO2[i],VOCs[i]))
  #f5.write('%15.5E    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00    0.00000E+00\n'%(SO2[i]))
f5.close()


#f11 = open('../inputs/TRACER_O3_MAQL2.txt','r')
#f11 = open('../inputs/TRACER_O3_AOS.txt','r')
f11 = open('../inputs/TRACER_O3_DeerPark.txt','r')
O3 = []
for line in f11.readlines():
  spl_line=line.split(',')
  #spl_line[1] = spl_line[1][:-2]
  #voc_raw = float(spl_line[0])/1000.  #ppm
  #if voc_raw < 0.0:
  #  voc_raw = 0.0

  dates = dt.datetime.strptime(spl_line[1][:-2],' %Y-%m-%d %H:%M:%S')
  dates = dates - dt.timedelta(hours=1)
  #sys.exit()
  if dates >= og_date[0] and dates <= og_date[-1]:
    O3.append(spl_line[0])
    #O3.append('0.0')
    #if dates >= og_date[0] and dates <= og_date[-1]:
    #f8.write('%s  %s  %s  %s\n'%(str(injection),str(injec_Dp),str(injec_sig),str(dates)))

f11.close()


f12 = open('../inputs/timeseries/%s%s%s_%s_o3'%(str(start_t.year).zfill(4),str(start_t.month).zfill(2),str(start_t.day).zfill(2),identify),'w')

for i in range(int(endtime*3600/aadt)):
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
#for NH3 in nh3_ppt:
#  for tend in endtime:
ctr+=1
No_bg1 = str(float(Nobg1))
No_bg2 = str(float(Nobg2))
No_bg3 = str(float(Nobg3))

#rname = '%s_%s_vwl%1i_pwl%1i_hr%4.2e_nh3%s_orgfn%s_inorg%s_db%li'%(name,identify,vwl,pwl,endtime,NH3,org_nuc,inorg_nuc,db)
rname = '%s_%s_A%s_db%s_pwl%1i_vwl%1i_OH%s_FN%s_HOM%li_T%li_RH%li'%(name,identify,A,dbk,pwl,vwl,OH_scale,fn_scale,HOM_switch,T_switch,RH_switch)

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
f1.write('%e\n'%fn_scale)
f1.write('%8.1e\n'%nh3_ppt[0])
f1.write('%10.1f\n'%boxvol)
f1.write('%5.2f\n'%endtime) # ***
f1.write('%8.5f\n'%alpha)
f1.write('%i\n'%dbk)
f1.write('%f\n'%kc)
f1.write('%8.5f\n'%storg)
f1.write('%i\n'%HOM_switch)
f1.write('%i\n'%T_switch)
f1.write('%i\n'%RH_switch)
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
#f1.write('%15.5E %s\n'%(0.0,emiss_ippm))
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
f2.write('inorg_nuc    = %s\n'%inorg_nuc)
f2.write('nh3_ppt     = %s\n'%nh3_ppt[0])
f2.write('boxvol      = %s [cm3]\n'%boxvol)
f2.write('endtime     = %s [hours]\n'%endtime) # ***
f2.write('alpha       = %s\n'%alpha)
f2.write('Db switch   = %s [1/0]\n'%dbk)
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
#f2.write('emiss_ippm  = %s\n'%emiss_ippm)
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

runme_out = open('../runs/%s/%s.sh'%(rname,identify), mode='w')
#runme_out = open('../runs/%s/runme.sh'%(rname), mode='w')
for i in runme_line:
 runme_out.write(i)
 runme_out.write('\n')
runme_out.close()

#os.system('cd ../runs/%s/; qsub -cwd -V -pe MPI 1 -q %s ./runme.sh'%(rname, queue))
os.system('cd ../runs/%s/; sbatch ./%s.sh'%(rname,identify))
#os.system('cd ../runs/%s/; sbatch ./runme.sh'%(rname))

#os.system('sleep 1')
    
#keep the compute node from logging out before each box.exe has finished
#test=2
#while test>=1:
#    c=os.popen('ps -u alia').read()
#    b=re.findall('box.exe', c)
#    test=len(b)
#    os.system('sleep 2')



