import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl

boxvol = 10000000.0
srtSO4 = 0
srtorg1 = 1
iorg = 456
srtorglast = srtorg1+iorg
pres = 101325.
R = 8.3145
#file = '1.1_Cstar0.001_T292.0_h2so41.00e+07_NH31.00e+02_05.0_SAPRCspname.npy'
#file = '1.1_Cstar0.001_T292.0_h2so41.00e+07_NH31.00e+02_S05.0_APRCgasconc.npy'
#file1 = '04272016_N-SIVOC0.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_SAPRCspname.npy'
#file2 = '04272016_N-SIVOC0.001_T294.0_h2so41.00e+07_NH34.99e+10_10.0_SAPRCgasconc.npy'
file2 = '04272016_high-sesq0.001_T294.0_nlay3.00e+00_NH32.00e+03_05.0_SAPRCgasconc.npy'
file1 = '04272016_high-sesq0.001_T294.0_nlay3.00e+00_NH32.00e+03_05.0_SAPRCspname.npy'
file3 = '04272016_rearranged0.001_T294.0_h2so41.00e+07_NH32.00e+03_05.0_SAPRCspname.npy'
file4 = '04272016_rearranged0.001_T294.0_h2so41.00e+07_NH32.00e+03_05.0_SAPRCgasconc.npy'
file5 = '04272016_high-sesq0.001_T294.0_nlay3.00e+00_NH32.00e+03_05.0_MW.npy'

layer = 1
what = 'som'
T = 294.
print(T)
layer = layer -1 
fid1 = np.load(file1,allow_pickle=True)
fid2 = np.load(file2,allow_pickle=True)
fid3 = np.load(file3,allow_pickle=True)
fid4 = np.load(file4,allow_pickle=True)
fid5 = np.load(file5)

print(np.shape(fid1))

if what == 'precursors':
  benzindx = int(np.where(fid1=='BENZENE')[0])
  isopindx = int(np.where(fid1=='ISOPRENE')[0])
  toluindx = int(np.where(fid1=='TOLUENE')[0])
  so2indx = int(np.where(fid1=='SO2')[0])
  sulfindx = int(np.where(fid1=='SULF')[0])
  sesqindx = int(np.where(fid1=='SESQTRP')[0])
  terpindx = int(np.where(fid1=='TERPENE')[0])
  trimindx = int(np.where(fid1=='TRIMBNZ')[0])
  xyleindx = int(np.where(fid1=='XYLENE')[0])
  ivocindx = int(np.where(fid1=='IVOC')[0])
  svocindx = int(np.where(fid1=='SVOC')[0])

if what == 'som':
  benzindx = []
  isopindx = []
  toluindx = []
  so2indx =  []
  sulfindx = []
  sesqindx = []
  terpindx = []
  trimindx = []
  xyleindx = []
  ivocindx = []
  svocindx = []
  temporary = []
  string = 'This is a string'
  print('The string = ',string)
  
  for i in np.arange(0,len(fid1)):
    temp = str(fid1[i])
  #  print(temp[0:7],'BNZSOMG')
    if temp[:7] == 'BNZSOMG':
  #    print('Yaassss')
      benzindx.append(i)
      temporary.append(i+100)
    elif temp[0:7] == 'ISOSOMG':
      isopindx.append(i)
    elif temp[0:7] == 'TOLSOMG':
      toluindx.append(i)
    elif temp[0:7] == 'SESSOMG':
      sesqindx.append(i)
    elif temp[0:7] == 'TERSOMG':
      terpindx.append(i)
    elif temp[0:7] == 'TRISOMG':
      trimindx.append(i)
    elif temp[0:7] == 'XYLSOMG':
      xyleindx.append(i)
    elif temp[0:7] == 'IVOSOMG':
      ivocindx.append(i)
    elif temp[0:7] == 'SVOSOMG':
      svocindx.append(i)

molwt = np.mean(fid5[temporary])
print(molwt)
print('Shape of file:',np.shape(fid2))
benz = fid2[:,layer,benzindx]*1e-6*pres/R/T*molwt #(boxvol) 
isop = fid2[:,layer,isopindx]
tolu = fid2[:,layer,toluindx]
so2 = fid2[:,layer,so2indx]
sulf = fid2[:,layer,sulfindx]*1e-6*pres*6.022e23/T/8.3145*1e-6
sesqtrp = fid2[:,layer,sesqindx]
terp = fid2[:,layer,terpindx]
trimeth = fid2[:,layer,trimindx]
xylene = fid2[:,layer,xyleindx]
ivoc = fid2[:,layer,ivocindx]
svoc = fid2[:,layer,svocindx]
print(np.shape(benz))
if what == 'som':
  benz = np.sum(benz,axis=1) 
  isop = np.sum(isop,axis=1) 
  tolu = np.sum(tolu,axis=1) 
  so2 = np.sum(so2,axis=1) 
  sulf = np.sum(sulf,axis=1) 
  sesqtrp = np.sum(sesqtrp,axis=1) 
  terp = np.sum(terp,axis=1)
  trimeth = np.sum(trimeth,axis=1) 
  xylene = np.sum(xylene,axis=1)
  ivoc = np.sum(ivoc,axis=1)
  svoc = np.sum(svoc,axis=1)
  print(np.shape(benz))

print('Shape of fid4',np.shape(fid4))
benz2 = fid4[0,:,benzindx]*1e-6*pres/R/T*molwt 
isop2 = fid4[0,:,isopindx]
tolu2 = fid4[0,:,toluindx]
so22 = fid4[0,:,so2indx]
sulf2 = fid4[0,:,sulfindx]*1e-6*pres*6.022e23/T/8.3145*1e-6
sesqtrp2 = fid4[0,:,sesqindx]
terp2 = fid4[0,:,terpindx]
trimeth2 = fid4[0,:,trimindx]
xylene2 = fid4[0,:,xyleindx]
ivoc2 = fid4[0,:,ivocindx]
svoc2 = fid4[0,:,svocindx]
print(np.shape(benz2))
if what == 'som':
  print('Yassss')
  benz2 = np.sum(benz2,axis=0) 
  isop2 = np.sum(isop2,axis=0) 
  tolu2 = np.sum(tolu2,axis=0) 
  so22 = np.sum(so22,axis=0) 
  sulf2 = np.sum(sulf2,axis=0) 
  sesqtrp2 = np.sum(sesqtrp2,axis=0) 
  terp2 = np.sum(terp2,axis=0)
  trimeth2 = np.sum(trimeth2,axis=0) 
  xylene2 = np.sum(xylene2,axis=0)
  ivoc2 = np.sum(ivoc2,axis=0)
  svoc2 = np.sum(svoc2,axis=0)
  print(np.shape(benz2))
#so2 = so2[0:-10]
#print(so2[-30:-1])
#print(np.shape(benz),np.shape(isop),np.shape(tolu),np.shape(so2),np.shape(sulf))
#print(np.nanmax(benz))
x = np.linspace(0,len(so2),len(so2))
#print(benz)
fig = plt.gcf()
fig.set_size_inches(10,6)
#plt.scatter(x/360,so2*1000,label='SO2')
#plt.plot(x/360,sulf,label='Sulfuric Acid')
plt.plot(x/360,100*(benz-benz2)/benz2,label='BNZSOMG_ratio')
#plt.plot(x/360,benz2*1000,label='BNZSOMG_old')
#plt.plot(x/360,benz*1000,label='BNZSOMG_new')
#plt.plot(x/360,benz*1000,label='Benzene new')
#plt.plot(x/360,benz2*1000,label='Benzene old')
#plt.scatter(x/360,tolu*1000,s=1.0,label='Toluene')
#plt.scatter(x/360,sesqtrp*1000,s=1.0,label='Sesqterp')
#plt.scatter(x/360,terp*1000,s=1.0,label='Terpenes')
#plt.scatter(x/360,trimeth*1000,s=1.0,label='Trimethylbenzene')
#plt.scatter(x/360,xylene*1000,s=1.0,label='M-Xylene')
#plt.scatter(x/360,ivoc*1000,s=1.0,label='IVOC')
#plt.scatter(x/360,svoc*1000,s=1.0,label='SVOC')
plt.title('BNZSOMG (%s/%s/2016)'%(file1[0:2],file1[2:4]))
plt.xlabel('Time [hours]')
#plt.ylabel('$ molec. $ $ cm^{-3} $')
plt.ylabel('% difference (new-old)/old',fontsize=12)
#plt.ylabel('ppb???',fontsize=12)
#plt.yscale('log')
plt.legend(loc='best',markerscale=4.)
plt.show()

#fig.savefig('20160917_GasConc.png',bbox_inches='tight')
#fig.savefig('%s_SO2.png'%file1[0:8],bbox_inches='tight')
