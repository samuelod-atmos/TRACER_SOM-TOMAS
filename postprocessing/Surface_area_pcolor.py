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

#===========================================================================================================

output_dir = '../outputs'
save_png = False 
#save_png = True

#===========================================================================================================
identify = 'y_mix'
#==========================================================================================================

endtime = 144.0

rname = '%s/20220801_%s_db1_pwl1_vwl1_OH1.0_FN100.0_HOM0_T1_RH1_noconc.dat'%(output_dir,identify)

#==========================================================================================================

df_no = np.array(pd.read_csv(rname,header=None, delim_whitespace=True))
print('shape of df_no=',np.shape(df_no))
ibins = 40
#endtime = 10.0
delt = 300.0

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
startT = dt.datetime(year,month,day,11)
print(startT)

date = []
date.append(startT)

for i in range(len(Time)-1):
  #print(Time[i+1])
  startT = startT + dt.timedelta(seconds=delt)
  date.append(startT)
#print(len(date))
date = np.array(date)


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

#==========================================================================================================
BinEdge = BinEdge*100
BinsE = np.log10(BinEdge[1:]/BinEdge[:-1])

Bins = Bins*100
#Y = (number_conc[:,:])/BinsE[:]


xk = np.zeros(ibins+1) 
xk[0]=1E-21*2**-10 
for k in range(1,ibins+1):
   xk[k] = xk[k-1]*2.
pdens=1400. # fixed density for simplicity
xkm=np.sqrt(xk[:-1]*xk[1:])
Dp=((6.*xkm/pdens/np.pi)**(1.0/3.0)) # [m] average particle diameter of bin

Surf = number_conc*np.pi/6.0*Dp**3
#Surf = np.sum(Surf[:,10:],axis=1)

plt.rcParams.update({'font.size': 11})

fig, axes = plt.subplots(nrows=2, ncols=1,sharex=True)

#x = mdates.date2num(date-dt.timedelta(hours=6))
x = mdates.date2num(date)
c1 = axes[0].pcolormesh(x,Bins[:],np.log10(np.transpose(Surf)),cmap='rainbow')


#==========================================================================================================
#==========================================================================================================

cage_dir = 'CAGE_SMPS'

low = mdates.date2num(dt.datetime(2022,8,1,11,0))#-dt.timedelta(hours=6))
up = mdates.date2num(dt.datetime(2022,8,7,11,0))#-dt.timedelta(hours=6))


Bins = []
bin_data = '%s/PSD_Dp.txt'%cage_dir
bin_fid = open(bin_data, 'r')
for line in bin_fid.readlines():
  #     spl_line= line.split('  ')
  # for i in range(len(spl_line)):
  #     print('line=',line)
  Bins.append(float(line))
Bins = np.array(Bins)*1e-6

bin_fid.close()


sizedist = []

data = '%s/Chamber_PSD.txt'%cage_dir
fid=open(data, 'r')

for line in fid.readlines():

  #print(line)
  #sys.exit()
  spl_line=line.split(' ')
  spl_line=line.split('\t')
  #print(spl_line[-1])
  #sys.exit()
#         time.append(float(spl_line[0]))
#         count=count+1
  temp=[]
  for i in range(len(Bins)):
    spl_line[i] = (float(spl_line[i]))
#         spl_line[i] = float(spl_line[i])
#             spl_line[i+1] = float(spl_line[i+1])
#             if spl_line[i] == -inf:
#                 spl_line[i] = 'NaN' 
    temp.append(float(spl_line[i]))
  sizedist.append(temp)
sizedist = np.array(sizedist)

Dp_bounds = np.zeros([len(Bins)+1])
Dp_bounds[:-1] = Bins[:]
Dp_bounds[-1] = 418.0

#print(Dp_bounds[:60])
#sys.exit()

totalN = sizedist*(np.log10(Dp_bounds[1:])-np.log10(Dp_bounds[:-1]))
Surf_smps = totalN*np.pi/6.0*Bins**3


time = []
data = '%s/Chamber_PSD_time.txt'%cage_dir
fid=open(data, 'r')
for line in fid.readlines():
  time.append(float(line))
fid.close()


date = []
# date.append(dt.datetime(2022,7,15,11,57))
date.append(dt.datetime(1970,1,1,0)+dt.timedelta(seconds=time[0]))

for i in range(len(time)-1):
  date.append(date[-1] + dt.timedelta(seconds = time[i+1]-time[i]))
    
date = np.array(date)- dt.timedelta(hours=6)
x1 = mdates.date2num(date) #-dt.timedelta(hours=12))



c2 = axes[1].pcolormesh(x1,Bins[:]*1e9,np.log10(np.transpose(Surf_smps)),cmap='rainbow')

#==========================================================================================================
#==========================================================================================================

fig.set_size_inches(10,6)
axes[0].grid(True)
axes[0].set_title('Model') 
axes[0].set_ylabel('Dp (nm)',fontsize=22)
axes[0].set_xlabel('Date',fontsize=22)


axes[1].grid(True)
axes[1].set_title('SMPS') 
axes[1].set_ylabel('Dp (nm)',fontsize=22)
axes[1].set_xlabel('Date',fontsize=22)

if len(x) < 300:
  axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  #axes.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0,60]))
  axes[1].xaxis.set_major_locator(mdates.HourLocator(interval = 3))
else:
  axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

axes[0].set_yscale('log')
axes[1].set_yscale('log')
plt.subplots_adjust(hspace=0.02)

#axes.locator_params(axis='x', nbins=6)
axes[0].set_ylim(12,200)
axes[1].set_ylim(12,200)
axes[1].set_xlim(low,up)
#axes.set_ylim(1.2,600)

#cb1 = fig.colorbar(c1, format=mpl.ticker.FormatStrFormatter('%2.3e'),ax=axes[0],pad=0.0061, label='Surface Area')
#c1.set_clim(1e-25,2e-20)
c1.set_clim(-25,-20)


#cb2 = fig.colorbar(c2, format=mpl.ticker.FormatStrFormatter('%2.3e'),ax=axes[1],pad=0.0061, label='Surface Area')
#c2.set_clim(1e-25,2e-20)
c2.set_clim(-25,-20)

plt.show()
if save_png==True:
  #fig.savefig('%s_full_SizeDist.png'%identify,bbox_inches='tight')
  #fig.savefig('%s_A2e-4_SizeDist.png'%identify,bbox_inches='tight')
  fig.savefig('%s_SizeDist_.png'%rname[11:-11],bbox_inches='tight')
