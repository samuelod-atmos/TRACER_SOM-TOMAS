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
srtorglast = srtorg1+iorg
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
identify = 'multi'

#=================================================================
orgnuc = 1
inorgnuc = 1
db = 1
pwl = 1
vwl = 1
OH = 0.8
fn = 1000.0
HOM = 0
T = 1
RH = 1


# C* bin bounds 
#=================================================================
l0,u0 = 0,5e-3
l1,u1 = 5e-3,5e-2
l2,u2 = 5e-2,5e-1
l3,u3 = 5e-1,5e0
l4,u4 = 5e0,5e1
l5,u5 = 5e1,5e2
l6,u6 = 5e2,5e3


#=================================================================
som_grids = ['BNZSOMG',
           'TOLSOMG',
           'XYLSOMG',
           'ISPSOMG',
           'TRPSOMG']

mfrag = [0.8450,
    0.2630,
    0.0800,
    0.0150,
    0.2360]

#=================================================================
#gc_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_gc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])
gc_file = '%s/20220801_%s_A0.001_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_gc.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))

#=================================================================
df_somgc = pd.read_csv(gc_file,header=None,delim_whitespace=True)
som_gas = np.array(df_somgc)

Time = []
for i in range(len(df_somgc)):
  sec = int(i*delt)
  Time.append(sec)
Time = np.array(Time)

#print(len(som_gas[1]))
#print(np.shape(som_gas))

df_spec = pd.read_csv('%s_spec.dat'%(gc_file[:-7]), header=None, delim_whitespace=True)
som_spname = np.array(df_spec.iloc[2,1:iorg+2])
som_cstar = np.array(df_spec.iloc[7,1:iorg+2])

cntr = 0
pfrag = np.empty([len(som_grids),len(Time)])

for som_grid in som_grids:

  OC = []
  gas_list = []
  
  for i in np.arange(1,len(som_gas[0])-3):
    if som_spname[i][:7] == som_grid:
      gas_list.append(i)
      OC.append(int(som_spname[i+102][11:13])/int(som_spname[i+102][8:10]))
  
  OC = np.array(OC)
  #sys.exit('you are bad at this')
  
  #OC_weighted = np.empty([len(Time)])
  
  for i in range(len(Time)):
    #OC_weighted[i] = np.mean(OC*(10.0**saprc_gas[i,1:-2]/np.max(10.0**saprc_gas[i,1:-2])))
    OC_weighted = np.mean(OC*(som_gas[i,gas_list]/np.max(som_gas[i,gas_list])))
    pfrag[cntr,i] = OC_weighted**mfrag[cntr]
  
  cntr = cntr + 1

pfrag_mean = np.mean(pfrag,axis=0)
#print(np.shape(pfrag_mean))
#sys.exit('you are bad at this')
#=================================================================

som_gas = som_gas[:,1:-1]
som_spname = som_spname[1:]
som_cstar = som_cstar[:-1]
#print(som_spname)


for i in range(len(som_cstar)):
  som_cstar[i] = float(som_cstar[i])
#print(som_cstar)
#print(som_spname[np.where(som_cstar < l1)[0]])
#sys.exit()

#=================================================================

year = int(gc_file[11:15])
month = int(gc_file[15:17])
day = int(gc_file[17:19])
startT = dt.datetime(year,month,day,11)
print(startT)

date = []
date.append(startT)

temp_date = startT

for i in range(len(Time)-1):
  #print(Time[i+1])
  temp_date = temp_date + dt.timedelta(seconds=delt)
  date.append(temp_date)
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
inst_flow = inst_flow[::30]
inst_flow = inst_flow[:-1]
switchfile.close()

#cs_fid = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_cs.dat'%(output_dir,identify,db[0])
cs_fid = '%s/20220801_%s_A0.001_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_cs.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))

cs_array = np.array(pd.read_csv(cs_fid,header=None,delim_whitespace=True))
#print('initial shape of array:',np.shape(cs_array))
cs_array = cs_array[:-1,1]

print(np.shape(cs_array),np.shape(inst_flow))

#kpwl = 60.0*2.53E-5
kpwl = 1.27E-4
#kpwl = 60.0*1.27E-6
#kpwl = 1.97E-7


oh_fid = open('../inputs/timeseries/%s%s%s_%s_OH'%(str(startT.year),str(startT.month).zfill(2),str(startT.day).zfill(2),identify),'r')

OH_ts = []
for line in oh_fid.readlines():
 OH_ts.append(float(line))

OH_ts = np.array(OH_ts)

OH_ts = OH_ts[::30]
OH_ts = OH_ts[:-1]

#pfrag = 0.7
koh = 8e-9

print(np.shape(cs_array))
print(np.shape(inst_flow))

G_A_frag = (1.0/cs_array/(koh*OH_ts*pfrag_mean[1:]))*(kpwl + 1./inst_flow)
G_A = (1.0/cs_array)*(kpwl + 1./inst_flow)
#G_A = (cs_array + kpwl + 1./inst_flow)**2.0 * 1.0/cs_array * 1.0/kpwl * inst_flow


#=================================================================
#for i in range(len(som_cstar)):
#  som_cstar[i] = float(som_cstar[i])

#=================================================================
cstar_n2_n1 = som_gas[:,np.where(som_cstar < l1)[0]]
cstar_n1_0 = som_gas[:,np.where((som_cstar > l2) & (som_cstar < u2))[0]]
cstar_0_1 = som_gas[:,np.where((som_cstar > l3) & (som_cstar < u3))[0]]
cstar_1_2 = som_gas[:,np.where((som_cstar > l4) & (som_cstar < u4))[0]]
cstar_2_3 = som_gas[:,np.where((som_cstar > l5) & (som_cstar < u5))[0]]
cstar_3_4 = som_gas[:,np.where((som_cstar > l6) & (som_cstar < u6))[0]]

#=================================================================
cstar_n2_n1 = np.sum(cstar_n2_n1,axis=1)/boxvol*1E6*1E9
cstar_n1_0 = np.sum(cstar_n1_0,axis=1)/boxvol*1E6*1E9
cstar_0_1 = np.sum(cstar_0_1,axis=1)/boxvol*1E6*1E9
cstar_1_2 = np.sum(cstar_1_2,axis=1)/boxvol*1E6*1E9
cstar_2_3 = np.sum(cstar_2_3,axis=1)/boxvol*1E6*1E9
cstar_3_4 = np.sum(cstar_3_4,axis=1)/boxvol*1E6*1E9



# Aerosol mass file name(s)
#####################################################
#amass_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db%s_aemass.dat'%(output_dir,identify,db[0])
amass_file = '%s/20220801_%s_A0.001_db%s_pwl%s_vwl%s_OH%s_FN%s_HOM%s_T%s_RH%s_aemass.dat'%(output_dir,
    identify,
    str(db),
    str(pwl),
    str(vwl),
    str(OH),
    str(fn),
    str(HOM),
    str(T),
    str(RH))
#
#df_ae = np.array(pd.read_csv(amass_file,header=None, delim_whitespace=True))
#Mk = df_ae[:,1:]
#print(np.shape(df_ae),int(len(Mk)/(icomp)))
#Mk = np.reshape(Mk, (int(len(Mk)/(icomp)), icomp,nbins))
#print(np.shape(Mk))
#Mk = np.sum(Mk,axis=-1)
#print(np.shape(Mk))
#Mk = Mk[:,1:-2]
#print(np.shape(Mk),np.shape(som_spname),np.shape(som_cstar),np.shape(som_gas))
#cstar_aer = Mk[:,np.where(som_cstar < l1)[0]]
#
#cstar_aer = np.sum(cstar_aer, axis=1)
##sys.exit()

#==================================================================================
#file = '%s/20220801_%s_A0.001_db1_pwl0_vwl0_OH1.0_FN1000.0_HOM0_T1_RH1_aemass.dat'%(output_dir,identify)

print('amass_file=',amass_file)
df_somaer = np.array(pd.read_csv(amass_file,header=None,delim_whitespace=True))

Mk = df_somaer[:,1:]
Mk = np.reshape(Mk, (int(len(Mk)/(icomp)),icomp,nbins))
Mk = np.sum(Mk,axis=-1)
Mk = Mk[:,1:-2]
print('shape of Mk =',np.shape(Mk))

som_aer = Mk #[:,1:]
print('Shape of aer file:',np.shape(som_aer))

#    # ----------------------------------------------------------------------------
#print(file)
#print('%s_spec.dat'%(file[:-7]))
#print('len(som_cstar) =',len(som_cstar))

#aer_n3_n2 = som_aer[low_indx:up_indx,np.where(som_cstar < l1)[0]]
aer_n3_n2 = som_aer[:,np.where((som_cstar > l0) & (som_cstar < u0))[0]]
aer_n2_n1 = som_aer[:,np.where((som_cstar > l1) & (som_cstar < u1))[0]]
aer_n1_0 = som_aer[:,np.where((som_cstar > l2) & (som_cstar < u2))[0]]
aer_0_1 = som_aer[:,np.where((som_cstar > l3) & (som_cstar < u3))[0]]
aer_1_2 = som_aer[:,np.where((som_cstar > l4) & (som_cstar < u4))[0]]
aer_2_3 = som_aer[:,np.where((som_cstar > l5) & (som_cstar < u5))[0]]
aer_3_4 = som_aer[:,np.where((som_cstar > l6) & (som_cstar < u6))[0]]


aer_n3_n2 = np.sum(aer_n3_n2,axis=1)#/boxvol*1E6*1E9
aer_n2_n1 = np.sum(aer_n2_n1,axis=1)#/boxvol*1E6*1E9
aer_n1_0 = np.sum(aer_n1_0,axis=1)#/boxvol*1E6*1E9
aer_0_1 = np.sum(aer_0_1,axis=1)#/boxvol*1E6*1E9
aer_1_2 = np.sum(aer_1_2,axis=1)#/boxvol*1E6*1E9
aer_2_3 = np.sum(aer_2_3,axis=1)#/boxvol*1E6*1E9
aer_3_4 = np.sum(aer_3_4,axis=1)#/boxvol*1E6*1E9


#=================================================================

fig, axes = plt.subplots(nrows=1, ncols=1,sharex=True)
fig.set_size_inches(10,3)
#ax2 = axes.twinx()

x = mdates.date2num(date)

#ax2.plot(x,cstar_n2_n1/cstar_aer,color='b',linestyle='--',label='Ratio')
#axes.plot(x[:-1],G_A, color='r',linestyle='-',label='Ratio (simple theory)')
#axes.plot(x[:-1],G_A_frag, color='blue',linestyle='-',label='Ratio (with fragmentation)')

#axes.plot(x,aer_n2_n1/(aer_n2_n1+cstar_n2_n1),  color='b',linestyle='--',label='C*=%s - %s'%(str(l1),str(u1)))
#axes.plot(x,aer_n1_0/(aer_n1_0+cstar_n1_0),  color='k',linestyle='--',label='C*=%s - %s'%(str(l2),str(u2)))
#axes.plot(x,aer_0_1/(aer_0_1+cstar_0_1),  color='r',linestyle='--',label='C*=%s - %s'%(str(l3),str(u3)))
#axes.plot(x,aer_1_2/(aer_1_2+cstar_1_2),  color='c',linestyle='--',label='C*=%s-%s'%(str(l4),str(u4)))
#axes.plot(x,aer_2_3/(aer_2_3+cstar_2_3),  color='m',linestyle='--',label='C*=%s-%s'%(str(l5),str(u5)))
#axes.plot(x,aer_3_4/(aer_3_4+cstar_3_4),  color='y',linestyle='--',label='C*=%s-%s'%(str(l6),str(u6)))

#axes.plot(x,cstar_n2_n1/aer_n2_n1,  color='black',linestyle='-',label='C*=%s - %s'%(str(l1),str(u1)))
#axes.plot(x,cstar_n1_0/aer_n1_0,  color='dimgray',linestyle='-',label='C*=%s - %s'%(str(l2),str(u2)))
#axes.plot(x,cstar_0_1/aer_0_1,  color='gray',linestyle='-',label='C*=%s - %s'%(str(l3),str(u3)))
#axes.plot(x,cstar_1_2/aer_1_2,  color='darkgray',linestyle='-',label='C*=%s-%s'%(str(l4),str(u4)))
#axes.plot(x,cstar_2_3/aer_2_3,  color='silver',linestyle='-',label='C*=%s-%s'%(str(l5),str(u5)))
#axes.plot(x,cstar_3_4/aer_3_4,  color='gainsboro',linestyle='-',label='C*=%s-%s'%(str(l6),str(u6)))


axes.plot(x,aer_n2_n1,  color='black',linestyle='-',label='C*=%s - %s'%(str(l1),str(u1)))
axes.plot(x,aer_n1_0,  color='dimgray',linestyle='-',label='C*=%s - %s'%(str(l2),str(u2)))
axes.plot(x,aer_0_1,  color='gray',linestyle='-',label='C*=%s - %s'%(str(l3),str(u3)))
axes.plot(x,aer_1_2,  color='darkgray',linestyle='-',label='C*=%s-%s'%(str(l4),str(u4)))
axes.plot(x,aer_2_3,  color='silver',linestyle='-',label='C*=%s-%s'%(str(l5),str(u5)))
axes.plot(x,aer_3_4,  color='gainsboro',linestyle='-',label='C*=%s-%s'%(str(l6),str(u6)))


#axes.plot(x,cstar_n2_n1,color='green',label='Gas C*= <= %s'%str(l1))
#axes.plot(x,cstar_aer,color='k',label='Aer C*= <= %s'%str(l1))

#=================================================================

#axes.set_ylabel('Gas/Aerosol')
axes.set_ylabel('Aerosol Mass [ug/m^3]')
#axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
axes.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
axes.xaxis.set_major_locator(mdates.HourLocator(interval = 3))
axes.set_yscale('log')
axes.set_ylim(1e-8,)
axes.set_xlim(mdates.date2num(dt.datetime(2022,8,4,7)),mdates.date2num(dt.datetime(2022,8,4,22)))
axes.legend(loc=2,fontsize=10)

#ax2.set_ylabel('Gas/Aer. Ratio')
#ax2.set_yscale('log')
#ax2.set_ylim(0.1,10000)
#ax2.legend(loc=1,fontsize=10)
axes.grid(True)

plt.show()

#fig.savefig('%s_gas-aer_kpwl%s_Cstar%s.png'%(identify,str(kpwl),str(l1)),bbox_inches='tight')


