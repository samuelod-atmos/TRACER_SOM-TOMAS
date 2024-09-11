
import numpy as np
import datetime as dt
from functions import g1,g2,g3,h,h2,closest,smoothdist
from scipy.optimize import curve_fit
import pygsheets as pyg
import sys
from matplotlib import pyplot


gc = pyg.authorize(service_file='../inputs/SOMTOMAS-Sam-GoogleSheetAccess.json')

############################################################################################################

gsh = gc.open('Injection')

df_1 = gsh.worksheet_by_title(title='Sheet').get_as_df()

temp = df_1.to_numpy()

print(len(temp))
#dates = temp[:,0]
sec = np.array(temp[:,1],dtype='float64')
N = np.array(temp[:,2],dtype='float64')
Dp = np.array(temp[:,3],dtype='float64')
sigma = np.array(temp[:,4],dtype='float64')

sec = sec - sec[0]
print(sec[-1]/3600./24)

startT = dt.datetime(2022,7,23,21,4)

dates = []

for i in range(len(sec)):
  dates.append(startT + dt.timedelta(seconds=sec[i]))

dates = np.array(dates)
print('dates=',dates)

endlist = []
endlist.append(dates[0])
#beginlist = []
for i in range(len(sec)-1):
  diff = sec[i+1]-sec[i]
  if diff > 3000:
    #print(diff,dates[i])
    endlist.append(dates[i])
    endlist.append(dates[i+1])

#print('endlist=',endlist)
#sys.exit()

#print('beginlist=',beginlist)
f7 = open('aersol_injections','w')

start_t = endlist[0]
end_t = endlist[-1]

length = int((dates[-1]-dates[0]).total_seconds())
print(sec[-1],length)

og_sec = np.arange(sec[0],sec[-1],10)
print(len(og_sec))

print(len(og_sec),len(sec),len(N))
interp_N = np.interp(og_sec,sec,N)
interp_Dp = np.interp(og_sec,sec,Dp)
interp_sig = np.interp(og_sec,sec,sigma)
print(len(interp_N))

og_date = startT

stat = 1
cntr = 0

#for i in range(500):
for i in range(len(interp_N)):
  if og_date >= endlist[cntr] and og_date < endlist[cntr+1] and stat==1:
    f7.write('%s %s %s %s \n'%(str(interp_N[i]),str(interp_Dp[i]),str(interp_sig[i]),str(og_date)))
    #print('endlist[cntr] =',endlist[cntr],endlist[cntr+1])
    #print('og_date =',og_date)
    #print('stat =',stat)
  elif og_date >= endlist[cntr] and og_date < endlist[cntr+1] and stat==0:
    f7.write('0.0 0.0 0.0 %s \n'%og_date)
  elif og_date > endlist[cntr+1]:
    cntr = cntr + 1
    print('endlist[cntr] =',endlist[cntr])
    print('og_date =',og_date)
    print('stat =',stat)
    if stat==1:
      stat=0
    elif stat==0:
      stat=1
  og_date = og_date + dt.timedelta(seconds=10)



