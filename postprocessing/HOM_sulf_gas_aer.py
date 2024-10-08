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
iorg = 477
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
#identify = 'kvpon'
#identify = 'smtOH'
#identify = 'wiMDL'
#identify = 'noinj'
identify = 'debug'

#=================================================================
db = [1E-15]
orgnuc = 1
inorgnuc = 1


#=================================================================
gc_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_gc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])

#=================================================================
df_somgc = pd.read_csv(gc_file,header=None,delim_whitespace=True)
som_gas = np.array(df_somgc)
#print(len(som_gas[1]))
#print(np.shape(som_gas))

sulf = som_gas[:,1]
#HOM = som_gas[:,-2]

#sys.exit()

#=================================================================
hom_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_hom.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])

df_homgc = pd.read_csv(hom_file,header=None,delim_whitespace=True)
hom_gas = np.array(df_homgc)
HOM = hom_gas[:,1]
  
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
#print(len(date))
date = np.array(date)

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

cs_fid = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_cs.dat'%(output_dir,identify,db[0])

cs_array = np.array(pd.read_csv(cs_fid,header=None,delim_whitespace=True))
#print('initial shape of array:',np.shape(cs_array))
cs_array = cs_array[:,1]

print('shapes =',np.shape(cs_array),np.shape(inst_flow))
#sys.exit()

#length = min(len(cs_array),len(inst_flow),len(date))-1

#kpwl = 60.0*2.53E-5
kpwl = 4.E-4
#kpwl = 60.0*1.27E-6
#kpwl = 1.97E-7

G_A_fast = (1./cs_array)*(kpwl + 1./inst_flow)

kpwl = 6.E-5

G_A_slow = (1./cs_array)*(kpwl + 1./inst_flow)


#=================================================================
#for i in range(len(som_cstar)):
#  som_cstar[i] = float(som_cstar[i])

#=================================================================

# Aerosol mass file name(s)
#####################################################
amass_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_aemass.dat'%(output_dir,identify,db[0])

df_ae = np.array(pd.read_csv(amass_file,header=None, delim_whitespace=True))
#print(np.shape(df_ae))
Mk = df_ae[:,1:]
Mk = np.reshape(Mk, (int(len(Mk)/(icomp)), icomp,nbins))
#print(np.shape(Mk))
Mk = np.sum(Mk,axis=-1)
print(np.shape(Mk))
sulfate = Mk[:,0]
print(np.shape(sulfate))
HOM_aer = Mk[:,srtorglast]
H2O = Mk[:,srtorglast+2]

#print(np.shape(Mk),np.shape(som_spname),np.shape(som_cstar),np.shape(som_gas))

#sulfate = np.sum(sulfate, axis=1)
#HOM_aer = np.sum(HOM_aer, axis=1)
#sys.exit()

#=================================================================

fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)
fig.set_size_inches(10,5)
ax2 = axes.twinx()

x = mdates.date2num(date)

#sulf = sulf[:length]
#sulfate = sulfate[:length]

#HOM = HOM[:length]
#HOM_aer = HOM_aer[:length]


ax2.plot(x,(sulf*1e9/boxvol*1e6)/sulfate,color='b',linestyle='--',label='H2SO4/Sulf Ratio')
ax2.plot(x,(HOM*1e9/boxvol*1e6)/HOM_aer,color='orange',linestyle='--',label='HOM Ratio')
ax2.plot(x,G_A_fast, color='r',linestyle='dashdot',label='Theory Fast PWL')
ax2.plot(x,G_A_slow, color='r',linestyle='dotted',label='Theory Slow PWL')
#axes.plot(x,cstar_0_1,  color='r',linestyle='--',label='C*=%s - %s'%(str(l3),str(u3)))
#axes.plot(x,cstar_1_2,  color='c',linestyle='--',label='C*=%s-%s'%(str(l4),str(u4)))
#axes.plot(x,cstar_2_3,  color='m',linestyle='--',label='C*=%s-%s'%(str(l5),str(u5)))
#axes.plot(x,cstar_3_4,  color='y',linestyle='--',label='C*=%s-%s'%(str(l6),str(u6)))

#axes.plot(x,sulf*1e9/boxvol*1e6,color='lightcoral',label='H2SO4')
#axes.plot(x,sulfate,color='darkred',label='Sulfate')

#axes.plot(x,HOM*1e9/boxvol*1e6,color='lightgreen',label='HOM gas')
#axes.plot(x,HOM_aer,color='darkgreen',label='HOM aerosol')
#axes.plot(x,H2O,label='H2O')


#=================================================================
axes.set_ylabel('$ \mu g $ $ m^{-3} $')
axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
axes.set_yscale('log')
axes.set_ylim(2e-6,100)
axes.legend(loc=2,fontsize=10)
axes.grid(True)

ax2.set_ylabel('Gas/Aer. Ratio')
ax2.set_yscale('log')
ax2.set_ylim(0.001,10000)
ax2.legend(loc=1,fontsize=10)
#ax2.grid(True)

plt.show()

#fig.savefig('fig6_%s_gas-aer_kpwl%s.png'%(identify,str(kpwl)),bbox_inches='tight')


