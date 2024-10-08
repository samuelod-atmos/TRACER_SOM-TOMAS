import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd
import sys
import matplotlib
from scipy import signal


def smoothdist(dist):
  sdist=np.empty(dist.shape)
  sdist[0]=dist[0]*0.75 + dist[1]*0.25
  sdist[1:-1]=dist[:-2]*0.25 + dist[1:-1]*0.5 + dist[2:]*0.25
  sdist[-1]=dist[-2]*0.25 + dist[-1]*0.75
  return sdist

#-----------------------------------------------------------
oh_fid = open('timeseries/20220801_splic_o3','r')

OH = []
for line in oh_fid.readlines():
 OH.append(float(line))

OH1 = np.array(OH)

oh_fid = open('timeseries/20220801_debug_o3','r')

OH = []
for line in oh_fid.readlines():
 OH.append(float(line))
#OH = smoothdist(OH)

OH2 = np.array(OH)


oh_fid = open('timeseries/20220801_DP_O3_o3','r')

OH = []
for line in oh_fid.readlines():
 OH.append(float(line))
#OH = smoothdist(OH)

OH3 = np.array(OH)


ax = plt.gca()
fig = plt.gcf()
fig.set_size_inches(10,3)

#matplotlib.axes.Axes.ticklabel_format(axis=['y'],style='sci')
plt.ticklabel_format(axis='y',style='sci')

x = np.linspace(0,len(OH),len(OH))/360.
plt.plot(x,OH2,label='AOS')
plt.plot(x,OH1,label='MAQL2')
plt.plot(x,OH3,label='Deer Park')
plt.xlabel('Hour of simulation')
plt.ylabel('Ozone [ppb]')
plt.title('Ozone Comparison') 
plt.legend(loc=1)
plt.ylim(0,)
plt.show()
