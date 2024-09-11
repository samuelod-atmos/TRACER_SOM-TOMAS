from pylab import *
import numpy as np 
import sys
import datetime as dt
import matplotlib.dates as mdates 


upper_pres = 70000
nlayers = 20
delt = 10.0

#rhdata = '04272016_QV'
#rhdata = '04282016_QV'
#rhdata = '05112016_QV'
#rhdata = '05142016_QV'
#rhdata = '05162016_QV'
rhdata = '05192016_QV'

year = int(rhdata[4:8])
month = int(rhdata[0:2])
day = int(rhdata[2:4])
print('Year = ',year,'Month = ', month,'Day = ', day) 

#startT = dt.datetime(year, month, day, 9, 20)
#startT = dt.datetime(year, month, day, 8, 0)
#startT = dt.datetime(year, month, day, 12, 0)
#startT = dt.datetime(year, month, day, 9, 45)
startT = dt.datetime(year, month, day, 9, 0)
#startT = dt.datetime(year, month, day, 9, 0)


fid = open(rhdata,'r')

qv = []

for line in fid.readlines():
  spl_line = line.split('  ')
  temp = []
  for i in range(20):
    temp.append(float(spl_line[i]))
  qv.append(temp)
qv = array(qv)

###############################################################
#pres_data = '04272016_SfcPres'
#pres_data = '04282016_SfcPres'
#pres_data = '05112016_SfcPres'
#pres_data = '05142016_SfcPres'
#pres_data = '05162016_SfcPres'
pres_data = '05192016_SfcPres'

fid = open(pres_data,'r')

sfcpres = []

for line in fid.readlines():
  spl_line = line.split('  ')
  sfcpres.append(float(spl_line[0]))
print(shape(sfcpres))

Time = []
for i in range(len(sfcpres)):
  sec = int(i*delt)
  Time.append(startT + dt.timedelta(seconds = sec))
Time = np.array(Time)

#Tdata = '04272016_Temperatures'
#Tdata = '04282016_Temperatures'
#Tdata = '05112016_Temperatures'
#Tdata = '05142016_Temperatures'
#Tdata = '05162016_Temperatures'
Tdata = '05192016_Temperatures'

fid = open(Tdata,'r')

T = []

for line in fid.readlines():
  spl_line = line.split('  ')
  temp = []
  for i in range(20):
    temp.append(float(spl_line[i]))
  T.append(temp)
T = array(T)

Dp_pa = (sfcpres[0] - upper_pres)/nlayers  # Define pressure differential  
pres_lay,temp_lay,pres_lay_edge,Z_lay = np.zeros([nlayers]),np.zeros([nlayers]),np.zeros([nlayers+1]),np.zeros([nlayers])
pres_lay[0] = sfcpres[0] - 0.5*Dp_pa 
pres_lay_edge[0] = sfcpres[0] 

temp_lay = T[0]

for i in range(nlayers-1):
  pres_lay[i+1] = pres_lay[i] - Dp_pa
for i in range(nlayers):
  pres_lay_edge[i+1] = pres_lay_edge[i] - Dp_pa

Z_lay[0] = (287.0*temp_lay[0]/9.8 * np.log(pres_lay_edge[0]/pres_lay_edge[1]))*0.5

for i in range(nlayers-1):
  Z_lay[i+1] = Z_lay[i] + (287.0*temp_lay[i]/9.8 * np.log(pres_lay_edge[i]/pres_lay_edge[i+1]))*0.5 + (287.0*temp_lay[i+1]/9.8 * np.log(pres_lay_edge[i+1]/pres_lay_edge[i+2]))*0.5

print('Z_lay =',Z_lay)

RH = []
for i in range(len(sfcpres)):
  w = qv[i]/(1-qv[i])
  e_s = 611.0*np.exp((17.67*(T[i]-273.15))/(T[i]-29.65))
  w_s = (e_s*287.05)/(461.552*(pres_lay-e_s))
  
  rh_lay = w/w_s
  for j in range(20):
    if (rh_lay[j] > 0.95):
      rh_lay[j] = 0.95
  RH.append(rh_lay)



x = mdates.date2num(Time)
RH = np.array(RH)
print(RH[0])
fig = plt.gcf()
ax = plt.gca()
fig.set_size_inches(6,4)
#c = pcolormesh(x,Z_lay,transpose(RH)*100) #),cmap='GnBu')
c = pcolormesh(x,Z_lay,transpose(T)) #),cmap='GnBu')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
#cb1 = fig.colorbar(c,label='Relative Humidity [%]')
cb1 = fig.colorbar(c,label='Temperature [Kelvin]')
#clim(30,90)
ylabel('Altitude [m]')
xlabel('Time [CDT]')
ax.set_title('%s/%s/2016'%(month,day),fontsize=18) 

show()

fig.savefig('%s-%s-%s_Temperature.png'%(month,day,year),bbox_inches='tight')
