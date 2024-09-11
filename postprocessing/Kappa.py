import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from pylab import * 
import pandas as pd 
import sys
import datetime as dt
from functions import h,closest
from matplotlib import rcParams
import matplotlib.dates as mdates 
rcParams.update({'figure.autolayout': True})

output_dir = '../outputs/'
what = 'bar' # 'bar' or 'layers'


save_png = False
#fig = plt.gcf()
#fig.set_size_inches(8,5)

#=============================================================================
ibins = 40
Dpedge = np.zeros(ibins+1)
Dp_low = 1E-9
Dpedge[0] = Dp_low 
rho_p = 1770.0
for i in range(1,ibins+1):
  Dpedge[i]=Dpedge[i-1]*2**(1./3.) 

MNedge = rho_p*pi/6.*Dpedge**3 
MNcenter = sqrt(MNedge[:-1]*MNedge[1:]) 
Dpcenter = (MNcenter/rho_p*6./pi)**(1./3.) # mDpedge[0] = Dp_low #jrp
#print('Dpcenter[0] =',Dpcenter[0])

#=============================================================================

file = '%s/20220731_vwl1_pwl1_hr7.20e+01_A7.2e-4_bg10_noconc.dat'%output_dir
  
df_k = np.array(pd.read_csv(file,header=None, delim_whitespace=True))
ibins = 40
endtime = 72.0
delt = 10.0
year = int(file[12:16])
month = int(file[16:18])
day = int(file[18:20])

print(year,month,day)
#=============================================================================
startT = dt.datetime(year,month,day,11)
print('startT = ',startT)

Time = []
for i in range(int(endtime*3600/delt+1)):
  sec = int(i*delt)
#  print(sec)
  Time.append(startT + dt.timedelta(seconds = sec))
Time = np.array(Time)
print(Time[0])
print(Time[-1])
print(np.shape(Time))
print('np.shape(Time) =',np.shape(Time)[0])
kappa_df = df_k[:,1:]
print('Shape oc kappa_df =',np.shape(kappa_df))
#kappa_df = np.reshape(kappa_df, (np.shape(Time)[0]-1,nlayers, ibins))
#print('shape of kappa_df =',np.shape(kappa_df))
#sys.exit()

if what=='bar':
  df = pd.DataFrame()
  df['Kappa'] = kappa_df[-1,:]
  df['Bins'] = Dpcenter*1E6
  #print(Dpcenter*1E6)
  #fig = plt.gcf()
  #fig.set_size_inches(8,5)
  
  ax = df.plot.bar(x='Bins',y='Kappa',rot=0,edgecolor='black')
  ax.set_title('%s/%s/%s'%(month,day,year))
  ax.set_ylabel('Kappa')
  ax.set_xlabel('$ D_p $ $ [nm] $')
  ax.set_xticklabels(np.round(Dpcenter*1E9,1), rotation=90)
  plt.show()

if what=='layers':
  x = mdates.date2num(Time[:-1])
  fig, axs = plt.subplots(nrows=nlayers, ncols=1, figsize=(12, 9),constrained_layout=True)
  for i in range(nlayers):  
    c = axs[i].pcolormesh(x,Dpcenter*1E9,np.transpose(kappa_df[:,i,:]),cmap='rainbow')
    axs[i].grid(True)
    axs[i].set_ylabel('Layer: %s \n Dp (nm)'%abs(i-nlayers))
    axs[i].set_yscale('log')
    axs[i].set_xticklabels([])
#    c.set_clim(1,4.3)

#  cb = fig.colorbar(c, format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),ax=axs[nlayers-1],shrink=0.6,location='bottom',label='$ Kappa $')
  cb = fig.colorbar(c, ax=axs[nlayers-1],shrink=0.6,location='bottom',label='$ Kappa $')
  axs[nlayers-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  plt.setp(plt.xticks()[1], rotation=45)
  #cb = fig.colorbar(c, pad=.006, label='$ N $ $ cm^{-3} $')
  axs[nlayers-1].set_xlabel('Time [CDT]') 
  axs[0].set_title('%s/%s/%s - %s'%(month,day,year,run)) 
  plt.show()
#    axs[i].set_xticklabels([])

#=============================================================================
#final = number_conc[index,layer-1,0:]/np.log10(Dpedge[1:]/Dpedge[:-1])
#  initial = number_conc[0,layer-1,0:]/np.log10(Dpedge[1:]/Dpedge[:-1])
#  print('final = ',final)
#  fig = plt.gcf()
#  fig.set_size_inches(8,5)
#plt.semilogx(1E9*Dpcenter,final)

#=============================================================================
#No1, No2, sigma1, sigma2, mu1, mu2 = SD_smps(SMPS_sheetname,SMPS_upper)
#print(No1, No2, sigma1, sigma2, mu1, mu2)
#obs = h(Dpcenter*1E9,No1,No2,sigma1,sigma2,mu1,mu2)
#plt.semilogx(1E9*Dpcenter,obs)
#=============================================================================

#plt.plot(np.arange(0,len(fid[0][1])),(fid[0][1]/boxvol),label='Initial')
#plt.plot(np.arange(0,len(fid[0][-1])),(fid[0][-1]/boxvol),label='Final')
#plt.plot(Bins,initial/boxvol,label='Initial')
#plt.plot(Bins,final/boxvol,label='Initial')
#runs.append('Obs')
#print('runs =',runs)
#plt.bar(1E9*Dpcenter,kappa_df[0,layer,:])
#plt.title('%s/%s/%s'%(month,day,year)) 
#plt.xlabel('$ D_p $ $ (nm) $')
#plt.ylabel('Kappa')
#plt.annotate('Total Number = %4.2f [#/cm^3]' % (np.sum(final)/boxvol),xy=(150,4500))
#plt.xlim(12,1000) 
#plt.ylim(0,)
#plt.legend()
#plt.grid(True)
#plt.show()

#fig.savefig('%s-%s-%s_FinalSD_compare.png'%(year,month,day),bbox_inches='tight')
