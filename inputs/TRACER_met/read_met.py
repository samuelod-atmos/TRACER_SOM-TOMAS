import numpy as np
import datetime as dt
import sys
from netCDF4 import Dataset 
from matplotlib import pyplot as plt


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
startD = dt.datetime(2022,7,31,0)
endD = dt.datetime(2022,8,31,0)
days = int((endD-startD).total_seconds()/3600/24)
#print('number of days =',days)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
date = startD
aadt = 10
interp_s = np.arange(0,24*3600,aadt)

temp_date = []
temp_date.append(startD)

for i in np.arange(1,len(interp_s),1):
  #print('interp_s[i]=',interp_s[i])
  temp_date.append(startD+dt.timedelta(seconds=int(interp_s[i])))
temp_date = np.array(temp_date) - dt.timedelta(hours=6)

#-------------------------------
f1 = open('Interp_dataset.txt','w')
#-------------------------------

total_T = []

for i in range(days):
  print('running:',date)

  ohfid = Dataset('houmetM1.b1.%s%s%s.000000.cdf'%(str(date.year),str(date.month).zfill(2),str(date.day).zfill(2)),'r')
  time = np.array(ohfid.variables['time'])
  time_offset = np.array(ohfid.variables['time_offset'])
  temp_mean = np.array(ohfid.variables['temp_mean'])
  rh_mean = np.array(ohfid.variables['rh_mean'])
  
  temp = np.interp(interp_s,time,temp_mean)
  RH = np.interp(interp_s,time,rh_mean)
  #total_T.append(temp)
  #for j in range(len(interp_s)):
  #  temp_date = date + dt.timedelta(seconds=interp_s)
  for j in range(len(interp_s)):
    f1.write('%s, %s, %s \n'%(str(temp_date[j]),str(temp[j]+273.15),str(RH[j])))
  
  date = date + dt.timedelta(days=1)
  temp_date = temp_date + dt.timedelta(days=1)

f1.close()
#total_T = np.array(total_T)
#print(np.shape(total_T))
#total_T = np.reshape(total_T, 31*8640)
#print(np.shape(total_T))

#plt.plot(np.linspace(0,len(total_T),len(total_T)),total_T,label='Temperature')
#plt.plot(time,rh_mean,label='rh_mean')
#plt.plot(time,short_direct_normal,label='short_direct_normal')
#plt.legend()
#plt.show()

