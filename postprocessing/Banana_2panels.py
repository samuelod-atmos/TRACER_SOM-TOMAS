from pylab import * 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.patches as patches
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
#save_png = False 
save_png = True

#===========================================================================================================

#identify = 'vwl_0'
#identify = 'kvpon'
#identify = '1.5OH'
#identify = 'HiNOx'
#identify = 'A8e-3'
#identify = 'dbk_0'
#identify = 'v2pwl'
#identify = 'smtOH'
#identify = '0_tmb'
#identify = 'kvpon'
#identify = 'HOM.3'
#identify = 'nan_0'
#identify = 'inx10'
identify = 'A5e-4'
#identify = 'styon'
#identify = 'tmbto'
#identify = 'HOMmx'
#identify = 'Fkpar'
#identify = 'smtOH'
#identify = 'injec'
#identify = 'splic'
#identify = 'multi'
#identify = 'noinj'
#identify = 'wiMDL'
#identify = 'NPF_5'
#identify = 'sclOH'
#identify = 'GC_OH'
#identify = 'sclfn'
#identify = 'DP2O3'
#identify = 'sommx'
#identify = 'noHOM'
#identify = 'kp2.5'
#identify = 'y_mix'
#identify = '1.8kp'
#identify = '10xkp'
#identify = '300KT'
#identify = 'kflat'
#identify = 'multi'
#identify = 'bigDp'
#identify = 'frag2'
#identify = 'frag4'
#identify = 'prfct'
#identify = 'debug'
#==========================================================================================================

endtime = 144.0
#endtime = 23.0

#rname = '%s/20220808_vwl0_pwl1_hr1.00e+01_no_particle_flow_bg10_noconc.dat'%output_dir
#rname = '%s/20220801_vwl0_pwl0_hr7.20e+01_Pfunc_bg10_noconc.dat'%output_dir
#rname = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_bg10_noconc.dat'%(output_dir,identify)
#rname = '%s/20220801_%s_vwl1_pwl1_hr%4.2e_nh35000_orgfn1_inorg1_db1e-14_noconc.dat'%(output_dir,identify,endtime)
rname = '%s/20220801_%s_A0.0005_db1_pwl1_vwl1_OH0.8_FN1000.0_HOM0_T1_RH1_noconc.dat'%(output_dir,identify)
#rname = '%s/20220801_multi_vwl0_pwl0_nh35000.0_orgfn1_inorg1_db1e-15_ohscale1.0_noconc.dat'%output_dir
#rname = '../outputs/20220801_multi_vwl1_pwl1_nh35000.0_orgfn1_inorg1_db1e-15_ohscale1.0_noconc.dat'


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

BinEdge = BinEdge*100
BinsE = np.log10(BinEdge[1:]/BinEdge[:-1])

Bins = Bins*100
n=3;m=3
Y = (number_conc[:,:])/BinsE[:]

plt.rcParams.update({'font.size': 11})

fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)

#x = mdates.date2num(date-dt.timedelta(hours=6))
x = mdates.date2num(date)
c1 = axes.pcolormesh(x,Bins[:],np.log10(np.transpose(Y)),cmap='rainbow')

#nuc = False
nuc = False
if nuc==True:
  
  smps_gr, model_gr, model_indx, smps_indx = [],[],[],[]
  stat,model_x = 0,[]
  for i in np.arange(0,len(x1),20):
    if Time[i] >= model_low and Time[i] <= model_up:
      model_x.append(i)
      if stat == 0:
        indx = np.where(Y[i,:]==np.nanmax(Y[i,lowerbin:upperbin]))[0][0]
        model_indx.append(indx)
      if stat != 0:
        if model_indx[-1] <=2:
          indx = np.where(Y[i,:]==np.nanmax(Y[i,model_indx[-1]:model_indx[-1]+5]))[0][0]
        else:
          indx = np.where(Y[i,:]==np.nanmax(Y[i,model_indx[-1]-3:model_indx[-1]+3]))[0][0]
        model_indx.append(indx)
        b2 = Bins[indx]
        model_gr.append((b2-b1)/(Time[i]-t1).total_seconds()*3600.0)
        if b2==b1:
          model_gr[-1] = 0.0
      stat = 1
      b1 = Bins[indx]
      t1 = Time[i]
  stat,smps_x = 0,[]
  for i in np.arange(0,len(x2),1):
    if smps_date[i] >= smps_low and smps_date[i] <= smps_up:
      smps_x.append(i)
      if stat == 0:
        indx = np.where(smps_sd[:,i]==np.nanmax(smps_sd[low_bin:up_bin,i]))[0][0]
        smps_indx.append(indx)
      if stat != 0:
        #indx = np.where(smps_sd[:,i]==np.nanmax(smps_sd[smps_indx[-1]-search_range:smps_indx[-1]+search_range,i]))[0][0]
        indx = np.where(smps_sd[:,i]==np.nanmax(smps_sd[:,i]))[0][0]
        smps_indx.append(indx)
        b2 = smps_bins[indx]
        smps_gr.append((b2-b1)/(smps_date[i]-t1).total_seconds()*3600.0)
        if b2==b1:
          smps_gr[-1] = 0.0
      stat = 1
      b1 = smps_bins[indx]
      t1 = smps_date[i]
  
  print('=======================================================')
  print('Model # =',np.nansum(Y[model_x[-1]]*np.log10(BinEdge[1:]/BinEdge[:-1])),'#/cm')
  print('SMPS # =',np.nansum(smps_sd[1:,smps_x[-1]]*np.log10(smps_bins[1:]/smps_bins[:-1])),'#/cm')

  smps_gr,model_gr,smps_x,model_x = np.array(smps_gr),np.array(model_gr),np.array(smps_x),np.array(model_x)

  print('Model Growth Rate =',np.nanmean(model_gr))
  print('Obs. Growth Rate =',np.nanmean(smps_gr))
  print('SMPS Dp =',np.nanmax(smps_bins[smps_indx]))
  print('Model Dp =',np.nanmax(Bins[model_indx]))
  print('=======================================================')

  axes[0].scatter(x1[model_x],Bins[model_indx],c='k',marker='x')
  axes[0].hlines(np.nanmax(smps_bins[smps_indx]),xmin=x1[0],xmax=x1[-1],linestyle=':',linewidth=1.5,label='SMPS - Dp=%5.2f [nm]'%np.nanmax(smps_bins[smps_indx]))
  axes[0].hlines(np.nanmax(Bins[model_indx]),xmin=x1[0],xmax=x1[-1],linestyle='--',linewidth=1,label='Model - Dp=%5.2f [nm]'%np.nanmax(Bins[model_indx]))
  #axes[1].annotate('GR =%6.2f [nm/hr]'%np.nanmean(smps_gr),xy=(x2[0], 100) , xytext=(x1[20], 200))
  
  axes[0].set_xlim(x1[0],x1[model_x[-1]+200])  
  smps_gr, model_gr, model_indx, smps_indx = [],[],[],[] 


fig.set_size_inches(12,5)
axes.grid(True)
#axes.set_title('Model') 
axes.set_ylabel('Dp (nm)',fontsize=22)
axes.set_xlabel('Date',fontsize=22)

#if len(x) < 300:
#  axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#  #axes.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0,60]))
#  axes.xaxis.set_major_locator(mdates.HourLocator(interval = 3))
#else:
#  axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

axes.set_yscale('log')
#axes.locator_params(axis='x',nbins=3)
plt.subplots_adjust(hspace=0.02)

#axes.locator_params(axis='x', nbins=6)
axes.set_ylim(12,100)
#axes.set_ylim(1.2,600)

#--------------------------------------------------------
#time_low = dt.datetime(2022,8,2,9,45)
#time_up = dt.datetime(2022,8,2,14,15)

#time_low = dt.datetime(2022,8,3,10,15)
#time_up = dt.datetime(2022,8,3,14,30)

#time_low = dt.datetime(2022,8,4,10)
#time_up = dt.datetime(2022,8,4,15,30)

#time_low = dt.datetime(2022,8,5,10)
#time_up = dt.datetime(2022,8,5,15)

#time_low = dt.datetime(2022,8,6,10,45)
#time_up = dt.datetime(2022,8,6,16)

#time_low = dt.datetime(2022,8,6,5)
#time_up = dt.datetime(2022,8,6,19)

time_low = dt.datetime(2022,8,4,0)
time_up = dt.datetime(2022,8,7,0)

axes.set_xlim(mdates.date2num(time_low),mdates.date2num(time_up))
#axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#axes.xaxis.set_major_locator(mdates.HourLocator(interval = 3))

axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
axes.xaxis.set_major_locator(mdates.DayLocator(interval = 1))
axes.tick_params(axis='x', which='major', labelsize=16)
axes.tick_params(axis='x', which='minor', labelsize=10)

#--------------------------------------------------------
#box_time = dt.datetime(2022,8,6,21)
#rect = patches.Rectangle((mdates.date2num(box_time), 12), 1/24, 88, linewidth=5, edgecolor='k', facecolor='none')

# Add the patch to the Axes
#axes.add_patch(rect)

#--------------------------------------------------------
#cb1 = fig.colorbar(c1, format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),ax=axes,pad=0.0061, label='$ dN/dlog_{10}(D_p) $')
#cb1 = fig.colorbar(c1, format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),ax=axes,pad=0.0061, label='$ dN/dlog_{10}(D_p) $')
c1.set_clim(1,4.3)

plt.show()
if save_png==True:
  fig.savefig('%sSizeDist.png'%rname[11:-10],bbox_inches='tight')
  #fig.savefig('%s_A2e-4_SizeDist.png'%identify,bbox_inches='tight')
  #fig.savefig('August_6th_SizeDist_hour%s.png'%(str(box_time.hour).zfill(2) ),bbox_inches='tight')
