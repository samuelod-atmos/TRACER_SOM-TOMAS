from pylab import * 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 
from BG_sizedist import SMPS_SD, SD_nanosmps, nonuc_nanosmps
from matplotlib.gridspec import GridSpec
from functions import h,closest
from scipy.optimize import curve_fit
from PBL_script import pbl2
import sys

#===========================================================================================================

output_dir = '../outputs/'

#===========================================================================================================

emiss_scheme = 3
OH_proxy = 2
#run = 'E%s_OH%s_constRH'%(emiss_scheme, OH_proxy)
run = 'E%s_OH%s_simple'%(emiss_scheme, OH_proxy)
cstar = 0.0
#nuc = True
#===========================================================================================================
#run,cstar = 'E2_OH2',1e-5
#run = 'E3_OH2_constRH'
#run = 'E3_OH2_InorgNuc'
#run = 'E3_OH2_OrgNuc'
#run = 'E3_OH2_ParentTest'
#run = 'E3_OH2_NoMix'
#===========================================================================================================
#save_png = False
save_png = True
#==========================================================================================================
files = [
  '%s04272016_%s_Cstar%s_T287.62_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run,cstar),
  '%s04282016_%s_Cstar%s_T285.89_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run,cstar),
  '%s05112016_%s_Cstar%s_T293.72_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run,cstar),
  '%s05142016_%s_Cstar%s_T282.61_NH32.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run,cstar),
  '%s05162016_%s_Cstar%s_T288.81_NH33.00e+02_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run,cstar),
  '%s05192016_%s_Cstar%s_T287.26_NH33.00e+02_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run,cstar)]
#==========================================================================================================


for file in files:
  df_no = np.array(pd.read_csv(file,header=None, delim_whitespace=True))
  print('shape of df_no=',np.shape(df_no))
  layer = 1
  #nlayers = int(file[-42:-40])
  nlayers = 20
  ibins = 40
  upper_pres = 70000
  endtime = 10.0
  delt = 10.0
  year = int(file[15:19])
  month = int(file[11:13])
  day = int(file[13:15])
  print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  number_conc = df_no[:,1:]
  
  Time = []
#=============================================================================

  if month == 4 and day == 27:
    SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
    startT = dt.datetime(year, month, day, 9, 20)
    low_bin, up_bin, upperbin,lowerbin = 0, 85, 10, 0
    smps_low = dt.datetime(year, month, day, 10, 0)
    smps_up = dt.datetime(year, month, day, 17, 0)
    model_low = dt.datetime(year, month, day, 10, 0)
    model_up = dt.datetime(year, month, day, 17, 0)
    model_counter,smps_counter = 8,100 
    if run == 'E3_OH3' or run == 'E4_OH3':
      delt = 10.0
    if run == 'E4_OH3':
      delt = 5.0
    nuc = True
  elif month == 4 and day == 28:
    SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
    startT = dt.datetime(year, month, day, 8, 0)
    low_bin, up_bin, upperbin,lowerbin = 0, 85, 12, 0
    smps_low = dt.datetime(year, month, day, 9, 15)
    smps_up = dt.datetime(year, month, day, 17, 0)
    model_low = dt.datetime(year, month, day, 9, 15)
    model_up = dt.datetime(year, month, day, 17, 0)
    model_counter,smps_counter = 8,100
    if run == 'E2_OH3' or run == 'E4_OH3' or run == 'E3_OH2_withHOM_ConstPar':
      delt = 10.0
    if run == 'E4_OH2':
      delt = 5.0
    nuc = True
  elif month == 5 and day == 11:
    SMPS_sheetname = 'HiScaleSMPSb_SGP_20160511_R0' 
    startT = dt.datetime(year, month, day, 12, 0)
    low_bin, up_bin, upperbin,lowerbin = 0, 85, 5, 0
    smps_low = dt.datetime(year, month, day, 13, 0)
    smps_up = dt.datetime(year, month, day, 19, 0)
    model_low = dt.datetime(year, month, day, 12, 40)
    model_up = dt.datetime(year, month, day, 19, 0)
    model_counter,smps_counter = 8,100 
    nuc = True
  elif month == 5 and day == 14:
    startT = dt.datetime(year, month, day, 9, 50)
    low_bin, up_bin, upperbin,lowerbin = 0, 85, 12, 0
    smps_low = dt.datetime(year, month, day, 11, 0)
    smps_up = smps_low + dt.timedelta(hours=7)
    model_low = dt.datetime(year, month, day, 11, 0)
    model_up = model_low + dt.timedelta(hours=7)
    model_counter,smps_counter = 8,100 
    #delt = 10.0
    if run == 'E4_OH3':
      delt = 10.0
    nuc = True
  elif month == 9 and day == 11:
    SMPS_sheetname = 'HiScaleSMPSb_SGP_20160827_R1'
    startT = dt.datetime(year, month, day, 10, 0)
    low_bin, up_bin, upperbin,lowerbin = 0, 11, 14, 12
    smps_low = dt.datetime(year, month, day, 11, 45)
    smps_up = dt.datetime(year, month, day, 15, 40)
    model_low = dt.datetime(year, month, day, 11, 45)
    model_up = dt.datetime(year, month, day, 15, 40)
    model_counter,smps_counter = 14,5
  elif month == 9 and day == 17:
    SMPS_sheetname = 'HiScaleSMPSb_SGP_20160827_R1'
    startT = dt.datetime(year, month, day, 9, 0)
    low_bin, up_bin, upperbin,lowerbin = 0, 11, 14, 12
    smps_low = dt.datetime(year, month, day, 10, 15)
    smps_up = smps_low + dt.timedelta(hours=6)
    model_low = dt.datetime(year, month, day, 11, 15)
    model_up = model_low + dt.timedelta(hours=6)
    model_counter,smps_counter = 14,5
  elif month == 5 and day == 16:
    #SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
    startT = dt.datetime(year, month, day, 9, 0)
    low_bin, up_bin, upperbin,lowerbin = 0, 85, 12, 5
    smps_low = dt.datetime(year, month, day, 9, 0)
    smps_up = smps_low + dt.timedelta(hours=7)
    model_low = dt.datetime(year, month, day, 9, 0)
    model_up = model_low + dt.timedelta(hours=7)
    model_counter,smps_counter = 8,100
    delt = 10.0
    nuc = False
  elif month == 5 and day == 19:
    #SMPS_sheetname = 'HiScaleSMPSb_SGP_20160511_R0' 
    startT = dt.datetime(year, month, day, 9, 0)
    low_bin, up_bin, upperbin,lowerbin = 0, 85, 12, 5
    smps_low = dt.datetime(year, month, day, 13, 0)
    smps_up = smps_low + dt.timedelta(hours=5)
    model_low = dt.datetime(year, month, day, 13, 0)
    model_up = model_low + dt.timedelta(hours=5)
    model_counter,smps_counter = 8,100 
    delt = 10.0
    nuc = False

  print('startT = ',startT)
  
  for i in range(int(endtime*3600/delt+1)):
    sec = int(i*delt)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
  
  reshape_var = np.shape(number_conc)[0]/nlayers
  reshape_var = int(np.shape(number_conc)[0]/nlayers)
  print('shape of number_conc before =',np.shape(number_conc))
  #number_conc = np.reshape(number_conc, (Time.shape[0],nlayers, ibins))
  number_conc = np.reshape(number_conc[:reshape_var*nlayers,:], (reshape_var,nlayers, ibins))
  print('shape of number_conc after =',np.shape(number_conc))
  
  nucrate = np.array(pd.read_csv(file[:-11]+'.dat',header=None,delim_whitespace=True))
  print('initial shape of nucrate:',np.shape(nucrate))
  fid1 = np.reshape(nucrate[:reshape_var*nlayers,:], (reshape_var-1, nlayers,7))
  print('reshaped nucrate array:',np.shape(fid1))
  
  if month==9:
    smps_sd,smps_date,smps_bins = SMPS_SD(SMPS_sheetname,startT,endtime)
    search_range = 2
  elif month == 4 or month ==5: 
    if nuc==True:
      smps_sd,smps_date,smps_bins = SD_nanosmps(startT,year,month,day,endtime)
      search_range = 10
    elif nuc==False:
      smps_sd,smps_date,smps_bins = nonuc_nanosmps(startT,year,month,day,endtime)
      search_range = 10

  upnucbin = 14
  lownucbin = 0

  num_conc = np.sum(number_conc[:,:,lownucbin:upnucbin],axis=-1)
  num_conc = num_conc[1:,:]
  ####################################################################
  
  PBL = pbl2(startT,endtime,delt)
  #PBL.fill(np.mean(PBL))
  ####################################################################
  
  temp_file = '../inputs/%s_Temperatures'%file[11:19]
  temp_fid = np.loadtxt(temp_file)
  temps = temp_fid[:,:]
  
  ####################################################################
  
  sfcpres_file = '../inputs/%s_SfcPres'%file[11:19]
  sfcpres = np.loadtxt(sfcpres_file)
  
  Dp_pa = (sfcpres - upper_pres)/nlayers
  
  pres_lay,pres_lay_edge,Z_lay = np.zeros([len(sfcpres),nlayers]),np.zeros([len(sfcpres),nlayers+1]),np.zeros([len(sfcpres),nlayers])
  pres_lay[:,0] = sfcpres[:] - 0.5*Dp_pa[:]
  pres_lay_edge[:,0] = sfcpres[:]
  
  for i in range(nlayers-1):
    for j in range(len(sfcpres)):
      pres_lay[j,i+1] = pres_lay[j,i] - Dp_pa[j]
  for i in range(nlayers):
    for j in range(len(sfcpres)):
      pres_lay_edge[j,i+1] = pres_lay_edge[j,i] - Dp_pa[j]  
  
  Z_lay[:,0] = (287.0*temps[:,0]/9.8 * np.log(pres_lay_edge[:,0]/pres_lay_edge[:,1]))*0.5
  
  for i in range(nlayers-1):
    Z_lay[:,i+1] = Z_lay[:,i] + (287.0*temps[:,i]/9.8 * np.log(pres_lay_edge[:,i]/pres_lay_edge[:,i+1]))*0.5 + (287.0*temps[:,i+1]/9.8 * np.log(pres_lay_edge[:,i+1]/pres_lay_edge[:,i+2]))*0.5

  ####################################################################
 
  FN = fid1[:,:,0]
  fn_ricco = fid1[:,:,1]
  fn_dunne = fid1[:,:,2]
  fn_bn = fid1[:,:,3]
  fn_tn = fid1[:,:,4]
  fn_bi = fid1[:,:,5]
  fn_ti = fid1[:,:,6]

  ####################################################################

  n=3;m=3
  x1 = mdates.date2num(Time)

  #plt.rcParams.update({'font.size': 18})

  fig, axes = plt.subplots(nrows=2, ncols=1,sharex=True)
  #fig.tight_layout()
  #plt.subplots_adjust(wspace = 1.0, hspace=1.0)

  #c1 = axes[0].pcolormesh(x1[1:],Z_lay[0],np.transpose(np.log10(FN)),cmap='jet')
  orig_map=plt.cm.get_cmap('tab20c')
  reversed_map = orig_map #.reversed()
  c1 = axes[0].pcolormesh(x1[1:],Z_lay[0],np.transpose(np.log10(fn_ricco)),cmap=reversed_map)
  orig_map=plt.cm.get_cmap('YlOrRd')
  reversed_map = orig_map #.reversed()
  c3 = axes[1].pcolormesh(x1,Z_lay[0],np.log10(np.transpose(num_conc)),cmap=reversed_map)

  axes[0].plot(x1[1:],PBL,color='k')
  axes[1].plot(x1[1:],PBL,color='k',label='ML Height')
  axes[0].set_ylim(0,2500)
  axes[1].set_ylim(0,2500)
  axes[0].set_xlim(x1[0],x1[-1])
  axes[1].set_xlim(x1[0],x1[-1])
  c3.set_clim(1,4.8)
  c1.set_clim(-1,1.3)
  
  axes[1].set_xticklabels(axes[1].get_xticks(),rotation=35) 
  axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  axes[0].set_yticklabels(['0','500','1000','1500','2000'],rotation=50)
  axes[1].set_yticklabels(['0','500','1000','1500','2000'],rotation=50)
  smps_gr, model_gr, model_indx, smps_indx = [],[],[],[]


  fig.set_size_inches(10,6)
  axes[0].grid(True,axis='x')
  axes[1].grid(True,axis='x')
  axes[0].set_title('%s/%s'%(month,day)) 
  axes[0].set_ylabel('Alt. [m]')
  axes[1].set_ylabel('Alt. [m]')
  axes[1].set_xlabel('Time [CDT]') 
  plt.subplots_adjust(hspace=0.02)
  axes[1].legend(fontsize='small',loc=4)
  axes[0].locator_params(axis='x', nbins=6)
  axes[1].locator_params(axis='x', nbins=6)

  cb1 = fig.colorbar(c1, format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),ax=axes[0],pad=0.01, shrink=0.7, aspect=8, label='Nuc. Rate [#$ /cm^3/s $]')
  cb2 = fig.colorbar(c3, format=mpl.ticker.FormatStrFormatter('$10^{%2.0f}$'),ax=axes[1],pad=0.01, shrink=0.7, aspect=8, label='1.5-25 nm particles \n [#$ /cm^3 $]')
  plt.subplots_adjust(hspace=0.2)
  
  plt.show()
  if save_png==True:
    fig.savefig('%s-%s-%s_%s_%s_FN+NumCon.png'%(month,day,year,cstar,run),bbox_inches='tight')
