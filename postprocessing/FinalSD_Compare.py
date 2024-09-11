import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from pylab import * 
import pandas as pd 
from BG_sizedist import SD_smps 
import sys
import datetime as dt
from functions import h,closest

output_dir = '../../outputs/'

#runs = #['CstarNuc',
#runs = ['NoHOM', 
#'NoDbk',
#'RHProfile',
#'OHscale',
#'noSIVOC',
#'Emiss2']
#'Emiss3']

#runs = ['ConstRH_Emiss1',
#    'ConstRH_Emiss3',
#    'Emiss1',
#    'Emiss3',
#    'Emiss4',
#    'no_mixing',
#    'no_mixSIVOC',
#    'NoSIVOCEmiss1',
#    'NoSIVOCEmiss3',
#    'ConRHE1SIVOC',
#    'ConRHE3SIVOC']

runs = ['OHprox2_E3']
#   'OHprox2_E1',
#   'ConstRH_E3',
#   'OHprox1_E3',
#   'WithSIVOC_E3',
#   'NoMix_E3',
#   'NoMix_E3_withSIVOC',
#   'E2']

save_png = False
#fig = plt.gcf()
#fig.set_size_inches(8,5)

#=============================================================================
ibins = 40
Dpedge = np.zeros(ibins+1)
Dp_low = 1E-9
Dpedge[0] = Dp_low 
rho_p = 1770.0
for i in range(1,ibins+1):
  Dpedge[i]=Dpedge[i-1]*2**(1./3.) 

MNedge = rho_p*pi/6.*Dpedge**3 
MNcenter = sqrt(MNedge[:-1]*MNedge[1:]) 
Dpcenter = (MNcenter/rho_p*6./pi)**(1./3.) # mDpedge[0] = Dp_low #jrp
#print('Dpcenter[0] =',Dpcenter[0])

#=============================================================================


#files = [
#    '%s04272016_%s_Cstar1e-09_T290.62_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#    '%s04282016_%s_Cstar1e-09_T290.34_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#    '%s05112016_%s_Cstar1e-09_T296.59_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#    '%s09112016_%s_Cstar1e-09_T298.11_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#    '%s09172016_%s_Cstar1e-09_T295.18_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]

rows,cols = 1,2
fig, axes = plt.subplots(nrows=rows, ncols=cols)
fig.set_size_inches(8,4)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.18, hspace=0.22)
print(axes)
#sys.exit('You suck')

#for b in range(rows):
'''
b=0
for z in range(cols):
#  plt.figure()
#  fig = plt.gcf()
#  fig.set_size_inches(8,5)
  for run in runs:
  #  if run != 'CstarNuc':
  #  file = [
  #      '%s04272016_%s_Cstar1e-09_T288.99_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s04282016_%s_Cstar1e-09_T288.76_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s05112016_%s_Cstar1e-09_T294.94_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s09112016_%s_Cstar1e-09_T296.47_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s09172016_%s_Cstar1e-09_T293.86_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #  else:
  #  file = [
  #    '%s04272016_%s_Cstar0.001_T288.99_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s04282016_%s_Cstar0.001_T288.76_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s05112016_%s_Cstar0.001_T294.94_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s09112016_%s_Cstar0.001_T296.47_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s09172016_%s_Cstar0.001_T293.86_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  
    files = [
      '%s04272016_%s_Cstar1e-09_T290.62_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
      '%s04282016_%s_Cstar1e-09_T290.34_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
      '%s05112016_%s_Cstar1e-09_T296.59_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
#      '%s09112016_%s_Cstar1e-09_T298.11_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#      '%s09172016_%s_Cstar1e-09_T295.18_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
    
    file = files[z]
    print('file =',file)
  #  print('shape of df_no=',np.shape(df_no))
    layer = 1
    nlayers = 20
    ibins = 40
    endtime = 10.0
  #  Time = int(endtime*360 + 1)
    year = int(file[18:22])
    month = int(file[14:16])
    day = int(file[16:18])
    delt = 20.0
    
  #=============================================================================
    if month == 4 and day == 27:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
      SMPS_upper = dt.datetime(2016,4,27,17,0)
  #    SMPS_upper = dt.datetime(2016,4,27,20,30)
      startT = dt.datetime(year, month, day, 12, 30)
    elif month == 4 and day == 28:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
      SMPS_upper = dt.datetime(2016,4,28,17,0)
      startT = dt.datetime(year, month, day, 11, 0)
      if run=='NoMix_E3':
        delt = 10.0
    elif month == 5 and day == 11:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160511_R0' 
      SMPS_upper = dt.datetime(2016,5,11,18,0)
      startT = dt.datetime(year, month, day, 12, 30)
    elif month == 9 and day == 11:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160827_R1'
      SMPS_upper = dt.datetime(2016,9,11,16,0)
      startT = dt.datetime(year, month, day, 10, 0)
    elif month == 9 and day == 17:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160827_R1'
      SMPS_upper = dt.datetime(2016,9,17,16,0)
      startT = dt.datetime(year, month, day, 9, 0)
    
    if run=='NoMix_E2' or run=='E2':
      delt = 10.0
    print('startT = ',startT)
    
    Time = []
    for i in range(int(endtime*3600/delt+1)):
      sec = int(i*delt)
    #  print(sec)
      Time.append(startT + dt.timedelta(seconds = sec))
    Time = np.array(Time)
    print(Time[0])
    print(Time[-1])
    print(np.shape(Time))
    index = closest(Time,SMPS_upper)
    print('index =',index)
    print('Time[index] =',Time[index])
  
    df_no = np.array(pd.read_csv(file,header=None, delim_whitespace=True))
    number_conc = df_no[:,1:]
    number_conc = np.reshape(number_conc, (Time.shape[0],nlayers, ibins))
    print('shape of number_conc =',np.shape(number_conc))
  
  #=============================================================================
  #
  #  No1, No2, sigma1, sigma2, mu1, mu2 = SD_smps(SMPS_sheetname,SMPS_upper)
  #  print(No1, No2, sigma1, sigma2, mu1, mu2)
  #=============================================================================
  #  ibins = 40
  #  Dpedge = np.zeros(ibins+1)
  #  Dp_low = 1E-9
  #  Dpedge[0] = Dp_low 
  #  rho_p = 1770.0
  #  for i in range(1,ibins+1):
  #    Dpedge[i]=Dpedge[i-1]*2**(1./3.) 
  #  
  #  MNedge = rho_p*pi/6.*Dpedge**3 
  #  MNcenter = sqrt(MNedge[:-1]*MNedge[1:]) 
  #  Dpcenter = (MNcenter/rho_p*6./pi)**(1./3.) # mDpedge[0] = Dp_low #jrp
  #  print('Dpcenter[0] =',Dpcenter[0])
  #
  #=============================================================================
  
    
    #initial = fid[0,0:]/BinsE
    #final = fid[-1,0:]/BinsE
    #thing = 9*360
    #initial = fid[0,0:]/np.log10(Dpedge[1:]/Dpedge[:-1])
  #  obs = h(Dpcenter*1E9,No1,No2,sigma1,sigma2,mu1,mu2)
  #  print('obs = ',obs)
    final = number_conc[index,layer-1,0:]/np.log10(Dpedge[1:]/Dpedge[:-1])
    initial = number_conc[0,layer-1,0:]/np.log10(Dpedge[1:]/Dpedge[:-1])
  #  print('final = ',final)
  #  fig = plt.gcf()
  #  fig.set_size_inches(8,5)
    axes[b,z].semilogx(1E9*Dpcenter,final)
  #    plt.yticks(rotation=60)
  #  plt.semilogx(1E9*Dpcenter,initial)
  
  #=============================================================================
  No1, No2, sigma1, sigma2, mu1, mu2 = SD_smps(SMPS_sheetname,SMPS_upper)
  print(No1, No2, sigma1, sigma2, mu1, mu2)
  obs = h(Dpcenter*1E9,No1,No2,sigma1,sigma2,mu1,mu2)
  axes[b,z].semilogx(1E9*Dpcenter,obs,color='k',linestyle='--')
  #=============================================================================
  
  #print('sum(obs) =',sum(obs))
  #print('sum(initial) =',sum(initial))
  #print('difference =',sum(obs)-sum(initial))
  #plt.plot(np.arange(0,len(fid[0][1])),(fid[0][1]/boxvol),label='Initial')
  #plt.plot(np.arange(0,len(fid[0][-1])),(fid[0][-1]/boxvol),label='Final')
  #plt.plot(Bins,initial/boxvol,label='Initial')
  #plt.plot(Bins,final/boxvol,label='Initial')
  #runs.append('Obs')
  #print('runs =',runs)
  axes[b,z].set_title('%s/%s/%s'%(month,day,year)) 
  #plt.legend(runs)
#  axes[b,z].set_xlabel('$ D_p $ $ (nm) $')
  #  axes[0].set_ylabel('$ dN/dlog(D_p) $ $[cm^{-3}]$')
  #plt.annotate('Total Number = %4.2f [#/cm^3]' % (np.sum(final)/boxvol),xy=(150,4500))
  #plt.xlim(12,1000)
  #  axes[z].set_yticklabels(axes[z].yaxis.get_majorticklabels(), rotation=45)
  axes[b,z].set_ylim(0,)
  #  axes[z].set_yticklabels(axes[z].yaxis.get_majorticklabels(), rotation=45)
  #  axes[0].legend(runs+['obs'])
  axes[b,z].grid(True)
  axes[b,z].tick_params(direction='in')
  for tick in axes[b,z].get_yticklabels():
    tick.set_rotation(60)
  axes[b,z].tick_params(axis='y', which='major', pad=-3)
'''
b=0
for z in range(cols):
#  plt.figure()
#  fig = plt.gcf()
#  fig.set_size_inches(8,5)
  for run in runs:
  #  if run != 'CstarNuc':
  #  file = [
  #      '%s04272016_%s_Cstar1e-09_T288.99_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s04282016_%s_Cstar1e-09_T288.76_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s05112016_%s_Cstar1e-09_T294.94_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s09112016_%s_Cstar1e-09_T296.47_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s09172016_%s_Cstar1e-09_T293.86_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #  else:
  #  file = [
  #    '%s04272016_%s_Cstar0.001_T288.99_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s04282016_%s_Cstar0.001_T288.76_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s05112016_%s_Cstar0.001_T294.94_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s09112016_%s_Cstar0.001_T296.47_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  #    '%s09172016_%s_Cstar0.001_T293.86_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
  
    files = [
#      '%s04272016_%s_Cstar1e-09_T290.62_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#      '%s04282016_%s_Cstar1e-09_T290.34_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#      '%s05112016_%s_Cstar1e-09_T296.59_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
      '%s09112016_%s_Cstar1e-09_T298.11_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
      '%s09172016_%s_Cstar1e-09_T295.18_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
    
    file = files[z]
    print('file =',file)
  #  print('shape of df_no=',np.shape(df_no))
    layer = 1
    nlayers = 20
    ibins = 40
    endtime = 10.0
  #  Time = int(endtime*360 + 1)
    year = int(file[18:22])
    month = int(file[14:16])
    day = int(file[16:18])
    delt = 20.0
    
  #=============================================================================
    if month == 4 and day == 27:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
      SMPS_upper = dt.datetime(2016,4,27,17,0)
  #    SMPS_upper = dt.datetime(2016,4,27,20,30)
      startT = dt.datetime(year, month, day, 12, 30)
    elif month == 4 and day == 28:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160424_R0'
      SMPS_upper = dt.datetime(2016,4,28,17,0)
      startT = dt.datetime(year, month, day, 11, 0)
      if run=='NoMix_E3':
        delt = 10.0
    elif month == 5 and day == 11:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160511_R0' 
      SMPS_upper = dt.datetime(2016,5,11,18,0)
      startT = dt.datetime(year, month, day, 12, 30)
    elif month == 9 and day == 11:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160827_R1'
      SMPS_upper = dt.datetime(2016,9,11,16,0)
      startT = dt.datetime(year, month, day, 10, 0)
    elif month == 9 and day == 17:
      SMPS_sheetname = 'HiScaleSMPSb_SGP_20160827_R1'
      SMPS_upper = dt.datetime(2016,9,17,16,0)
      startT = dt.datetime(year, month, day, 9, 0)
  
    if run=='NoMix_E2' or run=='E2':
      delt = 10.0
    print('startT = ',startT)
    
    Time = []
    for i in range(int(endtime*3600/delt+1)):
      sec = int(i*delt)
    #  print(sec)
      Time.append(startT + dt.timedelta(seconds = sec))
    Time = np.array(Time)
    print(Time[0])
    print(Time[-1])
    print(np.shape(Time))
    index = closest(Time,SMPS_upper)
    print('index =',index)
    print('Time[index] =',Time[index])
  
    df_no = np.array(pd.read_csv(file,header=None, delim_whitespace=True))
    number_conc = df_no[:,1:]
    number_conc = np.reshape(number_conc, (Time.shape[0],nlayers, ibins))
    print('shape of number_conc =',np.shape(number_conc))
  
  #=============================================================================
  #
  #  No1, No2, sigma1, sigma2, mu1, mu2 = SD_smps(SMPS_sheetname,SMPS_upper)
  #  print(No1, No2, sigma1, sigma2, mu1, mu2)
  #=============================================================================
  #  ibins = 40
  #  Dpedge = np.zeros(ibins+1)
  #  Dp_low = 1E-9
  #  Dpedge[0] = Dp_low 
  #  rho_p = 1770.0
  #  for i in range(1,ibins+1):
  #    Dpedge[i]=Dpedge[i-1]*2**(1./3.) 
  #  
  #  MNedge = rho_p*pi/6.*Dpedge**3 
  #  MNcenter = sqrt(MNedge[:-1]*MNedge[1:]) 
  #  Dpcenter = (MNcenter/rho_p*6./pi)**(1./3.) # mDpedge[0] = Dp_low #jrp
  #  print('Dpcenter[0] =',Dpcenter[0])
  #
  #=============================================================================
  
    
    #initial = fid[0,0:]/BinsE
    #final = fid[-1,0:]/BinsE
    #thing = 9*360
    #initial = fid[0,0:]/np.log10(Dpedge[1:]/Dpedge[:-1])
  #  obs = h(Dpcenter*1E9,No1,No2,sigma1,sigma2,mu1,mu2)
  #  print('obs = ',obs)
    final = number_conc[index,layer-1,0:]/np.log10(Dpedge[1:]/Dpedge[:-1])
    initial = number_conc[0,layer-1,0:]/np.log10(Dpedge[1:]/Dpedge[:-1])
  #  print('final = ',final)
  #  fig = plt.gcf()
  #  fig.set_size_inches(8,5)
    axes[z].semilogx(1E9*Dpcenter,final)
  #    plt.yticks(rotation=60)
  #  plt.semilogx(1E9*Dpcenter,initial)
  
  #=============================================================================
  No1, No2, sigma1, sigma2, mu1, mu2 = SD_smps(SMPS_sheetname,SMPS_upper)
  print(No1, No2, sigma1, sigma2, mu1, mu2)
  obs = h(Dpcenter*1E9,No1,No2,sigma1,sigma2,mu1,mu2)
  axes[z].semilogx(1E9*Dpcenter,obs,color='k',linestyle='--')
  #=============================================================================
  
  #print('sum(obs) =',sum(obs))
  #print('sum(initial) =',sum(initial))
  #print('difference =',sum(obs)-sum(initial))
  #plt.plot(np.arange(0,len(fid[0][1])),(fid[0][1]/boxvol),label='Initial')
  #plt.plot(np.arange(0,len(fid[0][-1])),(fid[0][-1]/boxvol),label='Final')
  #plt.plot(Bins,initial/boxvol,label='Initial')
  #plt.plot(Bins,final/boxvol,label='Initial')
  #runs.append('Obs')
  #print('runs =',runs)
  axes[z].set_title('%s/%s/%s'%(month,day,year)) 
  #plt.legend(runs)
  axes[z].set_xlabel('$ D_p $ $ (nm) $')
  #  axes[0].set_ylabel('$ dN/dlog(D_p) $ $[cm^{-3}]$')
  #plt.annotate('Total Number = %4.2f [#/cm^3]' % (np.sum(final)/boxvol),xy=(150,4500))
  #plt.xlim(12,1000)
  #  axes[z].set_yticklabels(axes[z].yaxis.get_majorticklabels(), rotation=45)
  axes[z].set_ylim(0,)
  #  axes[z].set_yticklabels(axes[z].yaxis.get_majorticklabels(), rotation=45)
  #  axes[0].legend(runs+['obs'])
  axes[z].grid(True)
  axes[z].tick_params(direction='in')
  for tick in axes[z].get_yticklabels():
    tick.set_rotation(60)
  axes[z].tick_params(axis='y', which='major', pad=-3)




#  plt.yticks(rotation=60)

#for tick in axes[z].get_xticklabels():
#  tick.set_rotation(45)

#plt.yticks(rotation=45)
axes[0].set_ylabel('$ dN/dlog(D_p) $ $[cm^{-3}]$')
axes[1].legend(['SOM-TOMAS','SMPS']) #, bbox_to_anchor=(1.05, 1),fontsize='small', loc='upper left', borderaxespad=0. )
#axes[1,1].set_zorder(1)
#axes[1,2].spines["top"].set_color('white')
#axes[1,2].spines["bottom"].set_color('white')
#axes[1,2].spines["left"].set_color('white')
#axes[1,2].spines["right"].set_color('white')
#axes[1,2].tick_params(axis='both', colors='white')

plt.show()
  
#fig.savefig('%s-%s-%s_FinalSD_compare.png'%(year,month,day),bbox_inches='tight')
if save_png==True:
  fig.savefig('FinalSD_compare.png',bbox_inches='tight')
