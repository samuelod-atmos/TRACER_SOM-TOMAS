import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd

#boxvol = 10000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 456
srtorglast = srtorg1+iorg
#srtorglast2 = srtorglast 

output_dir = '../../outputs/'
#run = 'CstarNuc'
#run = 'NoHOM' 
#run = 'NoDbk'
#run = 'RHProfile'
#run = 'OHscale' 
#run = 'noSIVOC'
#run = 'Emiss2'
run = 'OH_test'
save_png = False

#======================================================================================

#for run in runs:
files  = ['%s04272016_%s_Cstar1e-09_T288.99_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run),
    '%s04282016_%s_Cstar1e-09_T288.76_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run),
    '%s05112016_%s_Cstar1e-09_T294.94_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run),
    '%s09112016_%s_Cstar1e-09_T296.47_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run),
    '%s09172016_%s_Cstar1e-09_T293.86_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run)]
  
for file in files:
  print('Running file:',file)
#  layer = 1
  time_pick = 150
  nlayers = 10
  endtime = 10.0
  print('endtime = ',endtime)
  #print(file[-33:-31])
  #sys.exit()
  delt = 30.0
  year = int(file[18:22])
  month = int(file[14:16])
  day = int(file[16:18])
  print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  Time = []
#startT = dt.datetime(year, month, day, 5, 30)
  if month==4 and day ==27:
    startT = dt.datetime(year, month, day, 12, 45)
  elif month==4 and day ==28:
    startT = dt.datetime(year, month, day, 10, 30)
  elif month==5 and day ==11:
    startT = dt.datetime(year, month, day, 12, 40)
  elif month==9 and day ==11:
    startT = dt.datetime(year, month, day, 10, 30)
  elif month==9 and day ==17:
    startT = dt.datetime(year, month, day, 9, 0)
  print('startT = ',startT)
  
  for i in range(int(endtime*3600/delt+1)):
    sec = int(i*delt)
  #  print(sec)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
  print(Time[0])
  print(Time[-1])
  print(np.shape(Time))
  
  #fid = np.load(file) # ,allow_pickle=True)
  #fid1 = np.load(file1,allow_pickle=True)
  #print(np.shape(fid))
  
  
  df_ae = np.array(pd.read_csv(file,header=None, delim_whitespace=True))
  Mk = df_ae[:,1:] #.109 xCLCCHO + yR6OOH + #3.543 XC
#  try:
  Mk = np.reshape(Mk, (Time.shape[0], nlayers, iorg+3, Mk.shape[1]))
  Mk = np.sum(Mk,axis=-1)
  print(np.shape(Mk))
  #sys.exit('Sucker')
  
  #nonvol = np.sum(fid[1:,srtorglast2,:],axis=1)/boxvol*1e9*100**3
  nonvol = Mk[time_pick,:,-3]#/boxvol*1e9*100**3
  so4 = Mk[time_pick,:,srtSO4]# /boxvol*1e9*100**3
  #
  #organic = np.sum(fid[1:,srtorg1:srtorglast,:],axis=2)
  #organic = np.sum(organic, axis=1)/boxvol*1e9*100**3
  #NH4 = np.sum(fid[1:,-2,:],axis=1)/boxvol*1e9*100**3
  H2O = Mk[time_pick,:,-1]#/boxvol*1e9*100**3
  print(np.shape(H2O))
  #sys.exit('Sucker')
  
  benz = Mk[time_pick,:,1:54]
  tolu = Mk[time_pick,:,55:95]
  xyle = Mk[time_pick,:,96:143]
  isop = Mk[time_pick,:,144:170]
  terp = Mk[time_pick,:,171:srtorglast]
  total= Mk[time_pick,:,srtorg1:srtorglast]
  total = np.sum(total, axis=1)
  
  print(np.shape(benz),np.shape(tolu),np.shape(xyle),np.shape(isop),np.shape(terp))
  
#    benz = np.sum(benz, axis=1)
#    tolu = np.sum(tolu, axis=1)
#    xyle = np.sum(xyle, axis=1)
#    isop = np.sum(isop, axis=1)
#    terp = np.sum(terp, axis=1)
    
  print('shape of SO4 = ',np.shape(so4))
  print('shape of nonvol = ',np.shape(nonvol))
  print('srtorglast = ',srtorglast)
  #print('srtorglast2 = ',srtorglast2)
  #print('shape of organic',np.shape(organic))
  #
  ##organics = np.sum(fid[:,srtorg1:srtorglast,:],axis=2)
  ##organics = np.sum(organics, axis=1)/boxvol*1e9*100**3
  #
  print('orgfrac =',nonvol[1]/(nonvol[1]+so4[1]))
  
  #file = '051120160.001_T298.0_h2so41.00e+07_NH34.93e+09_10.0_Mk.npy'
  #print('shape of organics =',np.shape(organics))
  #var2 = np.sum(var1,axis=1)
  #print(np.shape(var2))
  #var2 = var1
  
  #boxvol = 10000000.0
  #x = np.linspace(0,len(so4),len(so4))
#    x = mdates.date2num(Time)
  layers = np.arange(1,nlayers+1,1)
  plt.figure()
  fig = plt.gcf()
  ax = plt.gca()
  fig.set_size_inches(4,8)
  #plt.plot(x/360,(benz+tolu+xyle+isop+terp+nonvol)/(benz+tolu+xyle+isop+terp+nonvol+so4),label='Org. Frac.')
  #plt.plot(x/360,organic,label='Organics')
  #plt.plot(x/360,NH4,label='NH4')
  plt.plot(total,layers,label='Total Organics')
  #plt.plot(x/360,nonvol,label='Non-Vol.')
  plt.plot(so4,layers,label='Sulfate')
  plt.plot(H2O,layers,label='Water')
  #plt.plot(x/360,benz,label='Benzene')
  #plt.plot(x/360,tolu,label='Toluene')
  #plt.plot(x/360,xyle,label='m-Xylene')
  #plt.plot(x/360,isop,label='Isoprene')
  #plt.plot(x/360,terp,label='Terpene')
  plt.plot(nonvol,layers,label='Non-Volatile')
  plt.title('Aerosol Composition (%s/%s/%s)'%(month,day,year))
  plt.ylabel('Layer')
  plt.xlabel('$ \mu g $ $ m^{-3} $')
#  ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
  plt.grid(True)
  plt.legend()
  plt.ylim(0,)
  plt.show()
  if save_png==True:
    fig.savefig('%s-%s-%s_%s_AeroComp.png'%(year,month,day,run),bbox_inches='tight')
#  except:
#    print('Could not reshape (or something else) - moving on')
