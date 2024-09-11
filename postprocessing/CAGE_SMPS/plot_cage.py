import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 
import sys
import matplotlib.ticker as ticker


low = mdates.date2num(dt.datetime(2022,8,1,11,0))#-dt.timedelta(hours=6))
up = mdates.date2num(dt.datetime(2022,8,7,11,0))#-dt.timedelta(hours=6))


Bins = []
bin_data = 'PSD_Dp.txt'
bin_fid = open(bin_data, 'r')
for line in bin_fid.readlines():
  #     spl_line= line.split('  ')
  # for i in range(len(spl_line)):
  #     print('line=',line)
  Bins.append(float(line))
Bins = np.array(Bins)
bin_fid.close()
print(Bins)
sys.exit()


sizedist = []

data = 'Chamber_PSD.txt'
fid=open(data, 'r')

for line in fid.readlines():

  #print(line)
  #sys.exit()
  spl_line=line.split(' ')
  spl_line=line.split('\t')
  #print(spl_line[-1])
  #sys.exit()
#         time.append(float(spl_line[0]))
#         count=count+1
  temp=[]
  for i in range(len(Bins)):
    spl_line[i] = (float(spl_line[i]))
#         spl_line[i] = float(spl_line[i])
#             spl_line[i+1] = float(spl_line[i+1])
#             if spl_line[i] == -inf:
#                 spl_line[i] = 'NaN' 
    temp.append(float(spl_line[i]))
  sizedist.append(temp)
sizedist = np.array(sizedist)

fid.close()
##############################################

time = []
data = 'Chamber_PSD_time.txt'
fid=open(data, 'r')
for line in fid.readlines():
  time.append(float(line))
fid.close()


date = []
# date.append(dt.datetime(2022,7,15,11,57))
date.append(dt.datetime(1970,1,1,0)+dt.timedelta(seconds=time[0]))

for i in range(len(time)-1):
  date.append(date[-1] + dt.timedelta(seconds = time[i+1]-time[i]))
    
date = np.array(date)- dt.timedelta(hours=6)
x = mdates.date2num(date) #-dt.timedelta(hours=12))

c = plt.pcolormesh(x,Bins*1000., np.log10(np.transpose(sizedist)), cmap='rainbow')

ax = plt.gca()
ax2 = ax.twinx()
fig = plt.gcf()
plt.rcParams.update({'font.size': 11})
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

fig.set_size_inches(16,6)
ax.grid(True)
ax.locator_params(axis='x', nbins=6)
#     ax.set_xlim(low,up)
ax.set_xlim(low,up)
ax.set_ylim(12,600)
# ax.set_ylabel("Dp (nm)", fontsize=22, color='k')
#     ax.set_title("Nano-SMPS %s/%s/%s"%(month,day,year))
ax.set_title("CAGE",fontsize=11)
# ax.set_xlabel("Date",fontsize=22, color='k')
ax.set_ylabel("Dp [nm]",fontsize=11, color='k')
ax.set_yscale('log')

# ax2.plot(x,CS,color='k',linestyle='--')
ax2.set_ylabel('CS [1/s]',fontsize=11)
ax2.set_yscale('log')
ax2.set_ylim(0.0001,)

plt.clim(1,4.3)
cb = plt.colorbar(c,pad=.1, format=ticker.FormatStrFormatter('$10^{%2.1f}$'), label='$ dN/dlog_{10}(D_p) $')
plt.show()
