import icartt 
import numpy as np
import datetime
import pandas as pd
import sys
import datetime as dt

#===========================================================================================================
def smoothdist(dist):
  sdist=np.empty(dist.shape)
  sdist[0]=dist[0]*0.75 + dist[1]*0.25
  sdist[1:-1]=dist[:-2]*0.25 + dist[1:-1]*0.5 + dist[2:]*0.25
  sdist[-1]=dist[-2]*0.25 + dist[-1]*0.75
  return sdist


#===========================================================================================================
output_dir = '../outputs'
save_png = False 
#save_png = True

boxvol = 2000000.0

identify = 'A2e-3'
db = [1E-15]
orgnuc = 1
inorgnuc = 0
nbins = 40


xk = np.zeros(nbins+1) 
xk[0]=1E-21*2**-10 
for k in range(1,nbins+1):
   xk[k] = xk[k-1]*2.
pdens=1400. # fixed density for simplicity
xkm=np.sqrt(xk[:-1]*xk[1:])
Dp=(6.*xkm/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin
Dp_lower=(6.*xk[:-1]/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin
Dp_upper=(6.*xk[1:]/pdens/np.pi)**(1.0/3.0)          # [m] average particle diameter of bin
Dp = Dp*1e9

for i in range(len(Dp)):
  print(Dp[i])
sys.exit()


BinsE = np.log10(Dp_upper/Dp_lower)
#===========================================================================================================

# ------------------------------------------------------
# Phase 1: define file format, properties and variables
# ------------------------------------------------------

ict = icartt.Dataset(format=icartt.Formats.FFI1001)

ict.PIName = "O'Donnell, Samuel"
ict.PIAffiliation = "Colorado State University"
ict.dataSourceDescription = "Model Data"
#ict.missionName = "MBEES"
# to simplify dates and avoid time zone issues, these dates are simple 3 item lists [YYYY, MM, DD]
ict.dateOfCollection = datetime.datetime.utcnow().timetuple()[:3]
ict.dateOfRevision = datetime.datetime.utcnow().timetuple()[:3]

ict.dataIntervalCode = [0]

ict.independentVariable = icartt.Variable(
        "Time_CST",
        "Time in CST (UTC-6)",
        "Time_CST",
        "Time_CST",
        vartype=icartt.VariableType.IndependentVariable,
        scale=1.0,
        miss=-9999999,
        )

#ict.dependentVariables["Time_Stop"] = icartt.Variable(
#        "Time_Stop",
#        "seconds_from_0_hours_on_valid_date",
#        "Time_Stop",
#        "Time_Stop",
#        scale=1.0,
#        miss=-9999999,
#        )


for i in range(nbins):
  ict.dependentVariables["NSD%i"%(i+1)] = icartt.Variable(
      "NSD%i"%i,"cm-3","particlenumbersizedistformobilitydiameter%4.1f"%Dp[i], "", scale=1.0, miss=-9999999
          )


# Normal and Special Comments

# note: all comments can be multi-line per standard.
# To ensure portability the decision was made to represent them as lists,
# with each list item representing a line.

# E.g., Special Comments are simple lists, which we can append to:
#ict.specialComments.append("Some comments on this dataset:")
#ict.specialComments.append("They are just examples!")
#ict.specialComments.append("Adapt as needed.")

# Normal Comments are separated into freeform and (required) keyword comments.

# Freeform comments are, just like special comments, a list with one line per entry
#ict.normalComments.freeform.append("free comment line 1")
#ict.normalComments.freeform.append("free comment line 2")

# Keywords are mandatory, all need to exist, and default to N/A
# they can be set as follows:
ict.normalComments.keywords["PI_CONTACT_INFO"].append(
        "Samuel O'Donnell, Colorado State University"
        )
ict.normalComments.keywords["PI_CONTACT_INFO"].append(
        "samuelod@colostate.edu"
        )
#ict.normalComments.keywords["PLATFORM"].append("ICARTT")
#ict.normalComments.keywords["PROJECT_INFO"].append(
#        "A format reader/writer for ICARTT files"
#        )
# ... and so forth

# note for revisions: we assume you take care of the required documentation of past versions
# and setting the correct date for the current revision (ict.dateOfRevision, see above)
#ict.normalComments.keywords["REVISION"].append("R1")
#ict.normalComments.keywords["REVISION"].append("R1: current status")
#ict.normalComments.keywords["REVISION"].append("R0: early beta")

ict.endDefineMode()

# ------------------------------------------------------
# Phase 2: after ending define mode, add data
# ------------------------------------------------------

# all data are stored as NumPy arrays, and need to be provided as such.


#                 ivar  dvar1 dvar2
#data = np.array([(15.4, 15.0, 5.24524952903484e5)])
#ict.data.add(data)

# Note 1: you are responsible to ensure that the order of elements in a data line
# corresponds to variable listing below:

#==================================================================================


rname = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_noconc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])

df_no = np.array(pd.read_csv(rname,header=None, delim_whitespace=True))

number_conc = df_no[:,1:]
Y = (number_conc[:,:])/BinsE[:]


year = int(rname[11:15])
month = int(rname[15:17])
day = int(rname[17:19])
startT = dt.datetime(year,month,day,11)
print(startT)

date = []
date.append(startT)
time = np.arange(0,len(Y),1)

for i in range(len(time)-1):
  #print(Time[i+1])
  startT = startT + dt.timedelta(seconds=10)
  date.append(startT)

date = np.array(date)

#==================================================================================

#for i in range(len(time)):
#  ict.data.add(np.array([time[i],time2[i],Y[i]]))


#data_all = np.empty([len(date),nbins+1], dtype=object)
#data_all = []
#
#f = open('SOMTOMAS_sizedist.ict', 'w')
#
##for i in range(len(date)):
#for i in range(20):
#  temp = []
#  temp.append(str(date[i]))
#  for j in range(nbins):
#    temp.append(Y[i,j])
#  temp.append('\n')
#  #data_all.append(temp)
#  #data_all[i,0] = date[i].timetuple()[:6]
#  #data_all[i,0] = str(date[i])
#  #data_all[i,1] = time2[i]
#  #data_all[i,1:] = Y[i]
#  f.write(str(temp))
#  f.write('\n')
#  #ict.data.add(data_all[i])
#
#f.close()
##data_all = np.array(data_all)
#data_all = np.transpose(data_all)
#print(np.shape(data_all))
#sys.exit()

#ict.data.add(data_all)

#print([x for x in ict.variables])

# Note 2: evenfor single lines, you still need to make it an array!

# Note 3: multiple data lines can be added in bulk!
#                 ivar  dvar1 dvar2       ivar  dvar1 dvar2      ...
#data = np.array([(13.4, 14.0, 2.348925e5), (14.1, 14.9, 2.3425634e5)])

#sulf = sulf*10.0
#ict.data.add(date)

# Now, look at it in ICARTT form:
#ict.write()

# And you could simply write to file:
#with open('SOMTOMAS_sizedist.ict', 'w') as f:
#   ict.write(f=f)


#data_all = np.empty([len(date),nbins+1], dtype=object)
#data_all = []


f = open('SOMTOMAS_sizedist.ict', 'a')

for i in range(len(date)):
#for i in range(20):
  #temp = []
  #temp.append(dt.datetime.strftime(date[i],format='%Y/%m/%d %H:%M:%S'))
  f.write(dt.datetime.strftime(date[i],format='%Y/%m/%d %H:%M:%S'))
  for j in range(nbins):
    f.write(', '+str(Y[i,j]))
    #temp.append(Y[i,j])
  #temp = np.array(temp)
  #temp.append('\n')
  #data_all.append(temp)
  #data_all[i,0] = date[i].timetuple()[:6]
  #data_all[i,0] = str(date[i])
  #data_all[i,1] = time2[i]
  #data_all[i,1:] = Y[i]
  #f.write(f"\n{str(temp)}")
  f.write('\n')
  #ict.data.add(data_all[i])

f.close()



