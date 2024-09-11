import numpy as np
import sys
import datetime as dt
from matplotlib import pyplot as plt 
import matplotlib as mpl
import matplotlib.dates as mdates 
import pandas as pd
from scipy.stats import pearsonr


#-------------------------------------------------------------
#-------------------------------------------------------------
def Pearson_correlation(X,Y):
    if len(X)==len(Y):
        Sum_xy = sum((X-X.mean())*(Y-Y.mean()))
        Sum_x_squared = sum((X-X.mean())**2)
        Sum_y_squared = sum((Y-Y.mean())**2)       
        corr = Sum_xy / np.sqrt(Sum_x_squared * Sum_y_squared)
    return corr
#-------------------------------------------------------------
#-------------------------------------------------------------

#----------|+++++|----------
#5 character identifier
identify = 'multi' 
output_dir = '../outputs'
#----------|+++++|----------

# ====================================================================================================

endtime = 144.0   # Length of model run
aadt = 300         # microphysics timestep [s]
ibins = 40        # number of bins

VWL  =  [1,0] # [0 or 1] the switch for On/Off vapor wall loss
PWL  =  [1,0] # [0 or 1] the switch for On/Off particle wall loss 

nh3_ppt = [500.0, 5000.0, 15000.0]   # NH3 concentration [ppt]
OH_multi = [0.5, 1.0, 2.0]            # multiplier for OH concentration
boxvol  = 2000000.0                   # teflon [cm3] - [CalTech 24 m3, CSU 10 m3, CMU ?? m3]

db     = [1.0E-15]  # particle-phase diffusion coefficient [m2/s] (could try 3.4e-15 from Charles) 
organic_nuc = [1,0]      # switch for organic nucleation [0 or 1]
inorganic_nuc = [1,0]    # switch for inorganic nucleation [0 or 1]


# ====================================================================================================
Time = []
#for i in range(int(endtime[0]*3600/delt+1)):
for i in range(int(endtime*60*60/aadt)):
  sec = int(i*aadt)
  Time.append(sec)
Time = np.array(Time)

startT = dt.datetime(2022,8,1,11)
print(startT)
name = '%s%s%s'%(str(startT.year).zfill(4),str(startT.month).zfill(2),str(startT.day).zfill(2))  # date string 

date = []
date.append(startT)

for i in range(len(Time)-1):
  #print(Time[i+1])
  startT = startT + dt.timedelta(seconds=aadt)
  date.append(startT)
#print(len(date))
date = np.array(date)
x = mdates.date2num(date)


# ====================================================================================================
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
Bins = np.array(Bins)
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
totalN = np.sum(totalN[:,:60],axis=1)

fid.close()
##############################################

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

print(date[np.where(low < x1)[0][0]])
print(date[np.where(up < x1)[0][0]])

totalN = np.interp(x, x1[np.where(low < x1)[0][0]:np.where(up < x1)[0][0]], totalN[np.where(low < x1)[0][0]:np.where(up < x1)[0][0]])

#sys.exit()

# ====================================================================================================

fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)

fig.set_size_inches(14,4)
axes.grid(True)
axes.set_title('SOM-TOMAS and SMPS Tot. Num. Compare') 
axes.set_ylabel('Total Number',fontsize=14)
axes.set_xlabel('Date',fontsize=14)
axes.set_xlim(low,up)
axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
#axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axes.set_yscale('log')
#plt.subplots_adjust(hspace=0.02)

axes.locator_params(axis='x', nbins=6)
#axes.set_ylim(0,6000)

#OH_scale = 1.0
#vwl = 1
#pwl = 1
#NH3 = 500.0
#org_nuc = 0
#inorg_nuc = 0
r_square1 = 0.0
r_square2 = 0.0

mae1 = 1.0e10
mae2 = 1.0e10

mse1 = 1.0e20
mse2 = 1.0e20

for NH3 in nh3_ppt:
  for dbk in db:
    for pwl in PWL:
      for vwl in VWL:
        for org_nuc in organic_nuc:
          for inorg_nuc in inorganic_nuc:
            for OH_scale in OH_multi:
            
              rname = '%s/%s_%s_vwl%1i_pwl%1i_nh3%s_orgfn%s_inorg%s_db%s_ohscale%s_noconc.dat'%(output_dir,name,identify,vwl,pwl,NH3,org_nuc,inorg_nuc,dbk,OH_scale)
              print(rname)
              #if rname == '../outputs/20220801_multi_vwl1_pwl1_nh315000.0_orgfn0_inorg1_db1e-15_ohscale0.5_noconc.dat':
              #if rname == '../outputs/20220801_multi_vwl1_pwl1_nh35000.0_orgfn1_inorg1_db1e-15_ohscale1.0_noconc.dat':
              #  color = 'blue'
              #  z = 3
              #  label='Best Correlation'
              ##elif rname == '../outputs/20220801_multi_vwl0_pwl1_nh3500.0_orgfn1_inorg0_db1e-15_ohscale2.0_noconc.dat':
              #elif rname == '../outputs/20220801_multi_vwl0_pwl1_nh3500.0_orgfn1_inorg0_db1e-15_ohscale2.0_noconc.dat':
              #  color = 'orange'
              #  z = 4
              #  label='Best MAE'
              ##elif rname == '../outputs/20220801_multi_vwl1_pwl0_nh3500.0_orgfn1_inorg0_db1e-15_ohscale2.0_noconc.dat':
              #elif rname == '../outputs/20220801_multi_vwl1_pwl0_nh3500.0_orgfn1_inorg0_db1e-15_ohscale2.0_noconc.dat':
              #  color = 'green'
              #  z = 5
              #  label='Best MSE'
              #else:
              color='grey'
              z = 1
              label=''

              df_no = np.array(pd.read_csv(rname,header=None, delim_whitespace=True))
              number_conc = df_no[:,1:]
              #Y = (number_conc[:,:])/BinsE[:]
             
              Y1 = np.sum(number_conc[:,10:],axis=1)
              c1 = axes.plot(x,Y1,color=color,zorder=z,label=label)
              
              #r_square1 = pearsonr(totalN,Y1)[0]
              r_square1 = Pearson_correlation(totalN,Y1)
              mae1 = np.mean(abs(Y1 - totalN))
              mse1 = (sum((totalN-Y1)**2.0))/len(totalN)
              #print(r_square1,Pearson_correlation(totalN,Y1))
              if r_square1 > r_square2:
                r_square2 = r_square1
                best_run = rname
              if mae1 < mae2:
                mae2 = mae1
                best_run_mae = rname
              if mse1 < mse2:
                mse2 = mse1
                best_run_mse = rname
              #print(r_square)
              #cb1 = fig.colorbar(c1, format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),ax=axes,pad=0.0061, label='$ dN/dlog_{10}(D_p) $')
              #c1.set_clim(1,4.3)

print('best run according to correlation:        ',best_run)
print('best run according to mean absolute error:',best_run_mae)
print('best run according to mean squared error: ',best_run_mse)

axes.plot(x,totalN,color='r',label='SMPS')
plt.legend()

plt.show()
