import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import sys
import pandas as pd
import datetime as dt
import matplotlib.dates as mdates 


output_dir = '../outputs/'
#identify = '01HOM'
identify = 'debug'

delt = 300.0

files = ['%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn1_inorg1_db1e-15_fn.dat'%(output_dir,identify)]

for file in files:  
  year = int(file[12:16])
  month = int(file[16:18])
  day = int(file[18:20])
  startT = dt.datetime(year,month,day,11)
  print('Year = ',year,'Month = ', month,'Day = ', day) 
   
  
  nucrate = np.array(pd.read_csv(file,header=None,delim_whitespace=True))
  print('shape of nucrate:',np.shape(nucrate))
 
  #sys.exit('Happy birthday!')
 
  Time = []
  for i in range(int(len(nucrate))):
    sec = int(i*delt)
    Time.append(startT + dt.timedelta(seconds = sec))
  Time = np.array(Time)
 
  #print(len(Time))
  #sys.exit('Happy birthday!')
  
  colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:grey','tab:olive','tab:cyan']
  plot_lines = []
  plot_lines2 = []
  
  ax = plt.gca()
  FN = nucrate[:,0]
  fn_ricco = nucrate[:,1]
  fn_dunne = nucrate[:,2]
  fn_bn = nucrate[:,3]
  fn_tn = nucrate[:,4]
  fn_bi = nucrate[:,5]
  fn_ti = nucrate[:,6]
  
  fig = plt.gcf()
  fig.set_size_inches(10,6)
  x = mdates.date2num(Time)
#    l2, = plt.plot(x/360,fn_ricco,color=colors[i],linestyle = '--')
##    l3, = plt.plot(x/360,fn_dunne,color=colors[i],linestyle = '-.')
#    l4, = plt.plot(x/360,fn_bn,color=colors[i],linestyle = '-.')
#    l5, = plt.plot(x/360,fn_tn,color=colors[i],linestyle = ':')
#    l6, = plt.plot(x/360,fn_bi,color=colors[i],linestyle = '-')
#    l7, = plt.plot(x/360,fn_ti,color=colors[i],linestyle = (0,(1,10)))
  l1, = plt.plot(x,FN,color='k')
  l2, = plt.plot(x,fn_ricco,color='g', linestyle = '--')
  l3, = plt.plot(x,fn_dunne,color='r',linestyle = '-.')
  #l4, = plt.plot(x,fn_bn,linestyle = '-.')
  #l5, = plt.plot(x,fn_tn,linestyle = ':')
  #l6, = plt.plot(x,fn_bi,linestyle = '-')
  #l7, = plt.plot(x,fn_ti,linestyle = (0,(1,10)))
  #  plt.legend(loc='best')
  
  plot_lines.append([l1,l2,l3])
  #plot_lines.append([l3])
  #plot_lines.append([l1,l2,l4,l5,l6,l7])
  
  handles, labels = ax.get_legend_handles_labels()
  plot_lines2.append([labels])
  
  plot_lines = np.array(plot_lines)
  plot_lines2 = np.array(plot_lines2)
  
  #legend1 = plt.legend(plot_lines[0], ["Total", "Org.", "BN","TN","BI","TI"], loc=1)
  legend1 = plt.legend(plot_lines[0], ["Total", "Org.", "InOrg"], loc=1)
  plt.legend([l[0] for l in plot_lines], plot_lines2[0,0], loc=2)
  plt.gca().add_artist(legend1)
  
  plt.xlabel('Date')
  plt.ylabel('Nucleation Rate [#/cm^3/s]')
  plt.title('Nucleation Rate - %s/%s/2016'%(month,day)) 
  plt.grid(True)
  plt.yscale('log')
  plt.ylim(1e-6,1000)
  #plt.ylim(0,10)

  ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
  #plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
  plt.show()
