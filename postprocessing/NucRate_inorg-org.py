import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import matplotlib.dates as mdates 
import sys
import pandas as pd
from PBL_script import pbl2
import datetime as dt

boxvol = 10000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 264
srtorglast = srtorg1+iorg
nlayers = 20
layer = 1
#R = 8.314
#TEMP = 294


emiss_scheme = 3
OH_proxy = 2
run = 'E%s_OH%s_gasmix'%(emiss_scheme, OH_proxy)
#run = 'E%s_OH%s_NoNuc'%(emiss_scheme, OH_proxy)
cstar = 0.0 #1e-7
output_dir = '../outputs/'
endtime = 10.0
delt = 10.0
upper_pres = 70000
save_fig = True

#nuc_type = 'organic'
nuc_type = 'inorganic'

files = [
  '%s04272016_%s_Cstar%s_T287.62_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
  '%s04282016_%s_Cstar%s_T285.89_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
  '%s05112016_%s_Cstar%s_T293.72_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
  '%s05142016_%s_Cstar%s_T282.61_NH32.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
  '%s05162016_%s_Cstar%s_T288.81_NH33.00e+02_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
  '%s05192016_%s_Cstar%s_T287.26_NH33.00e+02_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar)]
#  '%s09112016_%s_Cstar%s_T298.11_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
 # '%s09172016_%s_Cstar%s_T295.18_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar)]
#files = [
#  '%s04252016_%s_Cstar%s_T293.31_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
#  '%s05162016_%s_Cstar%s_T288.81_NH33.00e+02_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
#  '%s05192016_%s_Cstar%s_T287.26_NH33.00e+02_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar)]
#  '%s09042016_%s_Cstar%s_T297.64_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
#  '%s09132016_%s_Cstar%s_T296.83_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar),
#  '%s09202016_%s_Cstar%s_T299.88_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run,cstar)]

for file in files:  
  year = int(file[15:19])
  month = int(file[11:13])
  day = int(file[13:15])
  print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  Time = []
  if month==4 and day ==25:
    startT = dt.datetime(year, month, day, 9, 0)
  elif month==4 and day ==27:
    startT = dt.datetime(year, month, day, 9, 20)
  elif month==4 and day ==28:
    startT = dt.datetime(year, month, day, 8, 0)
  elif month==5 and day ==11:
    startT = dt.datetime(year, month, day, 9, 45)
  elif month==5 and day ==14:
    startT = dt.datetime(year, month, day, 9, 45)
  elif month==5 and day ==16:
    delt = 10.0
    startT = dt.datetime(year, month, day, 9, 0)
  elif month==5 and day ==19:
    delt = 10.0
    startT = dt.datetime(year, month, day, 9, 0)
  elif month==9 and day ==4:
    startT = dt.datetime(year, month, day, 9, 0)
  elif month==9 and day ==11:
    startT = dt.datetime(year, month, day, 10, 0)
  elif month==9 and day ==13:
    startT = dt.datetime(year, month, day, 9, 0)
  elif month==9 and day ==17:
    startT = dt.datetime(year, month, day, 9, 0)
  elif month==9 and day ==20:
    startT = dt.datetime(year, month, day, 9, 0)
  print('startT = ',startT)
  
  for i in range(int(endtime*3600/delt+1)):
    sec = int(i*delt)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
  
  #fid1 = np.load(file1,allow_pickle=True)
  #print(np.shape(fid1))
  
  nucrate = np.array(pd.read_csv(file,header=None,delim_whitespace=True))
  print('initial shape of nucrate:',np.shape(nucrate))
  fid1 = np.reshape(nucrate, (np.shape(Time)[0]-1,nlayers,7))
  print('reshaped nucrate array:',np.shape(nucrate))


  ####################################################################
  
  PBL = pbl2(startT,endtime,delt)
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

#  colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:grey','tab:olive','tab:cyan']
  
#  for i in range(nlayers):
  FN = fid1[:,:,0]
  fn_ricco = fid1[:,:,1]
  fn_dunne = fid1[:,:,2]
  #fn_bn = fid1[:,:,3]
  #fn_tn = fid1[:,:,4]
  #fn_bi = fid1[:,:,5]
  #fn_ti = fid1[:,:,6]
  
  plt.rcParams.update({'font.size': 18})
  plt.figure()
  fig = plt.gcf()
  ax = plt.gca()
  fig.set_size_inches(10,5)
  x = mdates.date2num(Time[1:])
  
  test = (fn_dunne)/FN
  if nuc_type=='inorganic':
    c = ax.pcolormesh(x,Z_lay[0],np.transpose(np.log10(fn_dunne)),cmap='tab20b')
  elif nuc_type=='organic':
    c = ax.pcolormesh(x,Z_lay[0],np.transpose(np.log10(fn_ricco)),cmap='tab20b')
  elif nuc_type=='total':
    c = ax.pcolormesh(x,Z_lay[0],np.transpose(np.log10(FN)),cmap='tab20b')
  #ax.set_xticklabels(ax.get_xticks(),fontsize=14)
  #ax.set_yticklabels(ax.get_yticks(),fontsize=14)
  ax.locator_params(axis='x', nbins=6)
  ax.set_yticklabels(['0','500','1000','1500','2000','2500'],rotation=50)
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  ax.plot(x,PBL,color='k',label='ML Height')
  plt.legend(fontsize='small',loc=4)
  #cb = fig.colorbar(c, format=mpl.ticker.FormatStrFormatter('${%2.1f}$'),pad=0.01, shrink=0.7, aspect=8, label='Nuc. Rate [#$ /cm^3/s $]')
  cb = fig.colorbar(c, format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),pad=0.01, shrink=0.7, aspect=8, label='Nuc. Rate [#$ /cm^3/s $]')
  c.set_clim(-1,2)
  #cb = fig.colorbar(c,ticks=[-1,1],pad=0.01, shrink=0.7, aspect=8)
  #cb.set_label('Organic vs. \n Inorganic Nuc.', labelpad=-55,fontsize=14)
  #cb.set_ticks([]) 
  #cb.ax.set_yticklabels(['Org. Nuc.', 'Inorg. Nuc.'],fontsize=14) 
  #c.set_clim(np.min(test),np.max(test))
  ax.set_xlabel('Time [CDT]',fontsize=18)
  ax.set_ylabel('Alt. [m]',fontsize=18)
  ax.set_title('%s/%s'%(month,day),fontsize=18) 

  plt.grid(True)
  #plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
  #plt.show()
  if save_fig == True:
    fig.savefig('%s-%s-%s_%s_%s_FN.png'%(month,day,year,run,nuc_type),bbox_inches='tight')
