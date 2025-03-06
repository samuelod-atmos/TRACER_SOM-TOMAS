from pylab import * 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 
#from BG_sizedist import SD_smps
from matplotlib.gridspec import GridSpec
from functions import h,closest
from scipy.optimize import curve_fit
import sys
from scipy import signal
#import pygsheets as pyg

#===========================================================================================================
def smoothdist(dist):
  sdist=np.empty(dist.shape)
  sdist[0]=dist[0]*0.75 + dist[1]*0.25
  sdist[1:-1]=dist[:-2]*0.25 + dist[1:-1]*0.5 + dist[2:]*0.25
  sdist[-1]=dist[-2]*0.25 + dist[-1]*0.75
  return sdist
#===========================================================================================================

output_dir = '../outputs'
save_png = False 
#save_png = True

boxvol = 2000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 477
icomp = iorg + 3
srtorglast = srtorg1+iorg
nbins = 40
#===========================================================================================================
db = 1
pwl = 1
vwl = 1
OH = 1.0
fn = 100.0
HOM = 1
T = 1
RH = 1

identify = 'multi'
#==========================================================================================================

startT = dt.datetime(2022,8,1,11)
endtime = 144.0


#rname = '%s/%s%s%s_%s_vwl1_pwl1_hr%4.2e_nh35000_orgfn%s_inorg%s_db%s_noconc.dat'%(output_dir,str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify,endtime,orgnuc,inorgnuc,db[0])
rname = '%s/20220801_%s_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_noconc.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))


df_no = np.array(pd.read_csv(rname,header=None, delim_whitespace=True))
print('shape of df_no=',np.shape(df_no))
ibins = 40
#endtime = 10.0
delt = 300.0

number_conc = df_no[:,1:]

Time = []
#for i in range(int(endtime[0]*3600/delt+1)):
for i in range(len(df_no)):
  sec = int(i*delt)
  Time.append(sec)
Time = np.array(Time)

#year = int(rname[11:15])
#month = int(rname[15:17])
#day = int(rname[17:19])
print(startT)

date = []
date.append(startT)
date_step = startT

for i in range(len(Time)-1):
  #print(Time[i+1])
  date_step = date_step + dt.timedelta(seconds=delt)
  date.append(date_step)
#print(len(date))
date = np.array(date)
#print(len(date))

#sys.exit()

   #=============================================================================

#SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
#low_bin, up_bin, upperbin,lowerbin = 0, 85, 10, 0
#low_bin, up_bin, upperbin,lowerbin = 0, 85, 10, 4
#model_counter,smps_counter = 8,100 
#nuc = True

####################################################################

Bins = np.array([1.2350826156568765E-002,
1.5561065965403546E-002,
1.9605714703615617E-002,
2.4701652823409345E-002,
3.1122132573709296E-002,
3.9211430217237254E-002,
4.9403306667362333E-002,
6.2244266433223019E-002,
7.8422862054486592E-002,
9.8806615375812007E-002,
.12448853543805495,
.15684572734899740,
.19761323483379878,
.24897707601932786,
.31369146117804336,
.39522647783194720,
.49795416232509176,
.62738293531618428,
.79045297199259412,
.99590834522305627,
1.2547658965525639,
1.5809059766425884,
1.9918167315918585,
2.5095318449455197,
3.1618120185999783,
3.9836335454752101,
5.0190637935718252,
6.3236241678295615,
7.9672672555334119,
10.038127794505227,
12.647248596918340,
15.934534840232814,
20.076256003733615,
25.294497716355124,
31.869070338797616,
40.152512836913573,
50.588996477747159,
63.738141994259244,
80.305027332719860,
101.17799504556817])

BinEdge = np.array([1.1003335152977913E-002,
1.3863333673745220E-002,
1.7466706037540244E-002,
2.2006670760556325E-002,
2.7726667920251188E-002,
3.4933412796713817E-002,
4.4013342430313677E-002,
5.5453336986023886E-002,
6.9866827036694307E-002,
8.8026686679029437E-002,
0.11090667626309085,
0.13973365695992204,
0.17605337699486312,
0.22181335710826797,
0.27946731969291105,
0.35210676126333484,
0.44362672338070858,
0.55893465093195627,
0.70421353707388734,
0.88725346508976299,
1.1178693249561813,
1.4084271032422104,
1.7745069668362181,
2.2357386960969010,
2.8168542646732937,
3.5490140069858223,
4.4714774845628806,
5.6337086457243348,
7.0980281605984192,
8.9429551538639238,
11.267417524204170,
14.196056614450397,
17.885910677204180,
22.534835513919351,
28.392113815407917,
35.771822093361038,
45.069671958860738,
56.784228803830111,
71.543645664627462,
90.139345779765591,
113.56845995368882])

BinEdge = BinEdge*100
BinsE = np.log10(BinEdge[1:]/BinEdge[:-1])

Bins = Bins*100
n=3;m=3
Y = (number_conc[:,:])/BinsE[:]

plt.rcParams.update({'font.size': 11})

fig, axes = plt.subplots(nrows=5, ncols=1,sharex=True)
fig.set_size_inches(15,8)

#x = mdates.date2num(date-dt.timedelta(hours=6))
x = mdates.date2num(date)
print('len(x) =',len(x))
c1 = axes[0].pcolormesh(x,Bins[:],np.log10(np.transpose(Y)),cmap='rainbow')

axes[0].grid(True)
axes[0].set_title('Model') 
axes[0].set_ylabel('Dp (nm)')
#axes[0].set_xlabel('Date',fontsize=22)

if len(x) < 300:
  axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  axes[0].xaxis.set_major_locator(mdates.HourLocator(interval = 3))
else:
  axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

axes[0].set_yscale('log')
#axes.locator_params(axis='x',nbins=3)
plt.subplots_adjust(hspace=0.1)

axes[0].locator_params(axis='x', nbins=6)
axes[0].set_ylim(12,100)
#axes[0].set_ylim(1.2,600)
#cb1 = fig.colorbar(c1, format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),ax=axes,shrink=0.9,pad=0.061, label='$ dN/dlog_{10}(D_p) $')
c1.set_clim(1,4.3)


ax2 = axes[0].twinx()

#cs_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_cs.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])
#cs_file = '%s/%s%s%s_%s_vwl1_pwl1_hr%4.2e_nh35000_orgfn%s_inorg%s_db%s_cs.dat'%(output_dir,str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify,endtime,orgnuc,inorgnuc,db[0])
cs_file = '%s/20220801_%s_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_cs.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))

cs_array = np.array(pd.read_csv(cs_file,header=None,delim_whitespace=True))
print('initial shape of array:',np.shape(cs_array))
cs_array = cs_array[:,1]
print('len CS array=',len(cs_array),len(x))

ax2.plot(x[:len(cs_array)],cs_array,color='k')
ax2.set_yscale('log')
ax2.set_ylabel('CS [$s^{-1}$]')
ax2.set_ylim(0.00001,0.01)

#=============================================================================================

#spname_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_spec.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])
#spname_file = '%s/%s%s%s_%s_vwl1_pwl1_hr%4.2e_nh35000_orgfn%s_inorg%s_db%s_spec.dat'%(output_dir,str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify,endtime,orgnuc,inorgnuc,db[0])
spname_file = '%s/20220801_%s_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_spec.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))

#spname_file = '../outputs/20220801_styre_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db1e-15_spec.dat'
df_spec = pd.read_csv(spname_file, header=None, delim_whitespace=True)
saprc_spname = np.array(df_spec.iloc[1,1:1505])

benzindx = int(np.where(saprc_spname=='BENZENE')[0])
isopindx = int(np.where(saprc_spname=='ISOPRENE')[0])
toluindx = int(np.where(saprc_spname=='TOLUENE')[0])
so2indx  = int(np.where(saprc_spname=='SO2')[0])
sesqindx = int(np.where(saprc_spname=='SESQTRP')[0])
terpindx = int(np.where(saprc_spname=='TERPENE')[0])
trimindx = int(np.where(saprc_spname=='TRIMBNZ')[0])
xyleindx = int(np.where(saprc_spname=='XYLENE')[0])
ivocindx = int(np.where(saprc_spname=='IVOC')[0])
svocindx = int(np.where(saprc_spname=='SVOC')[0])
styrindx = int(np.where(saprc_spname=='STYRENE')[0])

print('benzindx =',benzindx)

#gcfile = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_saprcgc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])
#gcfile = '%s/%s%s%s_%s_vwl1_pwl1_hr%4.2e_nh35000_orgfn%s_inorg%s_db%s_saprcgc.dat'%(output_dir,str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify,endtime,orgnuc,inorgnuc,db[0])
gcfile = '%s/20220801_%s_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_saprcgc.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))

df_saprcgc = pd.read_csv(gcfile,header=None,delim_whitespace=True,)

saprc_gas = np.array(df_saprcgc)
print('shape of saprc_gas =',np.shape(saprc_gas[:,103:]))

benz    = saprc_gas[:,benzindx]*1000 # ppm -> ppb 
isop    = saprc_gas[:,isopindx]*1000
tolu    = saprc_gas[:,toluindx]*1000
so2     = saprc_gas[:,so2indx]*1000
sesqtrp = saprc_gas[:,sesqindx]*1000
terp    = saprc_gas[:,terpindx]*1000
trimeth = saprc_gas[:,trimindx]*1000
xylene  = saprc_gas[:,xyleindx]*1000
ivoc    = saprc_gas[:,ivocindx]*1000
svoc    = saprc_gas[:,svocindx]*1000
styr    = saprc_gas[:,styrindx]*1000
print('benz shape =',np.shape(benz),np.shape(isop))

axes[4].plot(x,benz,color='y',label='Benzene')
axes[4].plot(x,isop,color='g',label='Isoprene')
axes[4].plot(x,tolu,color='brown',label='Toluene')
axes[4].plot(x,terp,color='m',label='Terpenes')
axes[4].plot(x,trimeth,color='c',label='Trimethylbenzene')
axes[4].plot(x,xylene,color='lime',label='M-Xylene')
axes[4].plot(x,styr,color='blue',label='Styrene')
axes[3].plot(x,so2,color='orange',linestyle='--',label='SO2')
axes[3].set_ylabel('[ppbv]',color='orange')
axes[3].legend(loc=4,prop={'size': 6})
axes[3].set_ylim(0,)

axes[4].set_ylabel('[ppbv]')
axes[4].legend(loc=2,prop={'size': 5})
axes[4].set_ylim(0,)
#=============================================================================================

ax2 = axes[3].twinx()

#gc_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_gc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])
#gc_file = '%s/%s%s%s_%s_vwl1_pwl1_hr%4.2e_nh35000_orgfn%s_inorg%s_db%s_gc.dat'%(output_dir,str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify,endtime,orgnuc,inorgnuc,db[0])
gc_file = '%s/20220801_%s_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_gc.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))

df_saprcgc = pd.read_csv(gc_file,header=None,delim_whitespace=True,)

saprc_gas = np.array(df_saprcgc)
#print(np.shape(saprc_gas))
#sys.exit()

sulf = saprc_gas[:,1]
print(np.shape(sulf))

#for i in range(len(saprc_gas)):
#  sec = int(i*delt)
#  print(sec)
#  Time.append(startT + dt.timedelta(seconds = sec))
#Time = np.array(Time)

sulf = sulf/boxvol*1000.0/98.0*6.022e23

ax2.plot(x,sulf,color='r',linestyle='--',label='H2SO4')
ax2.set_yscale('log')
ax2.set_ylim(10**6,10**8)
ax2.set_ylabel('H2SO4 \n [molec/cm^3]',color='r')
ax2.legend(loc=1,prop={'size':6})
ax2.grid(True)

#=============================================================================================

ax2 = axes[1].twinx()

#oh_fid = open('../inputs/timeseries/20220801_%s_OH'%identify,'r')
oh_fid = open('../inputs/timeseries/%s%s%s_%s_OH'%(str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify),'r')

OH = []
for line in oh_fid.readlines():
 OH.append(float(line))

OH = np.array(OH)

#OH = signal.savgol_filter(OH,101,2)
OH = OH[::30]

#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)

#matplotlib.axes.Axes.ticklabel_format(axis=['y'],style='sci')
#plt.ticklabel_format(axis='y',style='sci')

#x = np.linspace(0,len(OH),len(OH))/360.
axes[1].plot(x,OH,color='purple')
#axes[2].set_xlabel('Time [hours]')
axes[1].set_ylabel('OH \n[molec/cm^3]',color='purple')
#axes[2].set_title('OH') 
axes[1].set_yscale('log')

#o3_fid = open('../inputs/timeseries/20220801_%s_o3'%identify,'r')
o3_fid = open('../inputs/timeseries/%s%s%s_%s_o3'%(str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify),'r')

o3 = []
for line in o3_fid.readlines():
 o3.append(float(line))

o3 = np.array(o3)
o3 = signal.savgol_filter(o3,101,2)
o3 = o3[::30]
#o3 = o3[:len(x)]
#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)

#matplotlib.axes.Axes.ticklabel_format(axis=['y'],style='sci')
#plt.ticklabel_format(axis='y',style='sci')

#x = np.linspace(0,len(OH),len(OH))/360.

ax2.plot(x,o3,color='r')
ax2.set_ylabel('Ozone [ppb]',color='r')
ax2.set_ylim(0,)

#axes[2].set_title('') 

#=============================================================================================

ax2 = axes[2].twinx()

#rh_fid = open('../inputs/timeseries/20220801_%s_RH'%identify,'r')
rh_fid = open('../inputs/timeseries/%s%s%s_%s_RH'%(str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify),'r')

RH = []
for line in rh_fid.readlines():
 RH.append(float(line))

RH = np.array(RH)
RH = signal.savgol_filter(RH,101,2)
RH = RH[::30]
#matplotlib.axes.Axes.ticklabel_format(axis=['y'],style='sci')
#plt.ticklabel_format(axis='y',style='sci')

#x = np.linspace(0,len(RH),len(RH))/360.
axes[2].plot(x[:len(RH)],RH*100.,color='green')
axes[2].set_xlabel('Date')
axes[2].set_ylabel('RH [%]',color='green')
#axes[2].set_ylim(0,2)

#T_fid = open('../inputs/timeseries/20220801_%s_Temp'%identify,'r')
T_fid = open('../inputs/timeseries/%s%s%s_%s_Temp'%(str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify),'r')

Temp = []
for line in T_fid.readlines():
 Temp.append(float(line))

Temp = np.array(Temp)
Temp = signal.savgol_filter(Temp,101,2)
Temp = Temp[::30]


#matplotlib.axes.Axes.ticklabel_format(axis=['y'],style='sci')
#plt.ticklabel_format(axis='y',style='sci')

#x = np.linspace(0,len(RH),len(RH))/360.
ax2.plot(x,Temp,color='blue')
#ax2.set_xlabel('Time [hours]')
ax2.set_ylabel('T [K]',color='blue')

#=============================================================================================
'''
#ax2 = axes[5].twinx()

aemass_wall_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_wallmk.dat'%(output_dir,identify,db[0])

df_ae = np.array(pd.read_csv(aemass_wall_file,header=None, delim_whitespace=True))
Mk = df_ae[:,1:] #.109 xCLCCHO + yR6OOH + #3.543 XC
Mk = np.reshape(Mk, (int(len(Mk)/(icomp)), icomp,nbins))
Mk = np.sum(Mk,axis=-1)


so4 = Mk[0:,srtSO4]#/boxvol*1e9*100**3
total_org = Mk[0:,srtorg1:srtorglast]
total_org = np.sum(total_org, axis=1)#/boxvol*1e9*100**3

axes[5].plot(x,total_org,color='green',label='Total Org.')
#plt.plot(x/360,nonvol,label='Non-Vol.')
axes[5].plot(x,so4,color='r',label='Sulfate')

axes[5].set_ylabel('$ \mu g $ $ m^{-3} $')
axes[5].set_yscale('log')
axes[5].legend()
axes[5].set_ylim(0.00001,2.0)



aemass_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_aemass.dat'%(output_dir,identify,db[0])

df_ae = np.array(pd.read_csv(aemass_file,header=None, delim_whitespace=True))
Mk = df_ae[:,1:] #.109 xCLCCHO + yR6OOH + #3.543 XC
Mk = np.reshape(Mk, (int(len(Mk)/(icomp)), icomp,nbins))
Mk = np.sum(Mk,axis=-1)


so4 = Mk[0:,srtSO4]#/boxvol*1e9*100**3
total_org = Mk[0:,srtorg1:srtorglast]
total_org = np.sum(total_org, axis=1)#/boxvol*1e9*100**3

#ax2.plot(x,total_org,color='green',label='Total Org.')
#ax2.plot(x,so4,color='r',label='Sulfate')
#ax2.set_ylabel('$ \mu g $ $ m^{-3} $')
#ax2.set_yscale('log')
#ax2.legend()
#ax2.set_ylim(0.000001,0.3)

axes[5].plot(x,total_org,color='green',linestyle='--',label='Total Org.')
axes[5].plot(x,so4,color='r',linestyle='--',label='Sulfate')

#org_frac = total_org/(total_org+so4)
#ax2.plot(x,org_frac,color='k',linestyle='--',label='organic fraction')
#ax2.set_ylabel('Org. Frac.')
#ax2.set_ylim(0,1)

#=============================================================================================

gc_wall_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_wallgc.dat'%(output_dir,identify,db[0])
# C* bin bounds 
l1,u1 = 1e-2,1e-1
l2,u2 = 1e-1,1e0
l3,u3 = 1e0,1e1
l4,u4 = 1e1,1e2
l5,u5 = 1e2,1e3
l6,u6 = 1e3,1e4


df_somgc = pd.read_csv(gc_wall_file,header=None,delim_whitespace=True)
som_gas = np.array(df_somgc)
som_gas = som_gas[:,1:-1]

df_spec = pd.read_csv('%s_spec.dat'%(gc_wall_file[:-11]), header=None, delim_whitespace=True)
som_spname = np.array(df_spec.iloc[2,1:iorg+2])
som_cstar = np.array(df_spec.iloc[7,1:iorg+2])

for i in range(len(som_cstar)):
  som_cstar[i] = float(som_cstar[i])

cstar_n2_n1 = som_gas[:,np.where((som_cstar > l1) & (som_cstar < u1))[0]]
cstar_n1_0 = som_gas[:,np.where((som_cstar > l2) & (som_cstar < u2))[0]]
cstar_0_1 = som_gas[:,np.where((som_cstar > l3) & (som_cstar < u3))[0]]
cstar_1_2 = som_gas[:,np.where((som_cstar > l4) & (som_cstar < u4))[0]]
cstar_2_3 = som_gas[:,np.where((som_cstar > l5) & (som_cstar < u5))[0]]
cstar_3_4 = som_gas[:,np.where((som_cstar > l6) & (som_cstar < u6))[0]]

cstar_n2_n1 = np.sum(cstar_n2_n1,axis=1)/boxvol*1E6*1E9
cstar_n1_0 = np.sum(cstar_n1_0,axis=1)/boxvol*1E6*1E9
cstar_0_1 = np.sum(cstar_0_1,axis=1)/boxvol*1E6*1E9
cstar_1_2 = np.sum(cstar_1_2,axis=1)/boxvol*1E6*1E9
cstar_2_3 = np.sum(cstar_2_3,axis=1)/boxvol*1E6*1E9
cstar_3_4 = np.sum(cstar_3_4,axis=1)/boxvol*1E6*1E9

#axes[6].plot(x,cstar_n2_n1,label='C*=%s - %s'%(str(l1),str(u1)))
#axes[6].plot(x,cstar_n1_0,label='C*=%s - %s'%(str(l2),str(u2)))
#axes[6].plot(x,cstar_0_1,label='C*=%s - %s'%(str(l3),str(u3)))
#axes[6].plot(x,cstar_1_2,label='C*=%s-%s'%(str(l4),str(u4)))
#axes[6].plot(x,cstar_2_3,label='C*=%s-%s'%(str(l5),str(u5)))
#axes[6].plot(x,cstar_3_4,label='C*=%s-%s'%(str(l6),str(u6)))

axes[6].plot(x,cstar_n2_n1,color='1.0',label='C*=%s - %s'%(str(l1),str(u1)))
axes[6].plot(x,cstar_n1_0, color='0.8',label='C*=%s - %s'%(str(l2),str(u2)))
axes[6].plot(x,cstar_0_1,  color='0.6',label='C*=%s - %s'%(str(l3),str(u3)))
axes[6].plot(x,cstar_1_2,  color='0.4',label='C*=%s-%s'%(str(l4),str(u4)))
axes[6].plot(x,cstar_2_3,  color='0.2',label='C*=%s-%s'%(str(l5),str(u5)))
axes[6].plot(x,cstar_3_4,  color='0.1',label='C*=%s-%s'%(str(l6),str(u6)))

#plt.title('Vapor Wall Losses')
#plt.xlabel('Date')
axes[6].set_ylabel('ug/m^3',fontsize=12)
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
#plt.yscale('log')
#plt.ylim(0,2)
axes[6].legend(loc='best',fontsize=5)


gc_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_gc.dat'%(output_dir,identify,db[0])
# C* bin bounds 
l1,u1 = 1e-2,1e-1
l2,u2 = 1e-1,1e0
l3,u3 = 1e0,1e1
l4,u4 = 1e1,1e2
l5,u5 = 1e2,1e3
l6,u6 = 1e3,1e4


df_somgc = pd.read_csv(gc_file,header=None,delim_whitespace=True)
som_gas = np.array(df_somgc)
som_gas = som_gas[:,1:-1]

df_spec = pd.read_csv('%s_spec.dat'%(gc_file[:-7]), header=None, delim_whitespace=True)
som_spname = np.array(df_spec.iloc[2,1:iorg+2])
som_cstar = np.array(df_spec.iloc[7,1:iorg+2])

for i in range(len(som_cstar)):
  som_cstar[i] = float(som_cstar[i])

cstar_n2_n1 = som_gas[:,np.where((som_cstar > l1) & (som_cstar < u1))[0]]
cstar_n1_0 = som_gas[:,np.where((som_cstar > l2) & (som_cstar < u2))[0]]
cstar_0_1 = som_gas[:,np.where((som_cstar > l3) & (som_cstar < u3))[0]]
cstar_1_2 = som_gas[:,np.where((som_cstar > l4) & (som_cstar < u4))[0]]
cstar_2_3 = som_gas[:,np.where((som_cstar > l5) & (som_cstar < u5))[0]]
cstar_3_4 = som_gas[:,np.where((som_cstar > l6) & (som_cstar < u6))[0]]

cstar_n2_n1 = np.sum(cstar_n2_n1,axis=1)/boxvol*1E6*1E9
cstar_n1_0 = np.sum(cstar_n1_0,axis=1)/boxvol*1E6*1E9
cstar_0_1 = np.sum(cstar_0_1,axis=1)/boxvol*1E6*1E9
cstar_1_2 = np.sum(cstar_1_2,axis=1)/boxvol*1E6*1E9
cstar_2_3 = np.sum(cstar_2_3,axis=1)/boxvol*1E6*1E9
cstar_3_4 = np.sum(cstar_3_4,axis=1)/boxvol*1E6*1E9

axes[6].plot(x,cstar_n2_n1,color='1.0') #,label='C*=%s - %s'%(str(l1),str(u1)))
axes[6].plot(x,cstar_n1_0, color='0.8') #,label='C*=%s - %s'%(str(l2),str(u2)))
axes[6].plot(x,cstar_0_1,  color='0.6') #,label='C*=%s - %s'%(str(l3),str(u3)))
axes[6].plot(x,cstar_1_2,  color='0.4') #,label='C*=%s-%s'%(str(l4),str(u4)))
axes[6].plot(x,cstar_2_3,  color='0.2') #,label='C*=%s-%s'%(str(l5),str(u5)))
axes[6].plot(x,cstar_3_4,  color='0.1') #,label='C*=%s-%s'%(str(l6),str(u6)))

#plt.title('Vapor Wall Losses')
#plt.xlabel('Date')
axes[6].set_ylabel('ug/m^3',fontsize=12)
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
axes[6].set_yscale('log')
axes[6].set_ylim(0.00001,2)
axes[6].legend(loc='best',fontsize=5)
'''

#=============================================================================================

plt.show()
if save_png==True:
  fig.savefig('%s_gas_summary_fig.png'%rname[len(output_dir)+1:-11],bbox_inches='tight')
