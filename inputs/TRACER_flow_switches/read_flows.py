import numpy as np
import datetime as dt
import sys
from netCDF4 import Dataset 
from matplotlib import pyplot as plt


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
startD = dt.datetime(2022,7,20,0)
endD = dt.datetime(2022,8,31,0)
days = int((endD-startD).total_seconds()/3600/24)
#print('number of days =',days)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
date = startD
aadt = 10
interp_s = np.arange(0,24*3600,aadt)

temp_date = []
temp_date.append(startD)

for i in np.arange(1,len(interp_s),1):
  #print('interp_s[i]=',interp_s[i])
  temp_date.append(startD+dt.timedelta(seconds=int(interp_s[i])))
temp_date = np.array(temp_date)

#-------------------------------
f1 = open('Interp_flows.txt','w')
#-------------------------------

total_T = []

for v in range(days):
  print('running:',date)

  switchfile = 'UCI_%s%s%s.cag'%(str(date.year).zfill(2)[2:],str(date.month).zfill(2),str(date.day).zfill(2))
  
  f2 = open(switchfile,'r')
   
  switch,dates,seconds =[],[],[]
  for line in f2.readlines():
    spl_line = line.split(',')
    switch.append(int(spl_line[-1]))
    dates.append(dt.datetime.strptime('%s/%s/%s '%(str(date.year).zfill(4),str(date.month).zfill(2),str(date.day).zfill(2))+spl_line[0][:-3],'%Y/%m/%d %H:%M:%S'))
  
  dates = np.array(dates) - dt.timedelta(hours=1) #Already in CDT? CDT -> CST

  for i in range(len(dates)):
    seconds.append((dates[i]-dates[0]).total_seconds())

  switch = np.array(switch)
  seconds = np.array(seconds)
  interp_flows = np.interp(interp_s,seconds,switch)
  
  for i in range(len(interp_flows)):
    if interp_flows[i] == 0.0 or interp_flows[i] == 1.0:
      interp_flows[i] = interp_flows[i]
    else:
      interp_flows[i] = interp_flows[i-1]
 
  for j in range(len(interp_s)):
    f1.write('%s, %s\n'%(str(temp_date[j]),str(interp_flows[j])))
  #sys.exit('give up now')
 
  f2.close()
  date = date + dt.timedelta(days=1)
  temp_date = temp_date + dt.timedelta(days=1)

f1.close()
