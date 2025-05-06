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
endtime = 144.0
delt = 300.0

#----------------------------------------------------------------------------------------------------------

#==========================================================================================================
name = '20220801'
identify = 'multi'
db = 1
pwl = 1
vwl = 1
OH_scale = 0.8
FN_scale = 1000.0
HOM = 0
T_switch = 1
RH_switch = 1
A = 1.0e-3

files = ['%s/20220801_%s_A%s_db%i_pwl%i_vwl%i_OH%s_FN%s_HOM%i_T%i_RH%i_cs.dat'%(output_dir,identify,A,db,pwl,vwl,OH_scale,FN_scale,HOM,T_switch,RH_switch)
  ]
#==========================================================================================================

#time_low = dt.datetime(2022,8,4,7)
#time_up = dt.datetime(2022,8,4,10)

#time_low = dt.datetime(2022,8,4,13)
#time_up = dt.datetime(2022,8,4,16)

time_low = dt.datetime(2022,8,4,19)
time_up = dt.datetime(2022,8,4,22)



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
  
  low_indx = np.where(Time>time_low)[0][0]
  up_indx = np.where(Time<time_up)[0][-1]
  #print('shape Time = ',np.shape(Time)[0])
  #----------------------------------------------------------------------------------------------------------
  cs_array = np.array(pd.read_csv(file,header=None,delim_whitespace=True))
  print('initial shape of array:',np.shape(cs_array))
  cs_array = cs_array[:,1]

  print(np.mean(cs_array[low_indx:up_indx]))
  sys.exit()

  #cs_array = np.reshape(cs_array, (np.shape(Time)[0]-1,2))
  #print('reshaped cs_array:',np.shape(cs_array))
  
  fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)
  fig = plt.gcf()
  fig.set_size_inches(10,4)

  x = mdates.date2num(Time[1:])
  #plt.plot(x,1/cs_array/3600.)
  plt.plot(x,cs_array)
  plt.scatter(x[low_indx], np.mean(cs_array[low_indx:up_indx]))
  plt.scatter(x[up_indx], np.mean(cs_array[low_indx:up_indx]))

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
