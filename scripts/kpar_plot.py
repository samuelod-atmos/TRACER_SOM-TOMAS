import numpy as np
import sys
from matplotlib import pyplot as plt
import matplotlib as mpl

ibins = 40

fig  = plt.gcf()

fig.set_size_inches(9,3)

A = 2.0E-3    #nm/s
xk = np.zeros(ibins+1) 
xk[0]=1E-21*2**-10 
for k in range(1,ibins+1):
   xk[k] = xk[k-1]*2.
pdens=1400. # fixed density for simplicity
xkm=np.sqrt(xk[:-1]*xk[1:])
Dp=((6.*xkm/pdens/np.pi)**(1.0/3.0))*1E9 # [m] average particle diameter of bin
#Dp_lower=(6.*xk[:-1]/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin
#Dp_upper=(6.*xk[1:]/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin

#print('Dp=',Dp)
kflat = 6.9E-5
#kflat = 1.3E-4

kpar = []
for i in range(len(Dp)):
  if i < 5:
    kpar.append(float(A/Dp[4]+kflat))
  else:
    kpar.append(float(A/Dp[i]+kflat))

kpar = np.array(kpar)


plt.semilogx(Dp,kpar,c='k',label='kflat+A/Dp')

#plt.scatter(80.0, 1.51579e-4, marker = '*')
#plt.scatter(150.0, 1.28315e-4, marker = '*')
#plt.scatter(20.0, 4.80041e-4, marker = '*')


A = 4.0E-3    #nm/s
xk = np.zeros(ibins+1) 
xk[0]=1E-21*2**-10 
for k in range(1,ibins+1):
   xk[k] = xk[k-1]*2.
pdens=1400. # fixed density for simplicity
xkm=np.sqrt(xk[:-1]*xk[1:])
Dp=((6.*xkm/pdens/np.pi)**(1.0/3.0))*1E9 # [m] average particle diameter of bin
#Dp_lower=(6.*xk[:-1]/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin
#Dp_upper=(6.*xk[1:]/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin

#print('Dp=',Dp)
kpar = []
for i in range(len(Dp)):
  if i < 11:
    #print('Dp[i]=',Dp[i])
    kpar.append(float(A/Dp[11]))
  else:
    kpar.append(float(A/Dp[i]))

kpar = np.array(kpar)

#plt.semilogx(Dp,kpar*60.0,c='r',label='A=4E-3')
#ticks = [6e-5,8e-5,1e-4,2e-4,3e-4,4e-4,5e-4]

plt.yscale('log')

ax = plt.gca()
#ax.ticklabel_format(style='sci', scilimits=(-5,-4), axis='y')
#ax.set_yticks(ticks)
#ax.set_yticklabels(ticks)
#ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('$10^{%2.1f}$'))
#ax.yaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.1e'))

plt.ylabel('K_par [$ s^{-1} $]')
plt.xlabel('Diameter [nm]')
plt.legend()
plt.grid()
#plt.ylim(5e-4,1.3e-3)
#plt.ylim(0,0.8)
plt.xlim(0,800)
plt.show()

fig.savefig('Kpar.png')
