import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates 

#----------------------------------------------------------------------------------------------------------
output_dir = '../outputs/'
endtime = 72.0
delt = 10.0

#----------------------------------------------------------------------------------------------------------

#==========================================================================================================
name = '20220801'
identify = 'Nkout'
#==========================================================================================================

files = ['%s/20220801_%s_vwl0_pwl1_hr7.20e+01_bg10_cs.dat'%(output_dir,identify)
]
#==========================================================================================================

for file in files: 
  year = 2022
  month = 8
  day = 1
  print('Year = ',year,'Month = ', month,'Day = ', day) 
  startT = dt.datetime(year,month,day,11)
  
  Time = []
  
  for i in range(int(endtime*3600/delt+1)):
    sec = int(i*delt)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
  #print('shape Time = ',np.shape(Time)[0])
  #----------------------------------------------------------------------------------------------------------
  cs_array = np.array(pd.read_csv(file,header=None,delim_whitespace=True))
  print('initial shape of array:',np.shape(cs_array))
  cs_array = cs_array[:,1]

  #cs_array = np.reshape(cs_array, (np.shape(Time)[0]-1,2))
  #print('reshaped cs_array:',np.shape(cs_array))
  
  fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)
  fig = plt.gcf()
  fig.set_size_inches(10,4)

  x = mdates.date2num(Time[1:])
  #plt.plot(x,1/cs_array/3600.)
  plt.plot(x,cs_array)
  
  plt.ylabel('Cond. Sink [$ s^{-1} $]')
  #plt.ylabel('1/(CS) [$ hours $]')
  plt.xlabel('Time')
  plt.title('Condensation Sink - %s/%s/%s'%(month,day,year)) 
  axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
  #plt.yscale('log')
  #plt.grid(True)
  #plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
  plt.show()
  #fig.savefig('%s-%s-%s-%s_CondSink.png'%(month,day,year,run),bbox_inches='tight')
