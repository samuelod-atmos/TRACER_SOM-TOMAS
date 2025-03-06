import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 

#==================================================================================
#==================================================================================

srtSO4 = 0
srtorg1 = 1
iorg = 456
srtorglast = srtorg1+iorg
pres = 101325.
R = 8.3145
output_dir = '../outputs'
nlayers =1
what = 'precursors'
boxvol = 2000000.0
endtime = 144.0

#===========================================================================================================
identify = 'multi'

files = [
    '%s/20220801_%s_A0.001_db1_pwl1_vwl1_OH1.0_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db1_pwl1_vwl1_OH0.8_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db1_pwl1_vwl1_OH0.6_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db1_pwl1_vwl1_OH1.0_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db1_pwl1_vwl1_OH0.8_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db1_pwl1_vwl1_OH0.6_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db2_pwl1_vwl1_OH1.0_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db2_pwl1_vwl1_OH0.8_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db2_pwl1_vwl1_OH0.6_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db2_pwl1_vwl1_OH1.0_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db2_pwl1_vwl1_OH0.8_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db2_pwl1_vwl1_OH0.6_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db3_pwl1_vwl1_OH1.0_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db3_pwl1_vwl1_OH0.8_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db3_pwl1_vwl1_OH0.6_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db3_pwl1_vwl1_OH1.0_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db3_pwl1_vwl1_OH0.8_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db3_pwl1_vwl1_OH0.6_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db4_pwl1_vwl1_OH1.0_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db4_pwl1_vwl1_OH0.8_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db4_pwl1_vwl1_OH0.6_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db4_pwl1_vwl1_OH1.0_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db4_pwl1_vwl1_OH0.8_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    '%s/20220801_%s_A0.001_db4_pwl1_vwl1_OH0.6_FN1000.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify),
    ]
#files = ['%s/20220820_Nobg11103.0176_scale1.00_hr1.00e+01_ricco1_dunn1_bg10_gc.dat'%output_dir]

save_png = False
layer = 0
delt = 300.0
#==================================================================================
temp = []

for file in files:
  year = 2022
  month = 8
  day = 1
  #print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  Time = []
  startT = dt.datetime(year, month, day, 11, 0)
  print('startT = ',startT)
  
  #for i in range(int(endtime*3600/delt+1)):
  #  sec = int(i*delt)
  ##  print(sec)
  #  Time.append(startT + dt.timedelta(seconds = sec))
  #Time = np.array(Time)
  
  #    # ----------------------------------------------------------------------------
  #df_saprcgc = pd.read_csv('%s_gc.dat'%(file[:-7]),header=None,delim_whitespace=True,)
  df_saprcgc = pd.read_csv(file,header=None,delim_whitespace=True,)
  
  print('Shape of gas file:',np.shape(df_saprcgc))
  saprc_gas = np.array(df_saprcgc)
  #saprc_gas = np.reshape(saprc_gas, (Time.shape[0], 556))
  print('shape of final gas array:',np.shape(saprc_gas))
 
  sulf = saprc_gas[:,1]
  print(np.shape(sulf))

  #    # ----------------------------------------------------------------------------
  for i in range(len(saprc_gas)):
    sec = int(i*delt)
  #  print(sec)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)

  # -------------------------------------------------------------------------------------------------------------
  #temp = []
  #temp_fid = open('../inputs/%s%s%s_%s_Temp'%(str(year).zfill(4),str(month).zfill(2),str(day).zfill(2),identify),'r')
  #for line in temp_fid.readlines():
  #  spl_line = line.split('\n')
  #  temp.append(float(spl_line[0])) 
  #temp = np.array(temp)
  #temp = temp[:len(Time)-1]

  sulf = sulf/boxvol*1000.0/98.0*6.022e23
  temp.append(sulf)
  print('temp shape =',np.shape(temp))
  #df2 = pd.DataFrame(sulf)
  #df2 = df2.rename(columns={0: 'Low Sulfuric Acid [molec./cm^3]'})

temp = np.array(temp)
std_sulf = np.std(temp, axis=0)
avg_sulf = np.mean(temp,axis=0)
print(np.shape(avg_sulf),np.shape(Time),np.shape(std_sulf))

  # write to csv
  # -------------------------------------------------------------------------------------------------------------


#df1 = pd.DataFrame(Time)
#df1 = df1.rename(columns={0: 'Date/Time'})
#
#df2 = pd.DataFrame(avg_sulf)
#df2 = df2.rename(columns={0: 'Avg. Sulfuric Acid [molec./cm^3]'})
#
#df3 = pd.DataFrame(std_sulf)
#df3 = df3.rename(columns={0: 'Sulfuric Acid Standard Dev. [molec./cm^3]'})
#
#frames = [df1,df2,df3]
#df = pd.concat(frames,axis=1)
#df.to_excel(excel_writer = 'SOM-TOMAS_sulfuric_acid_20230801_20230807.xlsx')
#
#sys.exit()

# -------------------------------------------------------------------------------------------------------------

x = mdates.date2num(Time)
##x = np.linspace(0,len(so2),len(so2))/360.
fig, ax = plt.subplots()
fig.set_size_inches(10,4)
ax.ticklabel_format(axis='y', style='sci', scilimits=(5,7))
##plt.scatter(x,so2*1000,s=1.0,label='SO2')
ax.plot(x,avg_sulf,label='Sulfuric Acid')
ax.fill_between(x,avg_sulf-std_sulf, avg_sulf+std_sulf ,alpha=0.3) #, facecolor=clrs[i])

plt.title('Sulfuric Acid',fontsize=20)
plt.xlabel('Date',fontsize=16)
plt.ylabel('Molecules $ cm^{-3} $',fontsize=16)
plt.grid(True)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
#plt.yscale('log')
#plt.ylim(1e5,)
plt.legend(loc='best',markerscale=4.)
plt.show()

#fig.savefig('20160917_GasConc.png',bbox_inches='tight')
#fig.savefig('CAGE_h2so4_liny.png',bbox_inches='tight')
