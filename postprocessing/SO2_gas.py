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
what = 'precursors'
upper_pres = 70000
endtime = 10.0

#==================================================================================
#emiss_scheme = 3
#OH_proxy = 2
#run = 'E%s_OH%s_RawPTRMS_ConstPar'%(emiss_scheme, OH_proxy)
#run = 'E%s_OH%s_HOMtest'%(emiss_scheme, OH_proxy)
#cstar = 0.0
#nuc = True
#===========================================================================================================

files = ['%s/20220731_vwl0_pwl1_hr7.20e+01_SO2_test_bg10_gc.dat'%output_dir]
#files = ['%s/20220820_Nobg11103.0176_scale1.00_hr1.00e+01_ricco1_dunn1_bg10_gc.dat'%output_dir]

save_png = False
delt = 10.0
#==================================================================================
amb_fid = open('../inputs/20220731_voc')
SO2_amb = []
for line in amb_fid.readlines():
  spl_line = line.split('   ')
  #print('spl_line=',spl_line)
  SO2_amb.append(float(spl_line[1]))
SO2_amb = np.array(SO2_amb[1:-1])
print('len(SO2)=',np.shape(SO2_amb))

#==================================================================================
for file in files:
  year = 2022
  month = 7
  day = 31
  #print('Year = ',year,'Month = ', month,'Day = ', day) 
  
  Time = []
  startT = dt.datetime(year, month, day, 9, 0)
  print('startT = ',startT)
  
  for i in range(int(endtime*3600/delt+1)):
    sec = int(i*delt)
  #  print(sec)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
  
  #    # ----------------------------------------------------------------------------
  df_saprcgc = pd.read_csv('%s_saprcgc.dat'%(file[:-7]),header=None,delim_whitespace=True,)
  
  print('Shape of gas file:',np.shape(df_saprcgc))
  saprc_gas = np.array(df_saprcgc)
  #saprc_gas = np.reshape(saprc_gas, (Time.shape[0], 556))
  print('shape of final gas array:',np.shape(saprc_gas))
  
  #    # ----------------------------------------------------------------------------
  
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
#    benzindx = int(np.where(saprc_spname=='BENZENE')[0])
#    isopindx = int(np.where(saprc_spname=='ISOPRENE')[0])
#    toluindx = int(np.where(saprc_spname=='TOLUENE')[0])
    so2indx  = int(np.where(saprc_spname=='SO2')[0])
#    sulfindx = int(np.where(saprc_spname=='SULF')[0])
#    sesqindx = int(np.where(saprc_spname=='SESQTRP')[0])
#    terpindx = int(np.where(saprc_spname=='TERPENE')[0])
#    trimindx = int(np.where(saprc_spname=='TRIMBNZ')[0])
#    xyleindx = int(np.where(saprc_spname=='XYLENE')[0])
#    ivocindx = int(np.where(saprc_spname=='IVOC')[0])
#    svocindx = int(np.where(saprc_spname=='SVOC')[0])
  
  
  #print(molwt)
  #benz    = saprc_gas[:,benzindx] #*1e-6*pres/R/T*molwt #(boxvol) 
  #isop    = saprc_gas[:,isopindx]
  #tolu    = saprc_gas[:,toluindx]
  so2     = saprc_gas[:,so2indx]
  #sulf    = saprc_gas[:,sulfindx] #*1e-6*pres*6.022e23/T/8.3145*1e-6
  #sesqtrp = saprc_gas[:,sesqindx]
  #terp    = saprc_gas[:,terpindx]
  #trimeth = saprc_gas[:,trimindx]
  #xylene  = saprc_gas[:,xyleindx]
  #ivoc    = saprc_gas[:,ivocindx]
  #svoc    = saprc_gas[:,svocindx]

#if what == 'som':
#  benz = np.sum(benz,axis=1) 
#  isop = np.sum(isop,axis=1) 
#  tolu = np.sum(tolu,axis=1) 
#  so2 = np.sum(so2,axis=1) 
#  sulf = np.sum(sulf,axis=1) 
#  sesqtrp = np.sum(sesqtrp,axis=1) 
#  terp = np.sum(terp,axis=1)
#  trimeth = np.sum(trimeth,axis=1) 
#  xylene = np.sum(xylene,axis=1)
#  ivoc = np.sum(ivoc,axis=1)
#  svoc = np.sum(svoc,axis=1)
#  print(np.shape(benz))

#print('Shape of fid4',np.shape(fid4))
#benz2 = fid4[0,:,benzindx]*1e-6*pres/R/T*molwt 
#isop2 = fid4[0,:,isopindx]
#tolu2 = fid4[0,:,toluindx]
#so22 = fid4[0,:,so2indx]
#sulf2 = fid4[0,:,sulfindx]*1e-6*pres*6.022e23/T/8.3145*1e-6
#sesqtrp2 = fid4[0,:,sesqindx]
#terp2 = fid4[0,:,terpindx]
#trimeth2 = fid4[0,:,trimindx]
#xylene2 = fid4[0,:,xyleindx]
#ivoc2 = fid4[0,:,ivocindx]
#svoc2 = fid4[0,:,svocindx]
#print(np.shape(benz2))
#if what == 'som':
#  print('Yassss')
#  benz2 = np.sum(benz2,axis=0) 
#  isop2 = np.sum(isop2,axis=0) 
#  tolu2 = np.sum(tolu2,axis=0) 
#  so22 = np.sum(so22,axis=0) 
#  sulf2 = np.sum(sulf2,axis=0) 
#  sesqtrp2 = np.sum(sesqtrp2,axis=0) 
#  terp2 = np.sum(terp2,axis=0)
#  trimeth2 = np.sum(trimeth2,axis=0) 
#  xylene2 = np.sum(xylene2,axis=0)
#  ivoc2 = np.sum(ivoc2,axis=0)
#  svoc2 = np.sum(svoc2,axis=0)
#  print(np.shape(benz2))
#so2 = so2[0:-10]
#print(so2[-30:-1])
#print(np.shape(benz),np.shape(isop),np.shape(tolu),np.shape(so2),np.shape(sulf))
#print(np.nanmax(benz))
#x = np.linspace(0,len(so2),len(so2))
#print(benz)
#==================================================================================
#  x = mdates.date2num(Time)
  x = np.linspace(0,len(so2),len(so2))
  x1 = np.linspace(0,len(SO2_amb),len(SO2_amb))
  ax = plt.gca()
  fig = plt.gcf()
  fig.set_size_inches(10,4)
  plt.scatter(x1,SO2_amb*1000,s=1.0,label='Ambient')
  plt.scatter(x,so2*1000,s=1.0,label='Chamber')
  #plt.scatter(x,sulf*1000,s=1.0,label='Sulfuric Acid')
  #plt.scatter(x,benz*1000,s=1.0,label='Benzene')
  #plt.plot(x,benz2*1000,label='BNZSOMG_old')
  #plt.plot(x,benz*1000,label='BNZSOMG_new')
  #plt.plot(x,benz*1000,label='Benzene new')
  #plt.scatter(x,isop*1000,s=1.0,label='Isoprene')
  #plt.scatter(x,tolu*1000,s=1.0,label='Toluene')
  #plt.scatter(x,sesqtrp*1000,s=1.0,label='Sesqterp')
  #plt.scatter(x,terp*1000,s=1.0,label='Terpenes')
  #plt.scatter(x,trimeth*1000,s=1.0,label='Trimethylbenzene')
  #plt.scatter(x,xylene*1000,s=1.0,label='M-Xylene')
  #plt.scatter(x/360,ivoc*1000,s=1.0,label='IVOC')
  #plt.scatter(x/360,svoc*1000,s=1.0,label='SVOC')
  plt.title('SO2 Gas Conc. (%s/%s/%s)'%(month,day,year))
  plt.xlabel('Time [CST]')
  #plt.ylabel('$ molec. $ $ cm^{-3} $')
  plt.ylabel('ppb',fontsize=12)
  plt.grid(True)
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
  #plt.ylabel('ppb???',fontsize=12)
  plt.yscale('log')
  plt.legend(loc='best',markerscale=4.)
  plt.show()
  
  #fig.savefig('20160917_GasConc.png',bbox_inches='tight')
  #fig.savefig('%s_SO2.png'%file1[0:8],bbox_inches='tight')
