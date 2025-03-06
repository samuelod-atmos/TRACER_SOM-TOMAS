import numpy as np
import sys
import datetime as dt
from matplotlib import pyplot as plt 
import matplotlib as mpl
import matplotlib.dates as mdates 
import pandas as pd
from scipy.stats import pearsonr


# ====================================================================================================
#----------|+++++|----------
#5 character identifier
identify = 'multi' 
output_dir = '../outputs/'
#----------|+++++|----------
# ====================================================================================================

endtime = 144.0   # Length of model run
aadt = 300         # microphysics timestep [s]
nbins = 40          # number of size bins

VWL  =  [1] # [0 or 1] the switch for On/Off vapor wall loss
PWL  =  [1] # [0 or 1] the switch for On/Off particle wall loss 
OH_multi = [0.8]            # multiplier for OH concentration
boxvol  = 2000000.0                   # teflon [cm3] - [CalTech 24 m3, CSU 10 m3, CMU ?? m3]
db     = [1]  # particle-phase diffusion coefficient [m2/s] (could try 3.4e-15 from Charles) 
RH_switch = [1]
T_switch = [1]
fn_multi = [100.0]
HOM_switch = [0]

# ====================================================================================================
low_date = dt.datetime(2022,8,4,7)
up_date = dt.datetime(2022,8,4,22)
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


# Define bins
#===========================================================================================================
xk = np.zeros(nbins+1)  # particle mass cutoffs [kg]...15 bins makes 16 bin *edges*
if nbins==40:
 xk[0]=1E-21*2**-10  # avg mass per particle in lowest bin edge
 for k in range(1,nbins+1):
    xk[k] = xk[k-1]*2.
elif nbins==15:
 xk[0]=1E-21*2**-6  # avg mass per particle in lowest bin edge
 for k in range(1,nbins+1):
    if k < nbins-1:
        xk[k] = xk[k-1]*4.
    else:
        xk[k] = xk[k-1]*32.

pdens=1400. # fixed density for simplicity
xkm=np.sqrt(xk[:-1]*xk[1:])
Dp=(6.*xkm/pdens/np.pi)**(1.0/3.0)          # [nm] average particle diameter of bin

Dp_lower= (6.*xk[:-1]/pdens/np.pi)**(1.0/3.0)          # [nm] average particle diameter of bin
Dp_upper= (6.*xk[1:]/pdens/np.pi)**(1.0/3.0)          # [nm] average particle diameter of bin

Dp = Dp[10:]

# ====================================================================================================

for dbk in db:
  for pwl in PWL:
    for vwl in VWL:
      for fn_scale in fn_multi:
        for HOMs in HOM_switch:
          for OH_scale in OH_multi:
            for Temp in T_switch:
              for RH in RH_switch:
            
                rname = '%s_%s_A0.001_db%s_pwl%1i_vwl%1i_OH%s_FN%s_HOM%li_T%li_RH%li'%(name,identify,dbk,pwl,vwl,OH_scale,fn_scale,HOMs,Temp,RH)
                print(rname[:6],str(low_date.day).zfill(2),rname[8:])
                
                df_no = np.array(pd.read_csv(output_dir + rname + '_noconc.dat',header=None, delim_whitespace=True))
                number_conc = df_no[:,1:]/np.log10(Dp_upper/Dp_lower)
                Y = number_conc[:,10:]
                #Y1 = np.sum(number_conc[:,10:],axis=1)

                #==========================================================================================================
                f1 = open('sum_files/%s%s%s.SUM'%(rname[:6],str(low_date.day).zfill(2),rname[8:]),'w')
                
                temp = ''
                temp = temp + str('0.0') + '  '
                
                for i in range(len(Dp)):
                  temp = temp + str(Dp[i]) + '  '
                f1.write(temp + '\n')
                
                for i in range(len(Y)):
                  if date[i] > low_date and date[i] < up_date:
                    temp = ''
                    temp = temp + str(x[i]) + '  '
                    for j in range(len(Dp)):
                      temp = temp + str(Y[i,j]) + ' '
                    f1.write(temp + '\n')
                    #f1.write('%s'%str(Y[i]))
                
                f1.close()
                sys.exit()
                
                #==========================================================================================================


