import numpy as np

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

######################################
##Read data files#####################
######################################
Nobjects=2
filename=["saved_data.data","saved_data2.data"]
myfile=[open(filename[0],"r"),open(filename[1],"r")]
file_length=[file_len(filename[0]),file_len(filename[1])]

times=[float((myfile[0].readline()).split()[0]) for x in range(file_length[0])]
myfile[0].seek(0)

#variables store on myfile[0]
ecc=[]
for i in range(Nobjects):
    ecc.append([float(myfile[0].readline().split()[1+i]) for x in range(file_length[0])])
    myfile[0].seek(0)
inc=[]
for i in range(Nobjects):
    inc.append([float(myfile[0].readline().split()[3+i]) for x in range(file_length[0])])
    myfile[0].seek(0)
    
#variables store on myfile[1]
myfile[1].seek(0)
Lz=[]
for i in range(Nobjects):
    Lz.append([float(myfile[1].readline().split()[1+i]) for x in range(file_length[1])])
    myfile[1].seek(0)
    
######################################
##Plot and save data##################
######################################
times_in_My = [x/365.25/1.0e6 for x in times]

from matplotlib import gridspec
import matplotlib.pyplot as plt

gs1 = gridspec.GridSpec(14, 1) #grid above which the pictures will be placed
gs1.update(left=0.05, right=0.95)
fig = plt.figure(figsize=(15,15))

ax1 = plt.subplot(gs1[0:2,0],xticklabels=[])
plt.plot(times_in_My,ecc[0],label="Jupiter",color="forestgreen")
ax1.set_xlabel("")
plt.legend();
ax2 = plt.subplot(gs1[2:4,0])
plt.plot(times_in_My,ecc[1],label="Companion")
ax2.set_xlabel("Time (My)",fontsize=12)
ax2.xaxis.set_tick_params(labelsize=10)
ax2.yaxis.set_tick_params(labelsize=10)
plt.legend();
fig.text(-0.015, 0.78, 'Eccentricity', va='center', rotation='vertical', fontsize=12)

ax3 = plt.subplot(gs1[5:7,0],xticklabels=[])
plt.plot(times_in_My,inc[0],label="Jupiter",color="forestgreen")
ax3.set_xlabel("")
plt.legend();
ax4 = plt.subplot(gs1[7:9,0])
plt.plot(times_in_My,inc[1],label="Companion")
ax4.set_xlabel("Time (My)",fontsize=12)
ax4.xaxis.set_tick_params(labelsize=10)
ax4.yaxis.set_tick_params(labelsize=10)
plt.legend();
fig.text(-0.015, 0.5, 'Inclination', va='center', rotation='vertical', fontsize=12)

ax5 = plt.subplot(gs1[10:12,0],xticklabels=[])
plt.plot(times_in_My,Lz[0],label="Jupiter",color="forestgreen")
ax5.set_xlabel("")
plt.legend();
ax6 = plt.subplot(gs1[12:14,0])
plt.plot(times_in_My,Lz[1],label="Companion")
ax6.set_xlabel("Time (My)",fontsize=12)
ax6.xaxis.set_tick_params(labelsize=10)
ax6.yaxis.set_tick_params(labelsize=10)
plt.legend();
fig.text(-0.015, 0.21, '$L_{z}$', va='center', rotation='vertical', fontsize=12)

fig.savefig("Companion_ecc+inc.png", bbox_inches = 'tight')
