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
srtorglast = srtorg1+iorg
nbins = 40
delt = 10.0

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
identify = 'x1000'
#identify = 'tmbto'

#=================================================================
db = [1E-15]
orgnuc = 1
inorgnuc = 1


# C* bin bounds 
#=================================================================
l1,u1 = 1e-3,1e-1
l2,u2 = 1e-1,1e0
l3,u3 = 1e0,1e1
l4,u4 = 1e1,1e2
l5,u5 = 1e2,1e3
l6,u6 = 1e3,1e4

#=================================================================
gc_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_gc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])

#=================================================================
df_somgc = pd.read_csv(gc_file,header=None,delim_whitespace=True)
som_gas = np.array(df_somgc)
#print(len(som_gas[1]))
#print(np.shape(som_gas))

som_gas = som_gas[:,1:-1]

df_spec = pd.read_csv('%s_spec.dat'%(gc_file[:-7]), header=None, delim_whitespace=True)
som_spname = np.array(df_spec.iloc[2,1:iorg+2])
som_cstar = np.array(df_spec.iloc[7,1:iorg+2])

som_spname = som_spname[1:]
som_cstar = som_cstar[:-1]
#print(som_spname)


for i in range(len(som_cstar)):
  som_cstar[i] = float(som_cstar[i])
#print(som_cstar)
#print(som_spname[np.where(som_cstar < l1)[0]])
#sys.exit()

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
  startT = startT + dt.timedelta(seconds=10)
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
inst_flow = inst_flow[:-1]
switchfile.close()

cs_fid = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_cs.dat'%(output_dir,identify,db[0])

cs_array = np.array(pd.read_csv(cs_fid,header=None,delim_whitespace=True))
#print('initial shape of array:',np.shape(cs_array))
cs_array = cs_array[:,1]

print(np.shape(cs_array),np.shape(inst_flow))

#kpwl = 60.0*2.53E-5
kpwl = 1.27E-4
#kpwl = 60.0*1.27E-6
#kpwl = 1.97E-7


G_A = (1./cs_array)*(kpwl + 1./inst_flow)



#=================================================================
for i in range(len(som_cstar)):
  som_cstar[i] = float(som_cstar[i])

#=================================================================
cstar_n2_n1 = som_gas[:,np.where(som_cstar < l1)[0]]
#cstar_n1_0 = som_gas[:,np.where((som_cstar > l2) & (som_cstar < u2))[0]]
#cstar_0_1 = som_gas[:,np.where((som_cstar > l3) & (som_cstar < u3))[0]]
#cstar_1_2 = som_gas[:,np.where((som_cstar > l4) & (som_cstar < u4))[0]]
#cstar_2_3 = som_gas[:,np.where((som_cstar > l5) & (som_cstar < u5))[0]]
#cstar_3_4 = som_gas[:,np.where((som_cstar > l6) & (som_cstar < u6))[0]]

#=================================================================
cstar_n2_n1 = np.sum(cstar_n2_n1,axis=1)/boxvol*1E6*1E9
#cstar_n1_0 = np.sum(cstar_n1_0,axis=1)/boxvol*1E6*1E9
#cstar_0_1 = np.sum(cstar_0_1,axis=1)/boxvol*1E6*1E9
#cstar_1_2 = np.sum(cstar_1_2,axis=1)/boxvol*1E6*1E9
#cstar_2_3 = np.sum(cstar_2_3,axis=1)/boxvol*1E6*1E9
#cstar_3_4 = np.sum(cstar_3_4,axis=1)/boxvol*1E6*1E9



# Aerosol mass file name(s)
#####################################################
amass_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_aemass.dat'%(output_dir,identify,db[0])

df_ae = np.array(pd.read_csv(amass_file,header=None, delim_whitespace=True))
print(np.shape(df_ae))
Mk = df_ae[:,1:]
Mk = np.reshape(Mk, (int(len(Mk)/(icomp)), icomp,nbins))
print(np.shape(Mk))
Mk = np.sum(Mk,axis=-1)
print(np.shape(Mk))
Mk = Mk[:,1:-2]
print(np.shape(Mk),np.shape(som_spname),np.shape(som_cstar),np.shape(som_gas))
cstar_aer = Mk[:,np.where(som_cstar < l1)[0]]

cstar_aer = np.sum(cstar_aer, axis=1)
#sys.exit()

#=================================================================

fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)
fig.set_size_inches(10,5)
ax2 = axes.twinx()

x = mdates.date2num(date)

ax2.plot(x,cstar_n2_n1/cstar_aer,color='b',linestyle='--',label='Ratio')
ax2.plot(x[:-1],G_A, color='r',linestyle='--',label='Ratio (simple theory)')
#axes.plot(x,cstar_0_1,  color='r',linestyle='--',label='C*=%s - %s'%(str(l3),str(u3)))
#axes.plot(x,cstar_1_2,  color='c',linestyle='--',label='C*=%s-%s'%(str(l4),str(u4)))
#axes.plot(x,cstar_2_3,  color='m',linestyle='--',label='C*=%s-%s'%(str(l5),str(u5)))
#axes.plot(x,cstar_3_4,  color='y',linestyle='--',label='C*=%s-%s'%(str(l6),str(u6)))

axes.plot(x,cstar_n2_n1,color='green',linestyle='--',label='Gas C*= <= %s'%str(l1))
axes.plot(x,cstar_aer,color='k',linestyle='--',label='Aer C*= <= %s'%str(l1))


#=================================================================
axes.set_ylabel('$ \mu g $ $ m^{-3} $')
axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
#axes.set_yscale('log')
axes.set_ylim(0,0.4)
axes.legend(loc=2,fontsize=10)

ax2.set_ylabel('Gas/Aer. Ratio')
ax2.set_yscale('log')
ax2.set_ylim(0.1,10000)
ax2.legend(loc=1,fontsize=10)
ax2.grid(True)

plt.show()

fig.savefig('%s_gas-aer_kpwl%s_Cstar%s.png'%(identify,str(kpwl),str(l1)),bbox_inches='tight')


