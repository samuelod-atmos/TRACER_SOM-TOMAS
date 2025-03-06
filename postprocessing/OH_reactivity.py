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
iorg = 459
srtorglast = srtorg1+iorg
pres = 101325.
R = 8.3145
output_dir = '../outputs'
nlayers =1
what = 'precursors'
upper_pres = 70000
endtime = 144.0

#===========================================================================================================
identify = 'A1e-3'
db = [1E-15]
orgnuc = 1
inorgnuc = 1

#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_gc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])]
files = ['%s/20220801_%s_db1_pwl1_vwl1_OH1.0_FN100.0_HOM0_T1_RH1_gc.dat'%(output_dir,identify)]
#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_bg10__gc.dat'%(output_dir,identify)]
#files = ['%s/20220820_Nobg11103.0176_scale1.00_hr1.00e+01_ricco1_dunn1_bg10_gc.dat'%output_dir]

save_png = False
layer = 0
delt = 300.0
#==================================================================================


for file in files:
  year = 2022
  month = 8
  day = 1
  #print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  Time = []
  startT = dt.datetime(year, month, day, 11, 0)
  print('startT = ',startT)
  
  #    # ----------------------------------------------------------------------------
  df_saprcgc = pd.read_csv('%s_saprcgc.dat'%(file[:-7]),header=None,delim_whitespace=True,)
  
  print('Shape of gas file:',np.shape(df_saprcgc))
  saprc_gas = np.array(df_saprcgc)
  #saprc_gas = np.reshape(saprc_gas, (Time.shape[0], 556))
  print('shape of final gas array:',np.shape(saprc_gas))
  
  #    # ----------------------------------------------------------------------------
  for i in range(len(saprc_gas)):
    sec = int(i*delt)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)

  #    # ----------------------------------------------------------------------------
  #sys.exit('Sucker')
  
  df_spec = pd.read_csv('%s_spec.dat'%(file[:-7]), header=None, delim_whitespace=True)
  saprc_spname = np.array(df_spec.iloc[1,1:1505])
  
  #print('saprc_spname =',saprc_spname)
  #sys.exit('Sucker')
  #    # ----------------------------------------------------------------------------
  #print(Time[0])
  #print(Time[-1])
  #print(np.shape(Time))
  
  #fid1 = np.load(file1,allow_pickle=True)
  #fid2 = np.load(file2,allow_pickle=True)
  #fid3 = np.load(file3,allow_pickle=True)
  #fid4 = np.load(file4,allow_pickle=True)
  #fid5 = np.load(file5)
  
  #print(np.shape(fid1))
  
  if what == 'precursors':
    benzindx = int(np.where(saprc_spname=='BENZENE')[0])
    isopindx = int(np.where(saprc_spname=='ISOPRENE')[0])
    toluindx = int(np.where(saprc_spname=='TOLUENE')[0])
    so2indx  = int(np.where(saprc_spname=='SO2')[0])
    sesqindx = int(np.where(saprc_spname=='SESQTRP')[0])
    terpindx = int(np.where(saprc_spname=='TERPENE')[0])
    trimindx = int(np.where(saprc_spname=='TRIMBNZ')[0])
    xyleindx = int(np.where(saprc_spname=='XYLENE')[0])
    ivocindx = int(np.where(saprc_spname=='IVOC')[0])
    svocindx = int(np.where(saprc_spname=='SVOC')[0])
  
  if what == 'som':
    benzindx = []
    isopindx = []
    toluindx = []
    so2indx  = []
    sesqindx = []
    terpindx = []
    trimindx = []
    xyleindx = []
    ivocindx = []
    svocindx = []
    string = 'This is a string'
    print('The string = ',string)
    
    for i in np.arange(0,len(fid1)):
      temp = str(fid1[i])
    #  print(temp[0:7],'BNZSOMG')
      if temp[:7] == 'BNZSOMG':
    #    print('Yaassss')
        benzindx.append(i)
      elif temp[0:7] == 'ISPSOMG':
        isopindx.append(i)
      elif temp[0:7] == 'TOLSOMG':
        toluindx.append(i)
      elif temp[0:7] == 'SESSOMG':
        sesqindx.append(i)
      elif temp[0:7] == 'TRPSOMG':
        terpindx.append(i)
      elif temp[0:7] == 'TRISOMG':
        trimindx.append(i)
      elif temp[0:7] == 'XYLSOMG':
        xyleindx.append(i)
      elif temp[0:7] == 'IVOSOMG':
        ivocindx.append(i)
      elif temp[0:7] == 'SVOSOMG':
        svocindx.append(i)
  
  benz    = saprc_gas[1:,benzindx]*1000 # ppm -> ppb 
  isop    = saprc_gas[1:,isopindx]*1000
  tolu    = saprc_gas[1:,toluindx]*1000
  so2     = saprc_gas[1:,so2indx]*1000
  sesqtrp = saprc_gas[1:,sesqindx]*1000
  terp    = saprc_gas[1:,terpindx]*1000
  trimeth = saprc_gas[1:,trimindx]*1000
  xylene  = saprc_gas[1:,xyleindx]*1000
  ivoc    = saprc_gas[1:,ivocindx]*1000
  svoc    = saprc_gas[1:,svocindx]*1000


  # -------------------------------------------------------------------------------------------------------------

  x = mdates.date2num(Time[1:])
  #x = np.linspace(0,len(so2),len(so2))/360.
  ax = plt.gca()
  fig = plt.gcf()
  fig.set_size_inches(10,4)
  #plt.scatter(x,so2*1000,s=1.0,label='SO2')
  plt.plot(x,benz*1.22e-12,color='y',label='Cage Benzene')
  plt.plot(x,isop*1.0e-10,color='g',label='Cage Isoprene')
  plt.plot(x,tolu*5.63e-12,color='r',label='Cage Toluene')
  plt.plot(x,terp*5.23e-11,color='m',label='Cage Terpenes')
  plt.plot(x,trimeth*3.27e-11,color='c',label='Cage Trimethylbenzene')
  plt.plot(x,xylene*2.31e-11,color='k',label='Cage M-Xylene')
  
  plt.title('Precursor Gas OH reactivity')
  plt.xlabel('Date')
  plt.ylabel('[ppb]*k_OH',fontsize=12)
  plt.grid(True)
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
  #plt.yscale('log')
  #plt.ylim(0,2)
  plt.legend(loc='best',markerscale=4.)
  plt.show()
  
  #fig.savefig('20160917_GasConc.png',bbox_inches='tight')
  #fig.savefig('CAGE_Amb_mxylene.png',bbox_inches='tight')
