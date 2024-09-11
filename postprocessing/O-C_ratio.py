import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl

boxvol = 10000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 264
srtorglast = srtorg1+iorg
R = 8.314
TEMP = 294
#file = '1.1_Cstar0.001_T292.0_h2so41.00e+07_NH31.00e+02_05.0_SAPRCspname.npy'
#file = '1.1_Cstar0.001_T292.0_h2so41.00e+07_NH31.00e+02_S05.0_APRCgasconc.npy'
#file1 = '051120160.001_T298.0_h2so41.00e+07_NH34.93e+09_10.0_SAPRCspname.npy'
#file2 = '051120160.001_T298.0_h2so41.00e+07_NH34.93e+09_10.0_SAPRCgasconc.npy'
#file = '091720160.001_T296.0_h2so41.00e+07_NH34.96e+09_10.0_Mk.npy'
#file1 = '042720160.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_OH.npy'
#file2 = '042820160.001_T293.0_h2so41.00e+07_NH35.01e+09_10.0_SAPRCgasconc.npy'
#file = '042820160.001_T293.0_h2so41.00e+07_NH35.01e+09_10.0_Mk.npy'

file1 = '04272016_Y-SIVOC0.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_soa_o2c_som.npy'
file2 = '04272016_Y-SIVOC0.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_soa_o2c.npy'
file3 = '04272016_Y-SIVOC0.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_o2c.npy'

#file1 = '042720160.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_soa_o2c_som.npy'
#file2 = '042720160.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_soa_o2c.npy'
#file3 = '042720160.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_o2c.npy'
#file1 = '042820160.001_T293.0_h2so41.00e+07_NH35.01e+10_10.0_FN.npy'
#file1 = '051120160.001_T298.0_h2so41.00e+07_NH34.93e+10_10.0_FN.npy'
#file1 = '091120160.001_T293.0_h2so41.00e+07_NH35.01e+10_10.0_FN.npy'  
#file1 = '091720160.001_T296.0_h2so41.00e+07_NH34.96e+10_10.0_FN.npy'

fid1 = np.load(file1) #,allow_pickle=True)
print(np.shape(fid1))

fid2 = np.load(file2) #,allow_pickle=True)
fid3 = np.load(file3) 

OC1 = fid1[0,:,0]
OC2 = fid1[0,:,1]
OC3 = fid1[0,:,2]
OC4 = fid1[0,:,3]
OC5 = fid1[0,:,4]
OC6 = fid1[0,:,5]
OC7 = fid1[0,:,6]

OCtot = fid2[0]
OCtot2 = fid3[0]
OCmean = np.mean(fid1[0],axis=1)
print(np.shape(OCmean))
print(OCmean[0])

fig = plt.gcf()
fig.set_size_inches(10,6)
x = np.linspace(0,len(OCtot),len(OCtot))
#plt.plot(x/360,OC1,label='BNZSOMG')
#plt.plot(x/360,OC2,label='TOLSOMG')
#plt.plot(x/360,OC3,label='XYLSOMG')
#plt.plot(x/360,OC4,label='ISPSOMG')
#plt.plot(x/360,OC5,label='TRPSOMG')
#plt.plot(x/360,OC6,label='IVOSOMG')
#plt.plot(x/360,OC7,label='SVOSOMG')
plt.plot(x/360,OCtot,label='soa O:C')
#plt.plot(x/360,OCmean,'k',label='Mean SOM O:C')
#plt.plot(x/360,OCtot2,'r',label='O:C')
plt.legend(loc='best')
plt.xlabel('Time [hours]')
plt.ylabel('O/C')
plt.title('O:C ratio - %s/%s/2016'%(file1[0:2],file1[2:4])) 
plt.grid(True)
#plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.show()
#fig.savefig('%s_O2C_v1.png'%file1[0:8],bbox_inches='tight')
