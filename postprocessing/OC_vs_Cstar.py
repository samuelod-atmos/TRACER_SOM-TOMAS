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


# Path to output directory
#####################################################
output_dir = '../outputs'

# Sage image [True/False]
#####################################################
save_png = False
#save_png = True

# 5 character name of run
#####################################################
identify = 'multi'

som_grids = ['BNZSOMG']


db = 1
pwl = 1
vwl = 1
OH = 0.8
fn = 100.0
HOM = 0
T = 1
RH = 1


# Particle phase diffusivity
#####################################################
#db = [1E-15]

# Parameters
#####################################################
boxvol = 2000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 456
srtorglast = srtorg1+iorg
nbins = 40
NACT = 103
delt = 300.0
low_bin = 0
up_bin = 39

# Length of run [hours]
#####################################################
endtime = 144.0

# Aerosol mass file name(s)
#####################################################
#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_aemass.dat'%(output_dir,identify,db[0])
spec_file = '%s/20220801_%s_A0.001_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_spec.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))


for som_grid in som_grids:
  # Import spec file to get SOM species names + indecies
  ############################################################ 
  df_spec = pd.read_csv(spec_file, header=None, delim_whitespace=True)
  saprc_spname = np.array(df_spec.iloc[2,:])
  som_cstar = np.array(df_spec.iloc[7,:iorg+2])
  
  #sys.exit('Give up now')
  
  # Initialize O:C grid array
  ############################################################ 
  
  #sys.exit('you are bad at this')
  OC_ts = [] 
  Cstar = []
  Cnum,Onum = [],[]
  for i in np.arange(1,len(saprc_spname)-NACT-1):
    print(saprc_spname[i][:7])
    if saprc_spname[i][:7] == som_grid: 
      Cstar.append(float(som_cstar[i])) 
      #print(float(saprc_spname[i+1][8:10]), float(saprc_spname[i+1][11:13]))
      OC_ts.append((float(saprc_spname[i+1][11:13]))/(float(saprc_spname[i+1][8:10])))
      Onum.append(float(saprc_spname[i+1][11:13]))
      Cnum.append(float(saprc_spname[i+1][8:10]))
      #Cstar.append(som_cstar[i])
      #OC_ts.append((float(saprc_spname[i+1][11:13])-1)/(float(saprc_spname[i+1][8:10])-1))
      
    if som_grid == 'All':

      #print(som_cstar[i], saprc_spname[i+1][11:13], saprc_spname[i+1][8:10])
      Cstar.append(float(som_cstar[i])) 
      #print(float(saprc_spname[i+1][8:10]), float(saprc_spname[i+1][11:13]))
      OC_ts.append((float(saprc_spname[i+1][11:13]))/(float(saprc_spname[i+1][8:10])))
      Onum.append(float(saprc_spname[i+1][11:13]))
      Cnum.append(float(saprc_spname[i+1][8:10]))

  #sys.exit('give up now')
  Cstar = np.array(Cstar)
  OC_ts = np.array(OC_ts)
  Cnum = np.array(Cnum)
  Onum = np.array(Onum)

  # Plotting 
  ############################################################ 
  fig, axes = plt.subplots(nrows=1, ncols=1)
  fig.set_size_inches(10,4)

  plt.scatter(Cstar,OC_ts)
  #plt.scatter(Cnum,Cstar)
  #plt.scatter(Onum,Cstar)

  #plt.title('C* vs Oxygen #')
  #plt.title('C* vs O:C')
  plt.xlabel('C* [ug/m^3]')
  plt.ylabel('O:C')
  #plt.xlabel('O:C')
  plt.xscale('log')

  plt.show()
  
  # Save the figure 
  ############################################################ 
  if save_png==True:
    #fig.savefig('NPF_event5_Aer_OCgrid_ratio.png',bbox_inches='tight')
    fig.savefig('NPF1_%s_%s_OCgrid_ratio.png'%(file[11:-11],som_grid),bbox_inches='tight')
  
  ############################################################ 
