from pylab import * 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 
#from BG_sizedist import SD_smps
from matplotlib.gridspec import GridSpec
from functions import h,closest
from scipy.optimize import curve_fit
import sys
#import pygsheets as pyg

# where are the outputs?
#===========================================================================================================
output_dir = '../outputs'

# Save a png file? 
#===========================================================================================================
save_png = False 
#save_png = True

# Some other inputs
#===========================================================================================================
identify = 'debug'  # identifier string 
nbins = 40          # number of size bins
delt = 300.0         # time step
#==========================================================================================================

# name of number concentration file - Enli will need to change this
rname = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db1e-15_noconc.dat'%(output_dir,identify)


df_no = np.array(pd.read_csv(rname,header=None, delim_whitespace=True))
print('shape of df_no=',np.shape(df_no))

number_conc = df_no[:,1:]

Time = []
for i in range(len(df_no)):
  sec = int(i*delt)
  Time.append(sec)
Time = np.array(Time)

year = int(rname[11:15])
month = int(rname[15:17])
day = int(rname[17:19])
startT = dt.datetime(year,month,day,11) # Enli will need to change the start time

print('Simulation start time:',startT)

date = []
date.append(startT)

for i in range(len(Time)-1):
  startT = startT + dt.timedelta(seconds=delt)
  date.append(startT)
date = np.array(date)

# Define bins
#===========================================================================================================
xk = np.zeros(nbins+1)  # particle mass cutoffs [kg]...15 bins makes 16 bin *edges*
if nbins==40:
 xk[0]=1E-21*2**-10  # avg mass per particle in lowest bin edge
 for k in range(1,nbins+1):
    xk[k] = xk[k-1]*2.
elif nbins==15:
 xk[0]=1E-21*2**-6  # avg mass per particle in lowest bin edge
 for k in range(1,nbins+1):
    if k < nbins-1:
        xk[k] = xk[k-1]*4.
    else:
        xk[k] = xk[k-1]*32.


pdens=1400. # fixed density for simplicity
xkm=np.sqrt(xk[:-1]*xk[1:])
Bins=(6.*xkm/pdens/np.pi)**(1.0/3.0)*1e9          # [nm] average particle diameter of bin
print(Bins[7:9])
#sys.exit()

Dp_lower= 1e9*(6.*xk[:-1]/pdens/np.pi)**(1.0/3.0)          # [nm] average particle diameter of bin
Dp_upper= 1e9*(6.*xk[1:]/pdens/np.pi)**(1.0/3.0)          # [nm] average particle diameter of bin


#===========================================================================================================
#Y = (number_conc[:,:])/BinsE[:]
Y = (number_conc[:,:])/np.log10(Dp_upper/Dp_lower)

plt.rcParams.update({'font.size': 18})

fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)
fig.set_size_inches(15,2)

x = mdates.date2num(date)
c1 = axes.pcolormesh(x,Bins[:],np.log10(np.transpose(Y)),cmap='rainbow')

axes.grid(True)
axes.set_title('Model') 
axes.set_ylabel('Dp (nm)',fontsize=22)
axes.set_xlabel('Date',fontsize=22)
#axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axes.set_yscale('log')
axes.set_ylim(12,600)

plt.subplots_adjust(hspace=0.02)

cb1 = fig.colorbar(c1, format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),ax=axes,pad=0.0061, label='$ dN/dlog_{10}(D_p) $')
c1.set_clim(1,4.3)

#===========================================================================================================
plt.show()
if save_png==True:
  fig.savefig('%s_A2e-4_SizeDist.png'%identify,bbox_inches='tight')
#===========================================================================================================
#===========================================================================================================
