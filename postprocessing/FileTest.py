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

file1 = '04272016_high-sesq0.001_T294.0_nlay3.00e+00_NH32.00e+03_05.0_MW.npy'
fid1 = np.load(file1)
print(np.shape(fid1))
