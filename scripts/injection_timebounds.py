import datetime as dt
import numpy as np


time_bounds = np.array([[
dt.datetime(2022,7,31,21,30),
dt.datetime(2022,7,31,21,30) + dt.timedelta(hours=8)],

[dt.datetime(2022,8,1,22,36),
dt.datetime(2022,8,1,22,30) + dt.timedelta(hours=8)],

[dt.datetime(2022,8,2,22,11),
dt.datetime(2022,8,2,22,11) + dt.timedelta(hours=8)],

[dt.datetime(2022,8,3,22,51),
dt.datetime(2022,8,3,22,51) + dt.timedelta(hours=8)],

[dt.datetime(2022,8,4,22,54),
dt.datetime(2022,8,4,22,54) + dt.timedelta(hours=8)],

#[dt.datetime(2022,8,5,11,15),
#dt.datetime(2022,8,5,11,15) + dt.timedelta(hours=7)],

[dt.datetime(2022,8,5,17,40),
dt.datetime(2022,8,5,17,40) + dt.timedelta(hours=8)],

[dt.datetime(2022,8,6,22,14),
dt.datetime(2022,8,6,22,14) + dt.timedelta(hours=8)],

[dt.datetime(2022,8,7,21,46),
dt.datetime(2022,8,7,21,46) + dt.timedelta(hours=8)],

[dt.datetime(2022,8,8,21,50),
dt.datetime(2022,8,8,21,50) + dt.timedelta(hours=8)],

[dt.datetime(2022,8,9,22,31),
dt.datetime(2022,8,9,22,31) + dt.timedelta(hours=7)]
    ])

print(np.shape(time_bounds))

startd = time_bounds[0][0]
endd = time_bounds[-1][-1]
date_step = startd
print(startd,endd)

length = int((endd-startd).total_seconds())
seconds = np.arange(0,length,10)

f1 = open('inject_aerosol','w')

for i in range(len(seconds)):
  if date_step >= time_bounds[0][0] and date_step <= time_bounds[0][-1]:
    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
  elif date_step >= time_bounds[1][0] and date_step <= time_bounds[1][-1]:
    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
  elif date_step >= time_bounds[2][0] and date_step <= time_bounds[2][-1]:
    f1.write('1000.0 0.40 1.4 %s \n'%(date_step))
  elif date_step >= time_bounds[3][0] and date_step <= time_bounds[3][-1]:
    f1.write('1000.0 0.40 1.4 %s \n'%(date_step))
  elif date_step >= time_bounds[4][0] and date_step <= time_bounds[4][-1]:
    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
  elif date_step >= time_bounds[5][0] and date_step <= time_bounds[5][-1]:
    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
  elif date_step >= time_bounds[6][0] and date_step <= time_bounds[6][-1]:
    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
  elif date_step >= time_bounds[7][0] and date_step <= time_bounds[7][-1]:
    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
  elif date_step >= time_bounds[8][0] and date_step <= time_bounds[8][-1]:
    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
  elif date_step >= time_bounds[9][0] and date_step <= time_bounds[9][-1]:
    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
#  elif date_step >= time_bounds[10][0] and date_step <= time_bounds[10][-1]:
#    f1.write('500.0 0.25 1.01 %s \n'%(date_step))
#  elif date_step >= time_bounds[11][0] and date_step <= time_bounds[11][-1]:
#    f1.write('1000.0 0.03 1.01 %s \n'%(date_step))
  else:
    f1.write('0.0 0.0 0.0 %s \n'%(date_step))

  date_step = date_step + dt.timedelta(seconds=10)


f1.close()




