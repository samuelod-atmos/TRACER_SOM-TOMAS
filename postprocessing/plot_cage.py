import numpy as np
import datetime as dt
import matplotlib.dates as mdates 
import pandas as pd 
import sys
import matplotlib.ticker as ticker


def get_smps():

  
  Bins = []
  bin_data = 'CAGE_SMPS/PSD_Dp.txt'
  bin_fid = open(bin_data, 'r')
  for line in bin_fid.readlines():
    #     spl_line= line.split('  ')
    # for i in range(len(spl_line)):
    #     print('line=',line)
    Bins.append(float(line))
  Bins = np.array(Bins)
  bin_fid.close()
  print(Bins)
  #sys.exit()
  
  
  sizedist = []
  
  data = 'CAGE_SMPS/Chamber_PSD.txt'
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
  data = 'CAGE_SMPS/Chamber_PSD_time.txt'
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

  return date,Bins,sizedist
