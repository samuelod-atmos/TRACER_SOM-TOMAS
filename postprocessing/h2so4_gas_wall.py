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
identify = 'sulfW'
files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_bg10_wallgc.dat'%(output_dir,identify)]

save_png = False
delt = 10.0
#==================================================================================

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
  h2so4 = som_gas[:,1]
  print('Shape of gas file:',np.shape(som_gas)) 
  #sys.exit('Sucker')
  # ----------------------------------------------------------------------------

  x = mdates.date2num(Time[0:len(h2so4)])
  #x = np.linspace(0,len(cstar_0_1),len(cstar_0_1))/360.
  ax = plt.gca()
  fig = plt.gcf()
  fig.set_size_inches(10,4)
  
  plt.plot(x,h2so4,color='r',label='Sulfuric Acid')

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
  fig.savefig('CAGE_H2SO4_Wall.png',bbox_inches='tight')
