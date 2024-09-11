import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd
import sys

output_dir = '../outputs/'
emiss_scheme = 3
OH_proxy = 3
run = 'E%s_OH%s'%(emiss_scheme, OH_proxy)
cstar = 0.0

files = [
  '%s04272016_%s_Cstar%s_T287.62_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar),
  '%s04282016_%s_Cstar%s_T285.89_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar),
  '%s05112016_%s_Cstar%s_T293.72_NH35.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar),
  '%s05142016_%s_Cstar%s_T282.61_NH32.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar)]

#files = [
#  '%s04252016_%s_Cstar%s_T293.31_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar),
#  '%s05162016_%s_Cstar%s_T288.81_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar),
#  '%s05192016_%s_Cstar%s_T287.82_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar),
#  '%s09042016_%s_Cstar%s_T297.64_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar),
#  '%s09132016_%s_Cstar%s_T300.86_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar),
#  '%s09202016_%s_Cstar%s_T299.88_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10_oh.dat'%(output_dir,run,cstar)]

layer = 1
nlayers = 20
endtime = 10.0
delt = 10.0
R = 8.3145

for file in files:
  year = int(file[15:19])
  month = int(file[11:13])
  day = int(file[13:15])
  print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  if month==4 and day == 25:
    startT = dt.datetime(year, month, day, 9, 20)
    upper_pres = 70000.0    # [Pa] upper level pressure
  if month==4 and day ==27:
    startT = dt.datetime(year, month, day, 9, 20)
    #OH_lower = dt.datetime(2016,4,27,5,30)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month==4 and day ==28:
    startT = dt.datetime(year, month, day, 8, 0)
    #OH_lower = dt.datetime(2016,4,28,5,30)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month==5 and day ==11:
    startT = dt.datetime(year, month, day, 12, 0)
    #OH_lower = dt.datetime(2016, 5, 11,5,30)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month==5 and day == 14:
    startT = dt.datetime(year, month, day, 9, 50)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month == 5 and day == 19:
    startT = dt.datetime(year, month, day, 12, 0)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month == 9 and day == 4:
    startT = dt.datetime(year, month, day, 9, 20)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month==9 and day ==11:
    startT = dt.datetime(year, month, day, 10, 30)
    #OH_lower = dt.datetime(2016, 9, 11,5,30)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month == 9 and day == 13:
    startT = dt.datetime(year, month, day, 10, 0)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month==9 and day ==17:
    startT = dt.datetime(year, month, day, 9, 0)
    #OH_lower = dt.datetime(2016,9,17,5,30)
    upper_pres = 70000.0    # [Pa] upper level pressure
  elif month == 9 and day == 20:
    startT = dt.datetime(year, month, day, 9, 0)
    upper_pres = 70000.0    # [Pa] upper level pressure
  print('startT = ',startT)

  Time = []
  for i in range(int(endtime*3600/delt+1)):
    sec = int(i*delt)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
  print(Time[0])
  print(Time[-1])
  
  
  ####################################################################
  upper = startT + dt.timedelta(hours = endtime)
  sfcpdata = '../scripts/MERRA2_P_data'
  Date = []
  fid3 = open(sfcpdata,'r')
  sfcpres_tmp = []
  for line in fid3.readlines():
    spl_line = line.split(' ')
    Date.append(dt.datetime.strptime(str(spl_line[0]+'-'+spl_line[1]),'%Y-%m-%d-%H:%M:%S' )-dt.timedelta(hours=5))
    sfcpres_tmp.append(spl_line [2]) #[2:-2:2])
  sfcpres_tmp = np.array(sfcpres_tmp)
  
  Date = np.array(Date)
  sfclow = np.where(Date>startT)[0][0]
  sfcup = np.where(Date>upper)[0][0]
  #print('np.shape(sfcpres_tmp) =',np.shape(sfcpres_tmp))
  #print('sfclow =',sfclow,'sfcup =',sfcup)
  P_cut = sfcpres_tmp[sfclow:sfcup]
  #print('sfcpres_tmp[sfclow:sfcup] =',sfcpres_tmp[sfclow:sfcup])
  P_cut = np.array(P_cut)
  P_cut = P_cut.astype(np.float)
  #print('np.shape(P_cut)',np.shape(P_cut))
  #print('P_cut[:] =',P_cut[:])
  sfcpres = np.mean(P_cut)
  
  Dp_pa = (sfcpres - upper_pres)/nlayers
  pres_lay = np.zeros([nlayers])
  pres_lay[0] = sfcpres - 0.5*Dp_pa
  for i in range(nlayers-1):
    pres_lay[i+1] = pres_lay[i] - Dp_pa
#  print('pres_lay =',pres_lay) 
  ####################################################################
  
  temp_file = '../inputs/%s_Temperatures'%file[11:19]
  temp_fid = np.loadtxt(temp_file)
  temps = temp_fid[:,:]
#  print('temps =',temps)
  ####################################################################
  
  saprc_oh = np.array(pd.read_csv('%s'%file,header=None,delim_whitespace=True))
  print('Initial shape of OH array:',np.shape(saprc_oh))
  saprc_oh = np.reshape(saprc_oh, (Time.shape[0],nlayers,2))
  print('shape of OH array:',np.shape(saprc_oh))
  #sys.exit('Just a temporary stop')
  for i in range(nlayers):
    saprc_oh[:,i,1] = saprc_oh[:,i,1]/1.0E6*6.022E23*pres_lay[i]/R/temps[:,i]/1.0E6
  print('shape of OH array:',np.shape(saprc_oh))
#  print('saprc_oh[:,layer-1,1] =',saprc_oh[:,layer-1,1])
  ax = plt.gca()
  fig = plt.gcf()
  fig.set_size_inches(10,6)
 # x = np.linspace(0,len(OH),len(OH))
  x = mdates.date2num(Time)
  plt.plot(x,saprc_oh[:,layer-1,1])
  plt.xlabel('Time [hours]')
  plt.ylabel('OH [molec/cm^3]')
  plt.title('OH Profile - %s/%s/%s'%(month,day,year)) 
  #ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
  plt.show()
  #fig.savefig('%s_OH.png'%file1[0:8],bbox_inches='tight')
