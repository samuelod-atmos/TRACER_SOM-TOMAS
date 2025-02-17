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


#------------------------------------------------------------
def smoothdist(dist):
  sdist=np.empty(dist.shape)
  sdist[0]=dist[0]*0.75 + dist[1]*0.25
  sdist[1:-1]=dist[:-2]*0.25 + dist[1:-1]*0.5 + dist[2:]*0.25
  sdist[-1]=dist[-2]*0.25 + dist[-1]*0.75
  return sdist
#------------------------------------------------------------

####################################################
oh_fid = open('timeseries/20220801_sclOH_OH','r')

OH = []
for line in oh_fid.readlines():
 OH.append(float(line))

OH = np.array(OH)
print(len(OH[::30]))
oh_fid.close()

####################################################

oh_fid2 = open('timeseries/20220801_GC_OH_OH','r')

OH2 = []
for line in oh_fid2.readlines():
 OH2.append(float(line))

OH2 = np.array(OH2)
print(len(OH2))
oh_fid2.close()

####################################################

oh_fid3 = open('timeseries/20220801_smtOH_OH','r')

OH3 = []
for line in oh_fid3.readlines():
 OH3.append(float(line))

OH3 = np.array(OH3)
print(len(OH3))
oh_fid3.close()

#=====================================================================
ax = plt.gca()
fig = plt.gcf()
fig.set_size_inches(10,3)

#matplotlib.axes.Axes.ticklabel_format(axis=['y'],style='sci')
plt.ticklabel_format(axis='y',style='sci')

x = np.linspace(0,len(OH),len(OH))/360.
plt.plot(x,OH,label='Radiation')
plt.plot(x,OH3,label='Smoothed radiation')
plt.plot(x,OH2,label='GEOS-Chem')
plt.xlabel('Time [hours]')
plt.ylabel('OH [molec/cm^3]')
plt.title('OH') 
plt.legend()
plt.show()
