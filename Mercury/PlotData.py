import matplotlib.pyplot as plt
import numpy as np

###########################
##Read Files###############
###########################
from os import walk
files_aux = []
for (dirpath, dirnames, filenames) in walk("."):
    files_aux.extend(filenames)
    break
files = [x for x in files_aux if ".aei" in x]

#'lines' stores the lines from all files (2D vector)
lines=[]
lines_to_skip=4
for i in files:
    f = open(i, 'r')
    for j in range(lines_to_skip):
        next(f) #skip line
    lines.append(f.readlines())
    f.close()

Nlines=sum(1 for line in lines[0])-lines_to_skip #the number of lines is the same in all files
    
varnames=["Time","Semi-major axis","Eccentricity","Inclination","Pericenter","Longitude of ascending node","Mean anomaly","Mass"]
lines_splitted=[[0 for x in range(Nlines)] for y in range(len(files))]
for f in range(len(files)):
    for n in range(Nlines):
        lines_splitted[f][n]=lines[f][n].split()


###########################
##Store Variables##########
###########################
planet_index=[files.index("JUPITER.aei"),
              files.index("SATURN.aei"),
              files.index("URANUS.aei"),
              files.index("NEPTUNE.aei")] #choose planets which variables we want to show
planet_names=["Jupiter","Saturn","Uranus","Neptune"]
if len(planet_index) != len(planet_names): print("ERROR!")

time=[[0 for x in range(Nlines)] for y in range(len(files))]
ecc =[[0 for x in range(Nlines)] for y in range(len(files))]

for i,ii in zip(planet_index,range(len(planet_index))): #order variables
    for j in range(Nlines):
        time[ii][j]=float(lines_splitted[i][j][0])
        ecc[ii][j]=float(lines_splitted[i][j][2])

###########################
##Plotting#################
###########################
fig = plt.figure(figsize=(12,5)) 
ax = plt.subplot(111)
for i in range(len(planet_index)):
    plt.plot(np.array(time[i]),np.array(ecc[i]),label=planet_names[i]) 
ax.set_xlabel(varnames[0])
ax.set_ylabel(varnames[2])
plt.legend();
fig.savefig("PlotData_eccentricities.png")  
