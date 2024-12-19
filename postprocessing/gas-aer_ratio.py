#=================================================================
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 
import sys
#=================================================================


#=================================================================
output_dir = '../outputs'
boxvol = 2000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 456
icomp = iorg + 3
srtorglast = srtorg1+iorg-1
nbins = 40
delt = 300.0

#=================================================================
#identify = 'styre'
#identify = 'tmbxy'
#identify = 'A2e-3'
#identify = 'A7e-6'
#identify = 'HiNOx'
#identify = 'A7e-4'
#identify = 'dbk_0'
#identify = 'v2pwl'
#identify = 'sm_OH'
#identify = 'noHOM'
#identify = 'x1000'
#identify = 'tmbto'
#identify = 'wiMDL'
#identify = 'debug'
identify = 'multi'

#=================================================================
#db = [1E-15]
orgnuc = 1
inorgnuc = 1

db = 1
pwl = 1
vwl = 1
OH_scale = 0.8
FN_scale = 1000.0
HOM = 0
T_switch = 1
RH_switch = 1
A = 1.0e-3


#=================================================================
#gc_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_gc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])
gc_file = '%s/20220801_%s_A%s_db%i_pwl%i_vwl%i_OH%s_FN%s_HOM%i_T%i_RH%i_gc.dat'%(output_dir,identify,A,db,pwl,vwl,OH_scale,FN_scale,HOM,T_switch,RH_switch)
#=================================================================
df_somgc = pd.read_csv(gc_file,header=None,delim_whitespace=True)
som_gas = np.array(df_somgc)
#print(len(som_gas[1]))
#print(np.shape(som_gas))

sulf = som_gas[:,1]
#HOM = som_gas[:,-2]

#sys.exit()

#=================================================================
'''
hom_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_hom.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])

df_homgc = pd.read_csv(hom_file,header=None,delim_whitespace=True)
hom_gas = np.array(df_homgc)
HOM = hom_gas[:,1]
'''
#=================================================================
Time = []
for i in range(len(df_somgc)):
  sec = int(i*delt)
  Time.append(sec)
Time = np.array(Time)

year = int(gc_file[11:15])
month = int(gc_file[15:17])
day = int(gc_file[17:19])
startT = dt.datetime(year,month,day,11)
print(startT)

date = []
date.append(startT)

for i in range(len(Time)-1):
  #print(Time[i+1])
  startT = startT + dt.timedelta(seconds=delt)
  date.append(startT)
date = np.array(date)
print(len(date))

#=================================================================

switchfile = open('../inputs/TRACER_flow_switches/Interp_flows.txt')

inst_flow = []
for line in switchfile.readlines():
  spl_line = line.split(',') 
  dates = dt.datetime.strptime(spl_line[0],'%Y-%m-%d %H:%M:%S')
  switch = float(spl_line[1]) #/1000.  #conversion to ppm is done in box.f 
 
  if dates >= date[0] and dates <= date[-1]:
    inst_flow.append(switch*133.0*60.0)

inst_flow = np.array(inst_flow)
#inst_flow = inst_flow[:-1]
inst_flow = inst_flow[::30]
switchfile.close()

#cs_fid = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_cs.dat'%(output_dir,identify,db[0])
cs_fid = '%s/20220801_%s_A%s_db%i_pwl%i_vwl%i_OH%s_FN%s_HOM%i_T%i_RH%i_cs.dat'%(output_dir,identify,A,db,pwl,vwl,OH_scale,FN_scale,HOM,T_switch,RH_switch)

cs_array = np.array(pd.read_csv(cs_fid,header=None,delim_whitespace=True))
#print('initial shape of array:',np.shape(cs_array))
cs_array = cs_array[:,1]

print(np.shape(cs_array),np.shape(inst_flow))

length = min(len(cs_array),len(inst_flow),len(date))-1

#kpwl = 60.0*2.53E-5
#kpwl = 1.27E-4
#kpwl = 60.0*1.27E-6
#kpwl = 1.97E-7

#G_A_fast = (1./cs_array[:length])*(kpwl + 1./inst_flow[:length])

#kpwl = 1.97E-7

#G_A_slow = (1./cs_array[:length])*(kpwl + 1./inst_flow[:length])


#=================================================================
ibins = 40

A = 1.0E-3    #nm/s
xk = np.zeros(ibins+1) 
xk[0]=1E-21*2**-10 
for k in range(1,ibins+1):
   xk[k] = xk[k-1]*2.
pdens=1400. # fixed density for simplicity
xkm=np.sqrt(xk[:-1]*xk[1:])
Dp=((6.*xkm/pdens/np.pi)**(1.0/3.0))*1E9 # [m] average particle diameter of bin

kflat = 6.9E-5

kpar = []
for i in range(len(Dp)):
  if i < 5:
    kpar.append(float(A/Dp[4]+kflat))
  else:
    kpar.append(float(A/Dp[i]+kflat))

kpar = np.array(kpar)

#=================================================================

# Aerosol mass file name(s)
#####################################################
#amass_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_aemass.dat'%(output_dir,identify,db[0])
amass_file = '%s/20220801_%s_A%s_db%i_pwl%i_vwl%i_OH%s_FN%s_HOM%i_T%i_RH%i_aemass.dat'%(output_dir,identify,A,db,pwl,vwl,OH_scale,FN_scale,HOM,T_switch,RH_switch)

df_ae = np.array(pd.read_csv(amass_file,header=None, delim_whitespace=True))
#print(np.shape(df_ae))
Mk = df_ae[:,1:]
Mk = np.reshape(Mk, (int(len(Mk)/(icomp)), icomp,nbins))
#print(np.shape(Mk))
smalls = np.sum(Mk[:,0,0:10],axis=-1)
meds = np.sum(Mk[:,0,10:14],axis=-1)
larges = np.sum(Mk[:,0,20:30],axis=-1)
#print(np.shape(smalls))
#sys.exit()
Mk = np.sum(Mk,axis=-1)

print(np.shape(Mk))
sulfate = Mk[:,0]
print(np.shape(sulfate))
#HOM_aer = Mk[:,srtorglast]
#H2O = Mk[:,srtorglast+2]

#print(np.shape(Mk),np.shape(som_spname),np.shape(som_cstar),np.shape(som_gas))

#sulfate = np.sum(sulfate, axis=1)
#HOM_aer = np.sum(HOM_aer, axis=1)
#sys.exit()

#=================================================================

fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)
fig.set_size_inches(10,5)
#ax2 = axes.twinx()

x = mdates.date2num(date[:length])

sulf = sulf[:length]
sulfate = sulfate[:length]
smalls = smalls[:length]
meds = meds[:length]
larges = larges[:length]


axes.plot(x,(sulf*1e9/boxvol*1e6)/sulfate,color='b',linestyle='--',label='H2SO4/Sulfate Ratio')
axes.plot(x,(sulf*1e9/boxvol*1e6)/smalls,linestyle='--',label='Small Particles')
axes.plot(x,(sulf*1e9/boxvol*1e6)/meds,linestyle='--',label='Medium Particles')
axes.plot(x,(sulf*1e9/boxvol*1e6)/larges,linestyle='--',label='Large Particles')

for i in range(int(ibins/4)):
  G_A = (1./cs_array[:length])*(kpar[i*4] + 1./inst_flow[:length])
  axes.plot(x,G_A,linestyle='dotted',label='Dp = %5.2f [nm]'%Dp[i*4])

#axes.plot(x,G_A_fast, color='r',linestyle='dashdot',label='Theory Fast PWL')
#axes.plot(x,G_A_slow, color='r',linestyle='dotted',label='Theory Slow PWL')
#axes.plot(x,cstar_0_1,  color='r',linestyle='--',label='C*=%s - %s'%(str(l3),str(u3)))
#axes.plot(x,cstar_1_2,  color='c',linestyle='--',label='C*=%s-%s'%(str(l4),str(u4)))
#axes.plot(x,cstar_2_3,  color='m',linestyle='--',label='C*=%s-%s'%(str(l5),str(u5)))
#axes.plot(x,cstar_3_4,  color='y',linestyle='--',label='C*=%s-%s'%(str(l6),str(u6)))

#axes.plot(x,sulf*1e9/boxvol*1e6,color='lightcoral',label='H2SO4')
#axes.plot(x,sulfate,color='darkred',label='Sulfate')

#axes.plot(x[1:],HOM*1e9/boxvol*1e6,color='lightgreen',label='HOM gas')
#axes.plot(x,HOM_aer,color='darkgreen',label='HOM aerosol')
#axes.plot(x,H2O,label='H2O')


#=================================================================

axes.set_ylabel('Gas/Aer. Ratio')
axes.set_yscale('log')
axes.set_ylim(0.001,10000)
axes.legend(loc=1,fontsize=10)
axes.grid(True)
axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))

plt.show()

#fig.savefig('%s_gas-aer_kpwl%s_Cstar%s.png'%(identify,str(kpwl),str(l1)),bbox_inches='tight')


