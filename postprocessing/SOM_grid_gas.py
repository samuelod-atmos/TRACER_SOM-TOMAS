
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
#identify = 'tmbto'
identify = 'cfrag'

#som_grids = ['BNZSOMG',
#   'TOLSOMG',
#   'XYLSOMG',
#   'ISPSOMG',
#   'TRPSOMG']

som_grids = ['All']


db = 1
pwl = 1
vwl = 1
OH = 0.8
fn = 1000.0
HOM = 0
T = 1
RH = 1

# Particle phase diffusivity
#####################################################
#db = [1E-15]

# Time index for plotting
#####################################################
time_pick = 8588

#time_low = dt.datetime(2022,8,2,9,45)
#time_up = dt.datetime(2022,8,2,14,15)

#time_low = dt.datetime(2022,8,3,10,15)
#time_up = dt.datetime(2022,8,3,14,30)

#time_low = dt.datetime(2022,8,4,10)
#time_up = dt.datetime(2022,8,4,15,30)

#time_low = dt.datetime(2022,8,5,10)
#time_up = dt.datetime(2022,8,5,15)

time_low = dt.datetime(2022,8,6,10,45)
time_up = dt.datetime(2022,8,6,16)

#time_low = dt.datetime(2022,8,1,11)
#time_up = dt.datetime(2022,8,7,1)

# Parameters
#####################################################
boxvol = 2000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 456
NACT = 578
srtorglast = srtorg1+iorg
nbins = 40
delt = 300.0

# Length of run [hours]
#####################################################
endtime = 144.0


# file name(s)
#####################################################
#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_aemass.dat'%(output_dir,identify,db[0])
files = ['%s/20220801_%s_A0.001_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_aemass.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))]  


for som_grid in som_grids:
  for file in files:
    print('Running file:',file)
    year = 2022
    month = 8
    day = 1
    print('Year = ',year,'Month = ', month,'Day = ', day) 
    
    Time = []
    startT = dt.datetime(year, month, day, 11, 0)
    print('startT = ',startT)
    
    for i in range(int(endtime*3600/delt+1)):
      sec = int(i*delt)
      Time.append(startT + dt.timedelta(seconds = sec))
    Time = np.array(Time)
  
    low_indx = np.where(Time>time_low)[0][0]
    up_indx = np.where(Time<time_up)[0][-1]
    
    #sys.exit('Sucker')
    
    df_spec = pd.read_csv('%s_spec.dat'%(file[:-11]), header=None, delim_whitespace=True)
    #saprc_spname = np.array(df_spec.iloc[1,1:1505])
    saprc_spname = np.array(df_spec.iloc[1,:])
    saprc_cstar = np.array(df_spec.iloc[7,:])
    saprc_mwcb = np.array(df_spec.iloc[6,:])
    #print(saprc_spname[101:-2])
    #sys.exit('you suck')
    # ----------------------------------------------------------------------------
    df_saprcgc = pd.read_csv('%s_gc.dat'%(file[:-11]),header=None,delim_whitespace=True,)
    
    print('Shape of gas file:',np.shape(df_saprcgc))
    saprc_gas = np.array(df_saprcgc)
    #print(max(saprc_gas.all()))
    #sys.exit('give up')
    #saprc_gas = np.reshape(saprc_gas, (Time.shape[0], 556))
    print('shape of final gas array:',np.shape(saprc_gas))
    #sys.exit('give up')
  
    # ----------------------------------------------------------------------------
   
    OC_grid = np.zeros([8,16])
    #print(saprc_spname)
    #print(len(saprc_gas[0]))
    #sys.exit('you are bad at this')
  
    #for i in np.arange(102,len(saprc_gas[0])):
    for i in np.arange(1,len(saprc_gas[0])-3):
      #print(saprc_spname[i][8:10])
      #print(type(saprc_spname[i+102][:7]))
      #sys.exit()
      #print(i)
      #print(i,saprc_spname[i+102])
      #print(saprc_spname[i+103][11:13])
      #if saprc_spname[i+102][:7] == som_grid:
      Cs = int(saprc_spname[i+102][8:10])-1
      Os = int(saprc_spname[i+102][11:13])-1
      #print('Cs and Os =',saprc_spname[i+102],Cs,Os,1e6*1e9/boxvol*np.average(saprc_gas[low_indx:up_indx,i],axis=0))
      print('Cs and Os =',saprc_spname[i+102],saprc_cstar[i],saprc_mwcb[i],np.mean(saprc_gas[low_indx:up_indx,i],axis=0))
      #OC_grid[Os,Cs] += saprc_gas[time_pick,i]*1000.0
      #OC_grid[Os,Cs] += np.average(saprc_gas[:,i]*1000.0,axis=0)
      OC_grid[Os,Cs] += np.average(saprc_gas[low_indx:up_indx,i],axis=0)
      #print(saprc_spname[i][8:13])
  
    #OC_grid[-1,-1] += np.average(saprc_gas[low_indx:up_indx,-3],axis=0)
    OC_grid = 1e6*1e9*OC_grid/boxvol
    #OC_grid = OC_grid/np.amax(OC_grid)
    #print('sum of OC_grid=',np.sum(OC_grid))
    #sys.exit('give up now')
    
    Cs = np.arange(1,17,1)
    Os = np.arange(1,9,1)
  
    fig, axes = plt.subplots(nrows=1, ncols=1)
    #fig = plt.gcf()
    #ax = plt.gca()
    fig.set_size_inches(10,4)
    
    c1 = axes.pcolormesh(Cs,Os,np.log10(OC_grid))
    
    plt.title('%s Gas'%som_grid)
    plt.ylabel('Oxygen #')
    plt.xlabel('Carbon #')
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    #plt.grid(True)
    fig.colorbar(c1,format=mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'),pad=0.01, shrink=0.6, aspect=14, label='$\mu$g /$m^{3}$')
    #fig.colorbar(c1,pad=0.01, shrink=0.6, aspect=14, label='$\mu$g /$m^{3}$')
    #c1.set_clim(-8,0)
    c1.set_clim(-2,0)
    #plt.yscale('log')
    #plt.legend()
    #plt.ylim(0.001,0.1)
    plt.show()
    if save_png==True:
      #fig.savefig('NPF_event5_Gas_OCgrid.png',bbox_inches='tight')
      fig.savefig('NPF5_%s_%s_OCgrid_gas.png'%(file[11:-11],som_grid),bbox_inches='tight')
    #except:
    #print('Could not reshape (or something else) - moving on')
