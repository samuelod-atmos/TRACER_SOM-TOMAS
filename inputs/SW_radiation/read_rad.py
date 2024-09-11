import numpy as np
import datetime as dt
import sys
from netCDF4 import Dataset 
from matplotlib import pyplot as plt
from scipy.signal import savgol_filter

################################### Smoothing function ##################################################
def smoothdist(dist):
  sdist=np.empty(dist.shape)
  sdist[0]=dist[0]*0.75 + dist[1]*0.25
  sdist[1:-1]=dist[:-2]*0.25 + dist[1:-1]*0.5 + dist[2:]*0.25
  sdist[-1]=dist[-2]*0.25 + dist[-1]*0.75
  return sdist
#########################################################################################################

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#startD = dt.datetime(2022,7,20,0)
#endD = dt.datetime(2022,8,31,0)
startD = dt.datetime(2022,8,1,0)
endD = dt.datetime(2022,8,10,0)
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
f1 = open('Interp_radiation.txt','w')
#-------------------------------

total_T = []

for i in range(days):
  print('running:',date)

  ohfid = Dataset('houskyrad60sM1.b1.%s%s%s.000000.cdf'%(str(date.year),str(date.month).zfill(2),str(date.day).zfill(2)),'r')
  time = np.array(ohfid.variables['time'])
  time_offset = np.array(ohfid.variables['time_offset'])
  
  down_short_hemisp = np.array(ohfid.variables['down_short_hemisp'])

  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  down_short_hemisp = smoothdist(down_short_hemisp)
  
  down_short_hemisp = savgol_filter(down_short_hemisp, 601, 2)


  #interp_time = np.linspace(time[0],time[-1],length)
  sw_rad = np.interp(interp_s,time,down_short_hemisp)
  
  total_T.append(sw_rad)
  #for j in range(len(interp_s)):
  #  temp_date = date + dt.timedelta(seconds=interp_s)
  for j in range(len(interp_s)):
    f1.write('%s, %s \n'%(str(temp_date[j]),str(sw_rad[j])))
  
  date = date + dt.timedelta(days=1)
  temp_date = temp_date + dt.timedelta(days=1)

f1.close()
total_T = np.array(total_T)
shape1 = np.shape(total_T[0])[0]
shape2 = np.shape(total_T[:,0])
print(int(np.shape(total_T[0])[0]*np.shape(total_T[:,0])[0]))
#sys.exit()
total_T = np.reshape(total_T, int(np.shape(total_T[0])[0]*np.shape(total_T[:,0])[0]))
print(np.shape(total_T))

plt.plot(np.linspace(0,len(total_T),len(total_T)),total_T,label='OH')
#plt.plot(time,rh_mean,label='rh_mean')
#plt.plot(time,short_direct_normal,label='short_direct_normal')
#plt.legend()
plt.show()

