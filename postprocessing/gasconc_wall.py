import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 

#==================================================================================
#==================================================================================

srtSO4 = 0
srtorg1 = 1
iorg = 456
srtorglast = srtorg1+iorg
output_dir = '../outputs'
endtime = 144.0
boxvol  = 2000000.0 

#===========================================================================================================
identify = 'debug'
db = [1E-15]
orgnuc = 1
inorgnuc = 1

#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_wallgc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])]
files = ['%s/20220801_%s_db1_pwl1_vwl1_OH1.0_FN100.0_HOM1_T1_RH1_wallgc.dat'%(output_dir,identify)]

save_png = False
delt = 300.0
#==================================================================================
# C* bin bounds 
l1,u1 = 1e-2,1e-1
l2,u2 = 1e-1,1e0
l3,u3 = 1e0,1e1
l4,u4 = 1e1,1e2
l5,u5 = 1e2,1e3
l6,u6 = 1e3,1e4



for file in files:
  year = 2022
  month = 8
  day = 1
  #print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  Time = []
  startT = dt.datetime(year, month, day, 11, 0)
  print('startT = ',startT)
  
  for i in range(int(endtime*3600/delt+1)):
    sec = int(i*delt)
  #  print(sec)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
  
  #    # ----------------------------------------------------------------------------
  print('file=',file)
  df_somgc = pd.read_csv(file,header=None,delim_whitespace=True)
  
  som_gas = np.array(df_somgc)
  #h2so4 = 
  som_gas = som_gas[:,1:-1]
  print('Shape of gas file:',np.shape(som_gas))
  
  #    # ----------------------------------------------------------------------------
  print(file)
  print('%s_spec.dat'%(file[:-7]))
  #sys.exit('Sucker')
  
  #df_spec = pd.read_csv('%s_spec.dat'%(file[:-11]), header=None, delim_whitespace=True)
  #df_spec = pd.read_csv('../outputs/20220801_A4e-3_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db1e-15_spec.dat', header=None, delim_whitespace=True)
  df_spec = pd.read_csv('%s/20220801_%s_db1_pwl1_vwl1_OH1.0_FN100.0_HOM1_T1_RH1_spec.dat'%(output_dir,identify),header=None, delim_whitespace=True)
  #som_spname = np.array(df_spec.iloc[2,1:iorg+2])
  som_cstar = np.array(df_spec.iloc[7,1:iorg+2])
 
  for i in range(len(som_cstar)):
    som_cstar[i] = float(som_cstar[i])

  
  print('len(som_cstar) =',len(som_cstar))
  cstar_n2_n1 = som_gas[:,np.where((som_cstar > l1) & (som_cstar < u1))[0]]
  cstar_n1_0 = som_gas[:,np.where((som_cstar > l2) & (som_cstar < u2))[0]]
  cstar_0_1 = som_gas[:,np.where((som_cstar > l3) & (som_cstar < u3))[0]]
  cstar_1_2 = som_gas[:,np.where((som_cstar > l4) & (som_cstar < u4))[0]]
  cstar_2_3 = som_gas[:,np.where((som_cstar > l5) & (som_cstar < u5))[0]]
  cstar_3_4 = som_gas[:,np.where((som_cstar > l6) & (som_cstar < u6))[0]]

  #print(np.shape(cstar_0_1))

  cstar_n2_n1 = np.sum(cstar_n2_n1,axis=1)/boxvol*1E6*1E9
  cstar_n1_0 = np.sum(cstar_n1_0,axis=1)/boxvol*1E6*1E9
  cstar_0_1 = np.sum(cstar_0_1,axis=1)/boxvol*1E6*1E9
  cstar_1_2 = np.sum(cstar_1_2,axis=1)/boxvol*1E6*1E9
  cstar_2_3 = np.sum(cstar_2_3,axis=1)/boxvol*1E6*1E9
  cstar_3_4 = np.sum(cstar_3_4,axis=1)/boxvol*1E6*1E9
  #print(np.shape(cstar_0_1))

  #sys.exit('Sucker')
  # ----------------------------------------------------------------------------

  x = mdates.date2num(Time[0:len(cstar_0_1)]-dt.timedelta(hours=6))
  #x = np.linspace(0,len(cstar_0_1),len(cstar_0_1))/360.
  ax = plt.gca()
  fig = plt.gcf()
  fig.set_size_inches(10,4)
  
  #plt.plot(x,cstar_n2_n1,color='black',label='C*=1E-2 - 1E-1')
  #plt.plot(x,cstar_n1_0,color='dimgrey',label='C*=1E-1 - 1')
  #plt.plot(x,cstar_0_1,color='grey',label='C*=1-10')
  #plt.plot(x,cstar_1_2,color='darkgrey',label='C*=10-100')
  #plt.plot(x,cstar_2_3,color='silver',label='C*=100-1000')
  #plt.plot(x,cstar_3_4,color='lightgrey',label='C*=1000-10000')

  plt.plot(x,cstar_n2_n1,label='C*=%s - %s'%(str(l1),str(u1)))
  plt.plot(x,cstar_n1_0,label='C*=%s - %s'%(str(l2),str(u2)))
  plt.plot(x,cstar_0_1,label='C*=%s - %s'%(str(l3),str(u3)))
  plt.plot(x,cstar_1_2,label='C*=%s-%s'%(str(l4),str(u4)))
  plt.plot(x,cstar_2_3,label='C*=%s-%s'%(str(l5),str(u5)))
  plt.plot(x,cstar_3_4,label='C*=%s-%s'%(str(l6),str(u6)))

  plt.title('Vapor Wall Losses')
  plt.xlabel('Date')
  plt.ylabel('ug/m^3',fontsize=12)
  plt.grid(True)
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
  #plt.yscale('log')
  #plt.ylim(0,2)
  plt.legend(loc='best',markerscale=4.)
  plt.show()
  
  #fig.savefig('20160917_GasConc.png',bbox_inches='tight')
  #fig.savefig('CAGE_GasWall.png',bbox_inches='tight')
