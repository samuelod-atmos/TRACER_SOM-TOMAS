
'''
@author: samuelod
'''

# Import packages
#####################################################
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd


# Parameters
#####################################################
boxvol = 2000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 456
icomp = iorg + 3
srtorglast = srtorg1+iorg
nbins = 40
delt = 300.0

# Path to output directory
#####################################################
output_dir = '../outputs'

# Sage image [True/False]
#####################################################
save_png = False
#save_png = True

# 5 character name of run
#####################################################
#identify = 'styon'
#identify = 'nwgrd'
#identify = 'tmbto'
identify = 'multi'
#identify = 'tmbt2'


# Length of run [hours]
#####################################################
endtime = 144.0

# Particle phase diffusivity
#####################################################
db = [1]
VWL  =  [0] # [0 or 1] the switch for On/Off vapor wall loss
PWL  =  [0,1] # [0 or 1] the switch for On/Off particle wall loss 
OH_multi = [0.8]            # multiplier for OH concentration
HOM_switch = [0]
T_switch = [1]
RH_switch = [1]
fn_multi = [100.0]

labels = ['Perfect Chamber','Base']

# Aerosol mass file name(s)
#####################################################
#files = ['%s/20220801_vwl0_pwl0_hr7.20e+01_Pfunc_bg10_aemass.dat'%output_dir
#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_bg10_aemass.dat'%(output_dir,identify)
#files = ['%s/20220801_%s_vwl1_pwl1_nh35000.0_orgfn1_inorg1_db%s_ohscale1.0_aemass.dat'%(output_dir,identify,db[0])]

plt.figure()
fig = plt.gcf()
ax = plt.gca()
fig.set_size_inches(10,4)

cntr = 0

for dbk in db:
  for pwl in PWL:
#    for vwl in VWL:
      for OH_scale in OH_multi:
        for fn_scale in fn_multi:
          for HOMs in HOM_switch:
            for Temp in T_switch:
              for RH in RH_switch:

                #rname = '%s/20220801_%s_vwl%1i_pwl%1i_nh3%s_orgfn%s_inorg%s_db%s_ohscale%s_aemass.dat'%(output_dir,identify,vwl,pwl,NH3,org_nuc,inorg_nuc,dbk,OH_scale)
                rname = '%s/20220801_%s_A0.001_db%s_pwl%1i_vwl%1i_OH%s_FN%s_HOM%li_T%li_RH%li'%(output_dir,identify,dbk,pwl,pwl,OH_scale,fn_scale,HOMs,Temp,RH)
                
                year = 2022
                month = 8
                day = 1
                print(rname)
                #print('Year = ',year,'Month = ', month,'Day = ', day) 
                
                Time = []
                startT = dt.datetime(year, month, day, 11, 0)
                #print('startT = ',startT)
                
                for i in range(int(endtime*3600/delt+1)):
                  sec = int(i*delt)
                  Time.append(startT + dt.timedelta(seconds = sec))
                Time = np.array(Time)
                
                #sys.exit('You sucker')
                
                # Import spec file to get SOM species names + indecies
                # These files generally don't differ between simulations 
                # unless the SOM grid or number of species has been changed
                ############################################################ 
                #spname_file = '../outputs/20220801_styre_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db1e-15_spec.dat'
                #df_spec = pd.read_csv(spname_file, header=None, delim_whitespace=True)
                #df_spec = pd.read_csv('%s_spec.dat'%(rname[:-11]), header=None, delim_whitespace=True)
                df_spec = pd.read_csv(rname + '_spec.dat', header=None, delim_whitespace=True)
                saprc_spname = np.array(df_spec.iloc[2,:])
                #sys.exit('You suck')
                
                df_ae = np.array(pd.read_csv(rname + '_aemass.dat',header=None, delim_whitespace=True))
                Mk = df_ae[:,1:]
                Mk = np.reshape(Mk, (int(len(Mk)/(icomp)), icomp,nbins))
                Mk = np.sum(Mk,axis=-1)
                
                # Initialize SOM species index lists 
                ############################################################ 
                benzindx = []
                isopindx = []
                toluindx = []
                so2indx  = []
                sulfindx = []
                sesqindx = []
                terpindx = []
                trimindx = []
                xyleindx = []
                ivocindx = []
                svocindx = []
               
                # Loop through SOM names and find indexes for each category 
                ############################################################ 
                for i in np.arange(0,len(saprc_spname)):
                  temp = str(saprc_spname[i])
                  if temp[:7] == 'BNZSOMG':
                    benzindx.append(i-1)
                  elif temp[0:7] == 'ISPSOMG':
                    isopindx.append(i-1)
                  elif temp[0:7] == 'TOLSOMG':
                    toluindx.append(i-1)
                  elif temp[0:7] == 'SESSOMG':
                    sesqindx.append(i-1)
                  elif temp[0:7] == 'TRPSOMG':
                    terpindx.append(i-1)
                  elif temp[0:7] == 'TRISOMG':
                    trimindx.append(i-1)
                  elif temp[0:7] == 'XYLSOMG':
                    xyleindx.append(i-1)
                  elif temp[0:7] == 'IVOSOMG':
                    ivocindx.append(i-1)
                  elif temp[0:7] == 'SVOSOMG':
                    svocindx.append(i-1)
              
                # Make non-volatile, SO4, and H2O arrays
                ############################################################ 
                #nonvol = np.sum(fid[1:,srtorglast2,:],axis=1)/boxvol*1e9*100**3
                nonvol = Mk[0:,-3]#/boxvol*1e9*100**3
                so4 = Mk[0:,srtSO4]#/boxvol*1e9*100**3
                #organic = np.sum(fid[1:,srtorg1:srtorglast,:],axis=2)
                #organic = np.sum(organic, axis=1)/boxvol*1e9*100**3
                #NH4 = np.sum(fid[1:,-2,:],axis=1)/boxvol*1e9*100**3
                H2O = Mk[0:,-1]#/boxvol*1e9*100**3
               
                #sys.exit('Sucker')
               
                # Make mass arrays
                ############################################################ 
                benz = Mk[0:,benzindx]
                tolu = Mk[0:,toluindx]
                xyle = Mk[0:,xyleindx]
                isop = Mk[0:,isopindx]
                terp = Mk[0:,terpindx]
                ivoc = Mk[0:,ivocindx]
                svoc = Mk[0:,svocindx]
                total_org = Mk[0:,srtorg1:srtorglast]
                total = Mk[0:,:]
                #total = Mk[0:,:-1]
                total = np.sum(total, axis=1)#/boxvol*1e9*100**3
                
                
                # Sum across the indecies
                ############################################################ 
                benz = np.sum(benz, axis=1)#/boxvol*1e9*100**3
                tolu = np.sum(tolu, axis=1)#/boxvol*1e9*100**3
                xyle = np.sum(xyle, axis=1)#/boxvol*1e9*100**3
                isop = np.sum(isop, axis=1)#/boxvol*1e9*100**3
                terp = np.sum(terp, axis=1)#/boxvol*1e9*100**3
                ivoc = np.sum(ivoc, axis=1)#/boxvol*1e9*100**3
                svoc = np.sum(svoc, axis=1)#/boxvol*1e9*100**3
               
                #sys.exit("you will bever graduate \n wow you didn't even spell that right")
               
                # Print the organic fraction at the beginning of the sim
                ############################################################ 
                #print('orgfrac =',nonvol[1]/(nonvol[1]+so4[1]))
               
                # Plotting! 
                ############################################################ 
                x = mdates.date2num(Time[0:len(total)])
                #plt.plot(x/360,(benz+tolu+xyle+isop+terp+nonvol)/(benz+tolu+xyle+isop+terp+nonvol+so4),label='Org. Frac.')
                #plt.plot(x/360,organic,label='Organics')
                #plt.plot(x/360,NH4,label='NH4')
                #plt.plot(x,H2O,label='Water')
                plt.plot(x,total,label=labels[cntr])
  #              plt.plot(x,so4,color='r',label='Sulfate')
  #              plt.plot(x,benz,color='y',label='Benzene')
  #              plt.plot(x,tolu,color='b',label='Toluene')
  #              plt.plot(x,xyle,color='cyan',label='m-Xylene')
  #              plt.plot(x,isop,color='green',label='Isoprene')
  #              plt.plot(x,terp,color='lime',label='Terpene')
  #              plt.plot(x,nonvol,color='k',label='Non-Volatile')
                cntr = cntr + 1

plt.title('Total Mass',fontsize=20)
plt.xlabel('Date',fontsize=24)
plt.ylabel('$ \mu g $ $ m^{-3} $',fontsize=24)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.grid(True)
#plt.yscale('log')
plt.legend()
plt.ylim(0.0,1.5)
plt.show()
              
# Save the figure
############################################################ 
if save_png==True:
  fig.savefig('CAGE_%s_AeroComp.png'%file[len(output_dir)+1:-11],bbox_inches='tight')
############################################################ 
