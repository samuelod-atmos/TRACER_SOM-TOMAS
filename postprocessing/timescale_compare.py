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
#identify = 'tmbto'
#identify = 'nopul'
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
#inst_flow = inst_flow[:-1]
switchfile.close()

cs_fid = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_cs.dat'%(output_dir,identify,db[0])

cs_array = np.array(pd.read_csv(cs_fid,header=None,delim_whitespace=True))
#print('initial shape of array:',np.shape(cs_array))
cs_array = cs_array[:,1]

print(np.shape(cs_array),np.shape(inst_flow))

#kpwl = 60.0*2.53E-5
kpwl = 1.27E-4
#kpwl = 1.27E-6
#kpwl = 1.97E-7

t_pwl = np.empty([len(date)])
t_pwl.fill(kpwl)

G_A = (1./cs_array)*(kpwl + 1./inst_flow)

#=================================================================

fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)
fig.set_size_inches(10,5)

x = mdates.date2num(date)

axes.plot(x,1./cs_array,label='t_cs')
axes.plot(x,inst_flow,label='t_inst')
axes.plot(x,1./t_pwl,label='t_pwl')

#=================================================================
axes.set_ylabel('Timescale [s]')
axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
axes.set_yscale('log')
axes.set_ylim(100.,8e6)
axes.legend(loc=2,fontsize=10)

plt.show()

#fig.savefig('%s_gas-aer_kpwl%s_Cstar%s.png'%(identify,str(kpwl),str(l1)),bbox_inches='tight')


