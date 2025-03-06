'''
@author: samuelod
'''

# Import packages
#####################################################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd


# Path to output directory
#####################################################
output_dir = '../outputs'

# Sage image [True/False]
#####################################################
save_png = False
#save_png = True

# 5 character name of run
#####################################################
#identify = 'tmbto'
identify = 'cfrag'

#som_grid = 'BNZSOMG'
#som_grid = 'TOLSOMG'
#som_grid = 'XYLSOMG'
#som_grid = 'ISPSOMG'
som_grid = 'TRPSOMG'

#som_grids = ['All']


db = 1
pwl = 1
vwl = 1
OH = 0.8
fn = 1000.0
HOM = 0
T = 1
RH = 1

# Particle phase diffusivity
#####################################################
#db = [1E-15]

# Parameters
#####################################################
boxvol = 2000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 456
NACT = 578
srtorglast = srtorg1+iorg
nbins = 40
delt = 300.0

# Length of run [hours]
#####################################################
endtime = 144.0

# file name(s)
#####################################################
#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_aemass.dat'%(output_dir,identify,db[0])
file = '%s/20220801_%s_A0.001_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_aemass.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))


print('Running file:',file)
year = 2022
month = 8
day = 1
print('Year = ',year,'Month = ', month,'Day = ', day) 

Time = []
startT = dt.datetime(year, month, day, 11, 0)
print('startT = ',startT)

for i in range(int(endtime*3600/delt)):
  sec = int(i*delt)
  Time.append(startT + dt.timedelta(seconds = sec))
Time = np.array(Time)

#sys.exit('Sucker')

df_spec = pd.read_csv('%s_spec.dat'%(file[:-11]), header=None, delim_whitespace=True)
#saprc_spname = np.array(df_spec.iloc[1,1:1505])
saprc_spname = np.array(df_spec.iloc[1,:])
saprc_cstar = np.array(df_spec.iloc[7,:])
saprc_mwcb = np.array(df_spec.iloc[6,:])
#print(saprc_spname[101:-2])
#sys.exit('you suck')
# ----------------------------------------------------------------------------
df_saprcgc = pd.read_csv('%s_gc.dat'%(file[:-11]),header=None,delim_whitespace=True,)

print('Shape of gas file:',np.shape(df_saprcgc))
saprc_gas = np.array(df_saprcgc)
#sys.exit('give up')
print('shape of final gas array:',np.shape(saprc_gas))
#sys.exit('give up')

# ----------------------------------------------------------------------------

#OC_grid = np.zeros([8,16])

#for i in np.arange(102,len(saprc_gas[0])):
#OC = np.empty([len(saprc_gas[0])-3])
OC = []
gas_list = []

for i in np.arange(1,len(saprc_gas[0])-3):
  if saprc_spname[i][:7] == som_grid:
    gas_list.append(i)
    OC.append(int(saprc_spname[i+102][11:13])/int(saprc_spname[i+102][8:10]))

OC = np.array(OC)
#print(len(OC))
#print(np.max(10.0**saprc_gas[-100,1:-2]/np.max(10.0**saprc_gas[-100,1:-2])))

#print(np.shape(saprc_gas),np.shape(OC))
#sys.exit('you are bad at this')

OC_weighted = np.empty([len(Time)])

for i in range(len(Time)):
  #OC_weighted[i] = np.mean(OC*(10.0**saprc_gas[i,1:-2]/np.max(10.0**saprc_gas[i,1:-2])))
  OC_weighted[i] = np.mean(OC*(saprc_gas[i,gas_list]/np.max(saprc_gas[i,gas_list])))

#OC_grid[Os,Cs] += np.average(saprc_gas[low_indx:up_indx,i],axis=0)
  #print(saprc_spname[i][8:13])

#OC_grid[-1,-1] += np.average(saprc_gas[low_indx:up_indx,-3],axis=0)
#OC_grid = 1e6*1e9*OC_grid/boxvol
#OC_grid = OC_grid/np.amax(OC_grid)
#print('sum of OC_grid=',np.sum(OC_grid))
#sys.exit('give up now')

x = mdates.date2num(Time)

fig, axes = plt.subplots(nrows=1, ncols=1)
fig.set_size_inches(10,4)

axes.plot(x,OC_weighted)

plt.title('Mass Weighted OC')
plt.ylabel('O:C')
plt.xlabel('Time')
#ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
#plt.grid(True)
#fig.colorbar(c1,format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),pad=0.01, shrink=0.6, aspect=14, label='$\mu$g /$m^{3}$')
#fig.colorbar(c1,pad=0.01, shrink=0.6, aspect=14, label='$\mu$g /$m^{3}$')
#c1.set_clim(-8,0)
#c1.set_clim(-2,0)
#plt.yscale('log')
#plt.legend()
#plt.ylim(0.6,0.8)
plt.show()
if save_png==True:
  #fig.savefig('NPF_event5_Gas_OCgrid.png',bbox_inches='tight')
  fig.savefig('NPF5_%s_%s_OCgrid_gas.png'%(file[11:-11],som_grid),bbox_inches='tight')
#except:
#print('Could not reshape (or something else) - moving on')
