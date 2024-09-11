import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd

boxvol = 2000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 456
icomp = 459
srtorglast = srtorg1+iorg
nbins = 40
#srtorglast2 = srtorglast 

output_dir = '../outputs'
save_png = False
identify = 'A2e-3'
endtime = 144.0
db = [1E-15]

#files = ['%s/20220801_vwl0_pwl0_hr7.20e+01_Pfunc_bg10_aemass.dat'%output_dir
#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_bg10_wallmk.dat'%(output_dir,identify)
files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_wallmk.dat'%(output_dir,identify,db[0])]
#files = ['%s/20220808_vwl0_pwl1_hr1.00e+01_no_particle_flow_bg10_aemass.dat'%output_dir
  #'%s04252016_%s_Cstar%s_T293.31_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
  #'%s05162016_%s_Cstar%s_T288.81_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar),
  #'%s05192016_%s_Cstar%s_T287.26_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar),
  #'%s09042016_%s_Cstar%s_T297.64_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar),
  #'%s09132016_%s_Cstar%s_T296.83_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar),
  #'%s09202016_%s_Cstar%s_T299.88_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar)]
  #]  
#files = [
#    '%s04272016_%s_Cstar%s_T287.62_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar),
#    '%s04282016_%s_Cstar%s_T285.89_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar),
#    '%s05112016_%s_Cstar%s_T293.72_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar),
#    '%s09112016_%s_Cstar%s_T298.11_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar),
#    '%s09172016_%s_Cstar%s_T295.18_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_aemass.dat'%(output_dir,run,cstar)]
for file in files:
  print('Running file:',file)
  print('endtime = ',endtime)
  #print(file[-33:-31])
  #sys.exit()
  delt = 10.0
  year = 2022
  month = 8
  day = 1
  print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  Time = []
  startT = dt.datetime(year, month, day, 11, 0)
  print('startT = ',startT)
  
  for i in range(int(endtime*3600/delt+1)):
    sec = int(i*delt)
    #print(sec)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
  #print(Time[0])
  #print(Time[-1])
  #print(np.shape(Time))
  
  #fid = np.load(file) # ,allow_pickle=True)
  #fid1 = np.load(file1,allow_pickle=True)
  #print(np.shape(fid))
  #print(file[:-9])
  #sys.exit('You sucker')
  df_spec = pd.read_csv('%s_spec.dat'%(file[:-11]), header=None, delim_whitespace=True)
  saprc_spname = np.array(df_spec.iloc[2,:])
  #print('saprc_spname =',saprc_spname)
  #sys.exit('You suck')
  
  df_ae = np.array(pd.read_csv(file,header=None, delim_whitespace=True))
  Mk = df_ae[:,1:] #.109 xCLCCHO + yR6OOH + #3.543 XC
#try:
  
  #print(np.shape(Mk))
  #print(int(len(Mk)/(icomp)))
  #print(Mk[0,:])
  #print(Mk[icomp-1,:])
  Mk = np.reshape(Mk, (int(len(Mk)/(icomp)), icomp,nbins))
  #print(np.shape(Mk))
  #print(Mk[0,0,:])
  #print(Mk[0,icomp-1,:])
  Mk = np.sum(Mk,axis=-1)
  print('np.shape(Mk)=',np.shape(Mk))
  #sys.exit()
  
  benzindx = []
  isopindx = []
  toluindx = []
  so2indx  = []
  sulfindx = []
  sesqindx = []
  terpindx = []
  trimindx = []
  xyleindx = []
  ivocindx = []
  svocindx = []
  
  for i in np.arange(0,len(saprc_spname)):
    temp = str(saprc_spname[i])
    if temp[:7] == 'BNZSOMG':
      benzindx.append(i-1)
    elif temp[0:7] == 'ISPSOMG':
      isopindx.append(i-1)
    elif temp[0:7] == 'TOLSOMG':
      toluindx.append(i-1)
    elif temp[0:7] == 'SESSOMG':
      sesqindx.append(i-1)
    elif temp[0:7] == 'TRPSOMG':
      terpindx.append(i-1)
    elif temp[0:7] == 'TRISOMG':
      trimindx.append(i-1)
    elif temp[0:7] == 'XYLSOMG':
      xyleindx.append(i-1)
    elif temp[0:7] == 'IVOSOMG':
      ivocindx.append(i-1)
    elif temp[0:7] == 'SVOSOMG':
      svocindx.append(i-1)

  #print('benzindx =',benzindx)
  #print('isopindx =',isopindx)
  #print('toluindx =',toluindx)
  #print('sesqindx =',sesqindx)
  #print('terpindx =',terpindx)
  #print('trimindx =',trimindx)
  #print('xyleindx =',xyleindx)
  #print('ivocindx =',ivocindx)
  #print('svocindx =',svocindx)
  #sys.exit()
  #nonvol = np.sum(fid[1:,srtorglast2,:],axis=1)/boxvol*1e9*100**3
  nonvol = Mk[0:,-3]#/boxvol*1e9*100**3
  so4 = Mk[0:,srtSO4]#/boxvol*1e9*100**3
  #so4 = so4 - so4[0]
  #nonvol = nonvol - nonvol[0]
  #
  #organic = np.sum(fid[1:,srtorg1:srtorglast,:],axis=2)
  #organic = np.sum(organic, axis=1)/boxvol*1e9*100**3
  #NH4 = np.sum(fid[1:,-2,:],axis=1)/boxvol*1e9*100**3
  H2O = Mk[0:,-1]#/boxvol*1e9*100**3
  #print(np.shape(H2O))
  #sys.exit('Sucker')
  
  benz = Mk[0:,benzindx]
  tolu = Mk[0:,toluindx]
  xyle = Mk[0:,xyleindx]
  isop = Mk[0:,isopindx]
  terp = Mk[0:,terpindx]
  ivoc = Mk[0:,ivocindx]
  svoc = Mk[0:,svocindx]
  total_org = Mk[0:,srtorg1:srtorglast]
  total = Mk[0:,:]
  #total = Mk[0:,:-1]
  total = np.sum(total, axis=1)#/boxvol*1e9*100**3
  
  #print(np.shape(benz),np.shape(tolu),np.shape(xyle),np.shape(isop),np.shape(terp))
  
  benz = np.sum(benz, axis=1)#/boxvol*1e9*100**3
  tolu = np.sum(tolu, axis=1)#/boxvol*1e9*100**3
  xyle = np.sum(xyle, axis=1)#/boxvol*1e9*100**3
  isop = np.sum(isop, axis=1)#/boxvol*1e9*100**3
  terp = np.sum(terp, axis=1)#/boxvol*1e9*100**3
  ivoc = np.sum(ivoc, axis=1)#/boxvol*1e9*100**3
  svoc = np.sum(svoc, axis=1)#/boxvol*1e9*100**3
 

  #print('sum(benz)=',sum(benz))
  #print('sum(tolu)=',sum(tolu))
  #print('sum(xyle)=',sum(xyle))
  #print('sum(isop)=',sum(isop))
  #print('sum(terp)=',sum(terp))
  #print('sum(ivoc)=',sum(ivoc))
  #print('sum(svoc)=',sum(svoc))
  #print('sum(H2O)=',sum(H2O))
  #sys.exit('you will bever graduate')
  
  #print('shape of SO4 = ',np.shape(so4))
  #print('shape of nonvol = ',np.shape(nonvol))
  #print('srtorglast = ',srtorglast)
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
  #x = np.linspace(0,len(Mk),len(Mk))
  x = mdates.date2num(Time[0:len(total)])
  plt.figure()
  fig = plt.gcf()
  ax = plt.gca()
  fig.set_size_inches(10,4)
  #plt.plot(x/360,(benz+tolu+xyle+isop+terp+nonvol)/(benz+tolu+xyle+isop+terp+nonvol+so4),label='Org. Frac.')
  #plt.plot(x/360,organic,label='Organics')
  #plt.plot(x/360,NH4,label='NH4')
  plt.plot(x,total,label='Total')
  #plt.plot(x/360,nonvol,label='Non-Vol.')
  plt.plot(x,so4,color='r',label='Sulfate')
  #plt.plot(x,H2O,label='Water')
  plt.plot(x,benz,color='y',label='Benzene')
  plt.plot(x,tolu,color='b',label='Toluene')
  plt.plot(x,xyle,color='cyan',label='m-Xylene')
  plt.plot(x,isop,color='green',label='Isoprene')
  plt.plot(x,terp,color='lime',label='Terpene')
  #plt.plot(x,ivoc,label='IVOC')
  #plt.plot(x,svoc,label='SVOC')
  plt.plot(x,nonvol,color='k',label='Non-Volatile')
  plt.title('Aerosol Mass on walls (%s/%s/%s)'%(month,day,year))
  plt.xlabel('Date')
  plt.ylabel('$ \mu g $ $ m^{-3} $')
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
  plt.grid(True)
  plt.yscale('log')
  plt.legend()
  plt.ylim(0.0001,2.0)
  plt.show()
  if save_png==True:
    fig.savefig('CAGE_WallAeroComp.png',bbox_inches='tight')
  #except:
  #print('Could not reshape (or something else) - moving on')
