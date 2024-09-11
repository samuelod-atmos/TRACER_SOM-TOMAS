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

oh_fid = open('20220801_base?_Temp','r')

OH = []
for line in oh_fid.readlines():
 OH.append(float(line))

OH = np.array(OH)
OH = signal.savgol_filter(OH,101,2)
#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)
#OH = smoothdist(OH)

ax = plt.gca()
fig = plt.gcf()
fig.set_size_inches(10,3)

#matplotlib.axes.Axes.ticklabel_format(axis=['y'],style='sci')
plt.ticklabel_format(axis='y',style='sci')

x = np.linspace(0,len(OH),len(OH))/360.
plt.plot(x,OH)
plt.xlabel('Time [hours]')
plt.ylabel('Temperature [K]')
plt.title('Tempature') 
plt.show()
