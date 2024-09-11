import numpy as np
import datetime as dt
from functions import closest, smoothdist
import sys
from netCDF4 import Dataset 
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter

#############################################################################################

NOx = 5.0               # NOx concentration for OH proxy #3

ohfid = Dataset('../inputs/SW_radiation/houskyrad60sM1.b1.20220802.000000.cdf','r')

#for i in ohfid.variables:
  #print(i,ohfid.variables[i].shape)
  #print(i,ohfid.variables[i].units,ohfid.variables[i].shape)


time = np.array(ohfid.variables['time'])

time_offset = np.array(ohfid.variables['time_offset'])
short_direct_normal = np.array(ohfid.variables['short_direct_normal'])
sw_rad = np.array(ohfid.variables['down_short_hemisp'])
 
for i in range(len(sw_rad)): 
  if sw_rad[i]<0.001:
    sw_rad[i] = 0.001

X = np.log10(NOx) - 0.195
Y = sw_rad/(1370*0.76)

P1 = -0.014*X**6 + 0.0027*X**5 + 0.1713*X**4 - 0.0466*X**3 - 0.7893*X**2 - 0.1739*X + 6.9414
P2 = (-1345*Y**3 + 4002*Y**2 - 471.8*Y + 42.72)*10**4

writer = 0.82*10**(P1*np.log10(P2)/6.8)


writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)
writer = smoothdist(writer)

t = savgol_filter(writer, 601, 2)


plt.plot(time/3600.,writer,label='OH')
plt.plot(time/3600.,t,label='Fit')
plt.xlabel('Time [hours]')
plt.ylabel('OH [molec/cm^3]')

plt.legend()
plt.show()

