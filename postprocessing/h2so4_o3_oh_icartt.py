import icartt 
import numpy as np
import datetime as dt
import pandas as pd
import sys


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
ict.dateOfCollection = dt.datetime.utcnow().timetuple()[:3]
ict.dateOfRevision = dt.datetime.utcnow().timetuple()[:3]

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

ict.dependentVariables["H2SO4"] = icartt.Variable(
        "H2SO4", "molec/cm^3", "H2SO4", "H2SO4", scale=1.0, miss=-9999999
        )

ict.dependentVariables["OH"] = icartt.Variable(
        "OH", "molec/cm^3", "OH", "OH", scale=1.0, miss=-9999999
        )

ict.dependentVariables["ozone"] = icartt.Variable(
        "ozone", "ppbv", "ozone", "ozone", scale=1.0, miss=-9999999
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

gc_file = '%s/20220801_%s_vwl1_pwl1_hr1.44e+02_nh35000_orgfn%s_inorg%s_db%s_gc.dat'%(output_dir,identify,orgnuc,inorgnuc,db[0])

df_saprcgc = pd.read_csv(gc_file,header=None,delim_whitespace=True,)

saprc_gas = np.array(df_saprcgc)

sulf = saprc_gas[:,1]
sulf = sulf/boxvol*1000.0/98.0*6.022e23

time = np.arange(0,len(sulf),1)
#time2 = np.arange(0,len(sulf),1)


year = int(gc_file[11:15])
month = int(gc_file[15:17])
day = int(gc_file[17:19])
startT = dt.datetime(year,month,day,11)
print(startT)

date = []
date.append(startT)
#time = np.arange(0,len(sulf),1)

for i in range(len(time)-1):
  #print(Time[i+1])
  startT = startT + dt.timedelta(seconds=10)
  date.append(startT)

date = np.array(date)


#==================================================================================

oh_fid = open('../inputs/20220801_%s_OH'%identify,'r')

OH = []
for line in oh_fid.readlines():
 OH.append(float(line))

OH = np.array(OH)

#OH = signal.savgol_filter(OH,101,2)
OH = OH[:len(sulf)]
OH = smoothdist(OH)

#==================================================================================

o3_fid = open('../inputs/20220801_%s_o3'%identify,'r')

O3 = []
for line in o3_fid.readlines():
 O3.append(float(line))

ozone = np.array(O3)

#OH = signal.savgol_filter(OH,101,2)
ozone = ozone[:len(sulf)]

#==================================================================================

#data_all = np.array([date, sulf, OH, ozone])
#data_all = np.transpose(data_all)

#print(np.shape(data_all))

#ict.data.add(data_all)

#print([x for x in ict.variables])

# Note 2: evenfor single lines, you still need to make it an array!

# Note 3: multiple data lines can be added in bulk!
#                 ivar  dvar1 dvar2       ivar  dvar1 dvar2      ...
#data = np.array([(13.4, 14.0, 2.348925e5), (14.1, 14.9, 2.3425634e5)])

#sulf = sulf*10.0
#ict.data.add(sulf)

# Now, look at it in ICARTT form:
#ict.write()

# And you could simply write to file:
#with open('o3_oh_h2so4.ict', 'w') as f:
#   ict.write(f=f)



f = open('o3_oh_h2so4.ict', 'a')

for i in range(len(date)):
#for i in range(20):
  #temp = []
  #temp.append(dt.datetime.strftime(date[i],format='%Y/%m/%d %H:%M:%S'))
  f.write(dt.datetime.strftime(date[i],format='%Y/%m/%d %H:%M:%S'))
  f.write(', %s, %s, %s'%(str(sulf[i]), str(OH[i]), str(ozone[i])))
  #for j in range(nbins):
  #  f.write(', '+str(Y[i,j]))
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



