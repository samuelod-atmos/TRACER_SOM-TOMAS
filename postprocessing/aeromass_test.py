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
from PBL_script import pbl
import sys
#import pygsheets as pyg

#===========================================================================================================

output_dir = '../outputs'
save_png = False 
#save_png = True

#===========================================================================================================

name = '20220801'
#==========================================================================================================

#rname = '%s/20220808_vwl0_pwl1_hr1.00e+01_no_particle_flow_bg10_noconc.dat'%output_dir
#rname = '%s/20220801_vwl1_pwl1_hr7.20e+01_NoO3_bg10_noconc.dat'%output_dir
#rname = '%s/20220801_vwl0_pwl1_hr7.20e+01_A7.2e-4_bg10_noconc.dat'%output_dir
rname = '%s/20220731_vwl0_pwl1_hr7.20e+01_A7.2e-3_bg10_noconc.dat'%output_dir
df_no = np.array(pd.read_csv(rname,header=None, delim_whitespace=True))
print('shape of df_no=',np.shape(df_no))
ibins = 40
#endtime = 10.0
delt = 10.0

number_conc = df_no[:,1:]

Time = []
#for i in range(int(endtime[0]*3600/delt+1)):
for i in range(len(df_no)):
  sec = int(i*delt)
  Time.append(sec)
Time = np.array(Time)

year = int(rname[11:15])
month = int(rname[15:17])
day = int(rname[17:19])
startT = dt.datetime(year,month,day,2)
print(startT)

date = []
date.append(startT)

for i in range(len(Time)-1):
  #print(Time[i+1])
  startT = startT + dt.timedelta(seconds=10)
  date.append(startT)
#print(len(date))
date = np.array(date)
#print(len(date))

#sys.exit()

   #=============================================================================

#SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
#low_bin, up_bin, upperbin,lowerbin = 0, 85, 10, 0
#low_bin, up_bin, upperbin,lowerbin = 0, 85, 10, 4
#model_counter,smps_counter = 8,100 
#nuc = True

####################################################################

Bins = np.array([1.2350826156568765E-002,
1.5561065965403546E-002,
1.9605714703615617E-002,
2.4701652823409345E-002,
3.1122132573709296E-002,
3.9211430217237254E-002,
4.9403306667362333E-002,
6.2244266433223019E-002,
7.8422862054486592E-002,
9.8806615375812007E-002,
.12448853543805495,
.15684572734899740,
.19761323483379878,
.24897707601932786,
.31369146117804336,
.39522647783194720,
.49795416232509176,
.62738293531618428,
.79045297199259412,
.99590834522305627,
1.2547658965525639,
1.5809059766425884,
1.9918167315918585,
2.5095318449455197,
3.1618120185999783,
3.9836335454752101,
5.0190637935718252,
6.3236241678295615,
7.9672672555334119,
10.038127794505227,
12.647248596918340,
15.934534840232814,
20.076256003733615,
25.294497716355124,
31.869070338797616,
40.152512836913573,
50.588996477747159,
63.738141994259244,
80.305027332719860,
101.17799504556817])

BinEdge = np.array([1.1003335152977913E-002,
1.3863333673745220E-002,
1.7466706037540244E-002,
2.2006670760556325E-002,
2.7726667920251188E-002,
3.4933412796713817E-002,
4.4013342430313677E-002,
5.5453336986023886E-002,
6.9866827036694307E-002,
8.8026686679029437E-002,
0.11090667626309085,
0.13973365695992204,
0.17605337699486312,
0.22181335710826797,
0.27946731969291105,
0.35210676126333484,
0.44362672338070858,
0.55893465093195627,
0.70421353707388734,
0.88725346508976299,
1.1178693249561813,
1.4084271032422104,
1.7745069668362181,
2.2357386960969010,
2.8168542646732937,
3.5490140069858223,
4.4714774845628806,
5.6337086457243348,
7.0980281605984192,
8.9429551538639238,
11.267417524204170,
14.196056614450397,
17.885910677204180,
22.534835513919351,
28.392113815407917,
35.771822093361038,
45.069671958860738,
56.784228803830111,
71.543645664627462,
90.139345779765591,
113.56845995368882])

BinEdge = BinEdge*100
BinsE = np.log10(BinEdge[1:]/BinEdge[:-1])
Bins = Bins*100

#-------------------------------------------------------------
mass_ts = np.zeros(len(Time))
for i in range(len(Time)):
  temp = np.zeros(len(Bins))
  for j in range(len(Bins)):
    temp[j] = np.pi/6*(Bins[j]*1e-9)**3*1770.0*number_conc[i,j]*1e6*1e9
  mass_ts[i] = sum(temp)

#-------------------------------------------------------------
plt.rcParams.update({'font.size': 18})
fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)

x = mdates.date2num(date)

axes.plot(x,mass_ts)

fig.set_size_inches(14,5)
axes.grid(True)
#axes.set_title('No_bg1 = %s, scale = %s'%(No_bg1,scale)) 
axes.set_ylabel('Mass (ug/m^3)')
axes.set_xlabel('Time')
axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
#axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axes.set_yscale('log')
axes.locator_params(axis='x',nbins=3)
plt.subplots_adjust(hspace=0.02)

axes.locator_params(axis='x', nbins=6)
#axes.set_xlim(12,600)
#axes.set_ylim(1.4,1000)

plt.show()
if save_png==True:
  fig.savefig('PWL1_constOH_SizeDist.png',bbox_inches='tight')
