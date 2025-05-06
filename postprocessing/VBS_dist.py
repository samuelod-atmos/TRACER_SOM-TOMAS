import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
plt.rcParams.update({'font.size': 14})

#==================================================================================
#==================================================================================
srtSO4 = 0
srtorg1 = 1
iorg = 456
srtorglast = srtorg1+iorg
icomp = iorg + 3
output_dir = '../outputs'
endtime = 144.0
boxvol  = 2000000.0 
nbins = 40
R = 8.314
MWORG = 200.0

#===========================================================================================================
identify = 'frag4'
db = 1
pwl = 1
vwl = 1
OH_scale = 0.8
FN_scale = 1000.0
HOM = 0
T_switch = 1
RH_switch = 1
A = 1.0e-3


#files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_wallgc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])]
#files = ['%s/20220801_%s_db1_pwl1_vwl1_OH1.0_FN100.0_HOM1_T1_RH1_wallgc.dat'%(output_dir,identify)]
#file = '%s/20220801_%s_A%s_db%i_pwl%i_vwl%i_OH%s_FN%s_HOM%i_T%i_RH1_gc.dat'%(output_dir,identify)
file = '%s/20220801_%s_A%s_db%i_pwl%i_vwl%i_OH%s_FN%s_HOM%i_T%i_RH%i_gc.dat'%(output_dir,identify,A,db,pwl,vwl,OH_scale,FN_scale,HOM,T_switch,RH_switch)

save_png = True
delt = 300.0

#time_low = dt.datetime(2022,8,6,7)
#time_up = dt.datetime(2022,8,6,10)
#t_cs = 2.3
#t_cs = 2.1
#t_cs = 326.

#time_low = dt.datetime(2022,8,6,13)
#time_up = dt.datetime(2022,8,6,16)
#t_cs = 0.5
#t_cs = 3.4
#t_cs = 0.3

time_low = dt.datetime(2022,8,6,19)
time_up = dt.datetime(2022,8,6,22)
#t_cs = 4.9
#t_cs = 4.0
t_cs = 3.7


#time_low = dt.datetime(2022,8,1,11)
#time_up = dt.datetime(2022,8,1,16)
#==================================================================================
# C* bin bounds 
l0,u0 = 0,3.2e-3
l1,u1 = 3.2e-3,3.2e-2
l2,u2 = 3.2e-2,3.2e-1
l3,u3 = 3.2e-1,3.2e0
l4,u4 = 3.2e0,3.2e1
l5,u5 = 3.2e1,3.2e2
l6,u6 = 3.2e2,3.2e3
#==================================================================================

year = 2022
month = 8
day = 1
print('Year = ',year,'Month = ', month,'Day = ', day) 

#==================================================================================

Time = []
startT = dt.datetime(year, month, day, 11, 0)
print('startT = ',startT)

for i in range(int(endtime*3600/delt+1)):
  sec = int(i*delt)
#  print(sec)
  Time.append(startT + dt.timedelta(seconds = sec))
Time = np.array(Time)
low_indx = np.where(Time>time_low)[0][0]
up_indx = np.where(Time<time_up)[0][-1]

#    # ----------------------------------------------------------------------------

#print('file=',file)
df_somgc = pd.read_csv(file,header=None,delim_whitespace=True)

som_gas = np.array(df_somgc)
h2so4 = np.mean(som_gas[low_indx:up_indx,1])/boxvol*1E6*1E9
#h2so4 = 
som_gas = som_gas[:,1:-1]
#print('Shape of gas file:',np.shape(som_gas))

#    # ----------------------------------------------------------------------------
#print(file)
#print('%s_spec.dat'%(file[:-7]))
#sys.exit('Sucker')

#df_spec = pd.read_csv('%s_spec.dat'%(file[:72]), header=None, delim_whitespace=True)
df_spec = pd.read_csv('%s_spec.dat'%(file[:-7]), header=None, delim_whitespace=True)
#df_spec = pd.read_csv('../outputs/20220801_A4e-3_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db1e-15_spec.dat', header=None, delim_whitespace=True)
#df_spec = pd.read_csv('%s/20220801_%s_db1_pwl1_vwl1_OH1.0_FN100.0_HOM1_T1_RH1_spec.dat'%(output_dir,identify),header=None, delim_whitespace=True)
#som_spname = np.array(df_spec.iloc[2,1:iorg+2])
som_cstar = np.array(df_spec.iloc[7,1:iorg+2])
som_cstar = som_cstar[:-1]

for i in range(len(som_cstar)):
  som_cstar[i] = float(som_cstar[i])

#print('len(som_cstar) =',len(som_cstar))

#cstar_n3_n2 = som_gas[low_indx:up_indx,np.where(som_cstar < l1)[0]]
cstar_n3_n2 = som_gas[low_indx:up_indx,np.where((som_cstar > l0) & (som_cstar < u0))[0]]
cstar_n2_n1 = som_gas[low_indx:up_indx,np.where((som_cstar > l1) & (som_cstar < u1))[0]]
cstar_n1_0 = som_gas[low_indx:up_indx,np.where((som_cstar > l2) & (som_cstar < u2))[0]]
cstar_0_1 = som_gas[low_indx:up_indx,np.where((som_cstar > l3) & (som_cstar < u3))[0]]
cstar_1_2 = som_gas[low_indx:up_indx,np.where((som_cstar > l4) & (som_cstar < u4))[0]]
cstar_2_3 = som_gas[low_indx:up_indx,np.where((som_cstar > l5) & (som_cstar < u5))[0]]
cstar_3_4 = som_gas[low_indx:up_indx,np.where((som_cstar > l6) & (som_cstar < u6))[0]]

#print(np.shape(cstar_0_1))

cstar_n3_n2 = np.sum(cstar_n3_n2,axis=1)/boxvol*1E6*1E9
cstar_n2_n1 = np.sum(cstar_n2_n1,axis=1)/boxvol*1E6*1E9
cstar_n1_0 = np.sum(cstar_n1_0,axis=1)/boxvol*1E6*1E9
cstar_0_1 = np.sum(cstar_0_1,axis=1)/boxvol*1E6*1E9
cstar_1_2 = np.sum(cstar_1_2,axis=1)/boxvol*1E6*1E9
cstar_2_3 = np.sum(cstar_2_3,axis=1)/boxvol*1E6*1E9
cstar_3_4 = np.sum(cstar_3_4,axis=1)/boxvol*1E6*1E9
#print(np.shape(cstar_0_1))

cstar_n3_n2 = np.mean(cstar_n3_n2)
cstar_n2_n1 = np.mean(cstar_n2_n1)
cstar_n1_0 = np.mean(cstar_n1_0)
cstar_0_1 = np.mean(cstar_0_1)
cstar_1_2 = np.mean(cstar_1_2)
cstar_2_3 = np.mean(cstar_2_3)
cstar_3_4 = np.mean(cstar_3_4)


#==================================================================================
#file = '%s/20220801_%s_A0.001_db1_pwl1_vwl1_OH0.8_FN1000.0_HOM0_T1_RH1_aemass.dat'%(output_dir,identify)
file = '%s/20220801_%s_A%s_db%i_pwl%i_vwl%i_OH%s_FN%s_HOM%i_T%i_RH%i_aemass.dat'%(output_dir,identify,A,db,pwl,vwl,OH_scale,FN_scale,HOM,T_switch,RH_switch)

#print('file=',file)
df_somaer = np.array(pd.read_csv(file,header=None,delim_whitespace=True))

Mk = df_somaer[:,1:]
Mk = np.reshape(Mk, (int(len(Mk)/(icomp)),icomp,nbins))
Mk = np.sum(Mk,axis=-1)
so4 = np.mean(Mk[low_indx:up_indx,0])
Mk = Mk[:,1:-2]
#print('shape of Mk =',np.shape(Mk))
#print('shape of so4=',np.shape(so4))
#som_aer = np.array(df_somaer)
#h2so4 = 
som_aer = Mk
#print('Shape of aer file:',np.shape(som_aer))

#    # ----------------------------------------------------------------------------
#print(file)
#print('%s_spec.dat'%(file[:-7]))
#print('len(som_cstar) =',len(som_cstar))

#aer_n3_n2 = som_aer[low_indx:up_indx,np.where(som_cstar < l1)[0]]
aer_n3_n2 = som_aer[low_indx:up_indx,np.where((som_cstar > l0) & (som_cstar < u0))[0]]
aer_n2_n1 = som_aer[low_indx:up_indx,np.where((som_cstar > l1) & (som_cstar < u1))[0]]
aer_n1_0 = som_aer[low_indx:up_indx,np.where((som_cstar > l2) & (som_cstar < u2))[0]]
aer_0_1 = som_aer[low_indx:up_indx,np.where((som_cstar > l3) & (som_cstar < u3))[0]]
aer_1_2 = som_aer[low_indx:up_indx,np.where((som_cstar > l4) & (som_cstar < u4))[0]]
aer_2_3 = som_aer[low_indx:up_indx,np.where((som_cstar > l5) & (som_cstar < u5))[0]]
aer_3_4 = som_aer[low_indx:up_indx,np.where((som_cstar > l6) & (som_cstar < u6))[0]]

#print(np.shape(cstar_0_1))

aer_n3_n2 = np.sum(aer_n3_n2,axis=1)#/boxvol*1E6*1E9
aer_n2_n1 = np.sum(aer_n2_n1,axis=1)#/boxvol*1E6*1E9
aer_n1_0 = np.sum(aer_n1_0,axis=1)#/boxvol*1E6*1E9
aer_0_1 = np.sum(aer_0_1,axis=1)#/boxvol*1E6*1E9
aer_1_2 = np.sum(aer_1_2,axis=1)#/boxvol*1E6*1E9
aer_2_3 = np.sum(aer_2_3,axis=1)#/boxvol*1E6*1E9
aer_3_4 = np.sum(aer_3_4,axis=1)#/boxvol*1E6*1E9
#print(np.shape(cstar_0_1))

aer_n3_n2 = np.mean(aer_n3_n2)
aer_n2_n1 = np.mean(aer_n2_n1)
aer_n1_0 = np.mean(aer_n1_0)
aer_0_1 = np.mean(aer_0_1)
aer_1_2 = np.mean(aer_1_2)
aer_2_3 = np.mean(aer_2_3)
aer_3_4 = np.mean(aer_3_4)

#===================================================================================
T_fid = open('../inputs/timeseries/%s%s%s_%s_Temp'%(str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify),'r')

T_list = []
for line in T_fid.readlines():
 T_list.append(float(line))

T_list = np.array(T_list)
#T_list = signal.savgol_filter(T_list,101,2)
T_list = T_list[::30]
Temp = np.mean(T_list[low_indx:up_indx])
print('Temp =',Temp)
#===================================================================================


C_star_bins = np.array([1e-6, 1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 1000.0])
for i in range(len(C_star_bins)):
  HVAP = -11.0*np.log10(C_star_bins[i]) + 131.0 
  PSTAR = C_star_bins[i]*R*300.0/MWORG/1.0e6
  psatorg = PSTAR*np.exp(HVAP*1.e3*(1.0/300.0-1.0/Temp)/R)
  C_star_bins[i] = psatorg/R/Temp*MWORG*1.0e6 


Caerosol = np.array([so4,aer_n3_n2,aer_n2_n1,aer_n1_0,aer_0_1,aer_1_2,aer_2_3,aer_3_4])
Cgasphase = np.array([h2so4,cstar_n3_n2,cstar_n2_n1,cstar_n1_0,cstar_0_1,cstar_1_2,cstar_2_3,cstar_3_4])
C_eqm = []

#for i in range(len(Cgasphase)):
  
Ci = Caerosol + Cgasphase
#print('----------------------------------------------')
#print('Ci =',Ci,'C* = ',C_star_bins)
CoaNew = 10 # this is the initial guess for Coa
Coa = 1 # this is specified here just to get the below loop initiated 
count = 0 # initialize count for the below loop 

'''The following loop finds the new value for Coa to the specified error value and within 50 iterations'''
while abs(Coa-CoaNew) > 10**-10 and count < 50: 
    Coa = CoaNew
    Caer = ((1+C_star_bins/Coa)**-1)*Ci
    #print('Caer =',Caer)
    #CoaNew = Caer
    CoaNew = sum(Caer)
    count = count +1

#print('Caer =',Caer)
#sys.exit()
C_eqm = Caer
  
#print('CoaNew =',CoaNew,Ci)
#print(np.round(CoaNew/Ci*100,3),'%')
C_eqm = np.array(C_eqm)

Caer = np.array([so4,aer_n3_n2,aer_n2_n1,aer_n1_0,aer_0_1,aer_1_2,aer_2_3,aer_3_4])
Ci = np.array([h2so4,cstar_n3_n2,cstar_n2_n1,cstar_n1_0,cstar_0_1,cstar_1_2,cstar_2_3,cstar_3_4])
#Cstar = np.array(['1e-4','1e-3','1e-2','1e-1','1e0','1e1','1e2','1e3'])
Cstar = ['SO4','1e-3','1e-2','1e-1','1e0','1e1','1e2','1e3']
#Caer = np.array([aer_n3_n2,aer_n2_n1,aer_n1_0,aer_0_1,aer_1_2,aer_2_3,aer_3_4])
#Ci = np.array([cstar_n3_n2,cstar_n2_n1,cstar_n1_0,cstar_0_1,cstar_1_2,cstar_2_3,cstar_3_4])
#Cstar = np.array([1e-3,1e-2,1e-1,1e0,1e1,1e2,1e3])
print('Total mass at eqm =',np.sum(C_eqm))
print('Total mass from ST =',np.sum(Caer))

#sys.exit('Sucker')
#==================================================================================
fig, ax = plt.subplots(nrows=1, ncols=1)
fig.set_size_inches(4,5)

#df = pd.DataFrame()
#df['Particle Phase'] = Caer
#df['Particle Phase'] = pd.to_numeric(df['Particle Phase'])
#df['Gas Phase'] = Ci
#df['Gas Phase'] = pd.to_numeric(df['Gas Phase'])
#df['C* Bin'] = Cstar
#df['C* Bin'] = pd.to_numeric(df['C* Bin'])

my_colors = ['red','green','green','green','green','green','green','green']
#my_colors = ['red','white','green','white','green','white','green','white','green','white','green','white','green','white','green','white']
#print('my_colors=',my_colors)
# df.plot.bar(x='Cstar', y='Caer', rot=0)
# df.plot.bar(x='Cstar', y='Ci', rot=0)
#ax = df.plot.bar('C* Bin',['Particle Phase','Gas Phase'],stacked=True,color=['green','white'],edgecolor='black')
#ax = df.plot.bar('C* Bin',stacked=False,color=my_colors,edgecolor='black',legend=False)
plt.bar(Cstar, Caer, color=my_colors, ec='k')
plt.bar(Cstar, Ci, bottom=Caer, color='white', ec='k')
plt.scatter(Cstar, C_eqm, color='k', marker='x',zorder=100,label='Equilibrium')

# Text for base sims
#ax.text(-0.5,4,'%4.3f [$\mu g$ $ m^{-3}$]'%np.sum(Caer))
#ax.text(-0.5,1.5,'%4.3f [$\mu g$ $ m^{-3}$]'%np.sum(C_eqm))

# Text for fragmentation sims
ax.text(-0.5,30.,'%4.3f [$\mu g$ $ m^{-3}$]'%np.sum(Caer))
ax.text(-0.5,10.,'%4.3f [$\mu g$ $ m^{-3}$]'%np.sum(C_eqm))
#ax.text(-0.5,0.6,'%3.2f [h]'%t_cs)
#ax.legend(loc=2,fontsize=14)
#fig = ax.get_figure()
#fig.set_size_inches(4,5)

#ax.set_title(time_low.strftime('%x') + ', ' + time_low.strftime('%H') + ':00-' + time_up.strftime('%H') + ':00')
ax.set_title(time_low.strftime('%H') + ':00-' + time_up.strftime('%H') + ':00')
# ax = df.plot.bar(Cstar,[Caer,Ci-Caer],stacked=True,color=['green','white'],edgecolor='black')
ax.set_yscale('log')
ax.set_ylim(0.00001,100.0)
#ax.set_ylim(0.000001,10.0)
plt.xticks(rotation=70)
#ax.set_ylim(0.0,1.5)
ax.set_ylabel('$\mu g$ $m^{-3}$',fontsize=16)
ax.set_xlabel('C* [$\mu g$ $m^{-3}$]',fontsize=16)


plt.show()


if save_png == True:
  #fig.savefig('%s%s%s%s_hour%s_VBS.png'%(str(time_low.year).zfill(4),str(time_low.month).zfill(2),str(time_low.day).zfill(2),file[len(output_dir)+9:-11],str(time_low.hour).zfill(2)),bbox_inches='tight')
  fig.savefig('%s%s%s%s_hour%s_Log10VBS.png'%(str(time_low.year).zfill(4),str(time_low.month).zfill(2),str(time_low.day).zfill(2),file[len(output_dir)+9:-11],str(time_low.hour).zfill(2)),bbox_inches='tight')

