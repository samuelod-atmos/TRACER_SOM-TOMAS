import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import pandas as pd
import datetime as dt

#----------------------------------------------------------------------------------------------------------
#colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:grey','tab:olive','tab:cyan']
nlayers = 20
layer = 1
output_dir = '../../outputs/'
endtime = 10.0
delt = 20.0
#----------------------------------------------------------------------------------------------------------

#run = 'CstarNuc'
run = 'E3_OH2' 
#run = 'NoDbk'
#run = 'RHProfile'
#run = 'OHscale' 
#run = 'noSIVOC'
#run = 'Emiss2'
#run = 'Emiss3'

#----------------------------------------------------------------------------------------------------------
#file = [
#  '%s04272016_%s_Cstar1e-09_T288.99_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run)]
#  '%s04282016_%s_Cstar1e-09_T288.76_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_fn.dat'%(output_dir,run),
#  '%s05112016_%s_Cstar1e-09_T294.94_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_fn.dat'%(output_dir,run),
#  '%s09112016_%s_Cstar1e-09_T296.47_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_fn.dat'%(output_dir,run),
#  '%s09172016_%s_Cstar1e-09_T293.86_NH31.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_fn.dat'%(output_dir,run)]

#files = [
#  '%s04272016_%s_Cstar0.001_T288.99_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#  '%s04282016_%s_Cstar0.001_T288.76_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#  '%s05112016_%s_Cstar0.001_T294.94_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#  '%s09112016_%s_Cstar0.001_T296.47_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run),
#  '%s09172016_%s_Cstar0.001_T293.86_NH32.00e+03_nlay10_hr1.00e+01_ricco1_dunn1_bg10_noconc.dat'%(output_dir,run)]
file = [
  '%s04272016_%s_Cstar1e-09_T290.62_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run)]
#  '%s04282016_%s_Cstar1e-09_T290.34_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run)]
#  '%s05112016_%s_Cstar1e-09_T296.59_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run)]
#  '%s05142016_%s_Cstar1e-09_T282.61_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run)]
#  '%s09112016_%s_Cstar1e-09_T298.11_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run)]
#  '%s09172016_%s_Cstar1e-09_T295.18_NH31.00e+03_nlay20_hr1.00e+01_ricco1_dunn1_bg10.dat'%(output_dir,run)]
#----------------------------------------------------------------------------------------------------------


year = int(file[0][18:22])
month = int(file[0][14:16])
day = int(file[0][16:18])
print('Year = ',year,'Month = ', month,'Day = ', day) 

Time = []
if month==4 and day ==27:
  startT = dt.datetime(year, month, day, 12, 45)
elif month==4 and day ==28:
  startT = dt.datetime(year, month, day, 10, 30)
elif month==5 and day ==11:
  startT = dt.datetime(year, month, day, 12, 40)
elif month==9 and day ==11:
  startT = dt.datetime(year, month, day, 10, 30)
elif month==9 and day ==17:
  startT = dt.datetime(year, month, day, 9, 0)
print('startT = ',startT)

for i in range(int(endtime*3600/delt+1)):
  sec = int(i*delt)
  Time.append(startT + dt.timedelta(seconds = sec))
Time = np.array(Time)
print('shape Time = ',np.shape(Time)[0])
#----------------------------------------------------------------------------------------------------------
nucrate = np.array(pd.read_csv(file[0],header=None,delim_whitespace=True))
print('initial shape of nucrate:',np.shape(nucrate))
nucrate = np.reshape(nucrate, (np.shape(Time)[0]-1,nlayers,7))
print('reshaped nucrate array:',np.shape(nucrate))

layers = np.arange(1,nlayers+1,1)
#for i in range(nlayers):
#  ax = plt.gca()
fig, ax = plt.subplots()
FN = np.nanmean(nucrate[:,:,0],axis=0)
fn_ricco = np.nanmean(nucrate[:,:,1],axis=0)/FN
fn_dunne = np.nanmean(nucrate[:,:,2],axis=0)/FN
fn_bn = np.nanmean(nucrate[:,:,3],axis=0)/FN
fn_tn = np.nanmean(nucrate[:,:,4],axis=0)/FN
fn_bi = np.nanmean(nucrate[:,:,5],axis=0)/FN
fn_ti = np.nanmean(nucrate[:,:,6],axis=0)/FN

print('fn_ricco =',fn_ricco)
print('fn_dunne =',fn_dunne)
print('fn_bn =',fn_bn)
print('fn_tn =',fn_tn)
print('fn_bi =',fn_bi)
print('fn_ti =',fn_ti)



fig = plt.gcf()
fig.set_size_inches(4,8)
#x = np.linspace(0,len(FN),len(FN))
#plt.fill_between(layers,fn_bn,fn_bi)
#ax.stackplot(fn_ricco,layers)
#ax.stackplot(fn_dunne,layers)
#ax.stackplot(fn_bn,layers)
#ax.stackplot(fn_tn,layers)
#ax.stackplot(fn_bi,layers)
#ax.stackplot(fn_ti,layers)
#plot_lines.append([l1,l2,l4,l5,l6,l7])


plt.plot(fn_ricco,layers,label='Organic')
plt.plot(fn_dunne,layers,label='Inorganic')
plt.plot(fn_bn,layers,label='Binary-neutral')
plt.plot(fn_tn,layers,label='Ternary-neutral')
plt.plot(fn_bi,layers,label='Binary-Ion')
plt.plot(fn_ti,layers,label='Ternary-Ion')
plt.legend()
#handles, labels = ax.get_legend_handles_labels()
#plot_lines2.append([labels])

#plot_lines = np.array(plot_lines)
#plot_lines2 = np.array(plot_lines2)
#print('plt_lines2 =',plot_lines2[0,0,0])
#print('l[0] for l in plot_lines =',(l[0] for l in plot_lines))

#legend1 = plt.legend(plot_lines[0], ["Total", "Org.", "BN","TN","BI","TI"], loc=1)
#plt.legend([l[0] for l in plot_lines], plot_lines2[0,0], loc=2)
#plt.gca().add_artist(legend1)

plt.xlabel('Nucrate fraction')
plt.ylabel('Layer')
plt.title('Nucleation Rate - %s/%s/%s'%(month,day,year)) 
#plt.yscale('log')
#plt.grid(True)
#plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.show()
  #fig.savefig('%s_FN.png'%file1[0:8],bbox_inches='tight')
