import numpy as np
import time as tm
start_time = tm.time()

def RadianToDegree(angle):
    while angle < -np.pi:
        angle += 2*np.pi
    while angle > np.pi:
        angle -= 2*np.pi
    return (angle*180/np.pi)

f=open("PlanetProperties.dat",'r')
import rebound
sim = rebound.Simulation()
sim.units = ('AU', 'days', 'Msun')
all_labels=["Sun","Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptun","Pluto"]
labels=["Sun","Jupiter","Saturn","Uranus","Neptun","Pluto"]
Nplanets=len(labels)-1
"""
for iObject in range(len(all_labels)):
    line=f.readline()
    if line.split()[0] in labels:
        print(line.split()[1])
        #sim.add(m=float(line.split()[1]),x=float(line.split()[2]),y=float(line.split()[3]),z=float(line.split()[4]),vx=float(line.split()[5]),vy=float(line.split()[6]),vz=float(line.split()[7]))
        if iObject != 0:
            sim.add(m=float(line.split()[1]),a=float(line.split()[8]),e=float(line.split()[9]))
        else:
            sim.add(m=float(line.split()[1]))
"""
sim.add(labels)
sim.status()
sim.move_to_com()
sim.integrator="whfast"
#sim.ri_whfast.safe_mode = 0
#sim.ri_whfast.corrector = 11
energy_initial=sim.calculate_energy()
orbits=sim.calculate_orbits() #it does not calculate the orbit of the Sun
for t in range(0,Nplanets):
    print("P = %6.3f" % (orbits[t].P))
sim.dt=0.05*orbits[0].P
tmax=2000*365.25
Nout=1000


import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt
fig=rebound.OrbitPlot(sim, trails=True, unitlabel="[AU]", color=True)
fig.savefig("SolarSystem_initialorbits.png")

######################################
##Iterate and store interesting values
######################################
x=np.zeros((Nplanets,Nout))
longitude=np.zeros((Nplanets,Nout))
varpi=np.zeros((Nplanets,Nout))
times = np.linspace(0.,tmax,Nout)
particles=sim.particles
for i,time in enumerate(times):
    sim.integrate(time, exact_finish_time=0)
    if time%100000==0: print(time)
    orbits=sim.calculate_orbits()
    for j in range(Nplanets):
        x[j][i]=particles[j+1].x
        longitude[j][i]=orbits[j].l
        varpi[j][i]=orbits[j].Omega+orbits[j].omega

thetaJupSat=[RadianToDegree(3*longitude[1][i]-longitude[0][i]-2*varpi[0][i]) for i in range(Nout)]
pheriheliondiffJupSat=[RadianToDegree(-varpi[1][i]+varpi[0][i]) for i in range(Nout)]
thetaUraNep=[RadianToDegree(2*longitude[3][i]-longitude[2][i]-varpi[2][i]) for i in range(Nout)]
pheriheliondiffUraNep=[RadianToDegree(-varpi[3][i]+varpi[2][i]) for i in range(Nout)]
thetaNepPlu=[RadianToDegree(1.5*longitude[4][i]-longitude[3][i]-0.5*varpi[4][i]) for i in range(Nout)]
pheriheliondiffNepPlu=[RadianToDegree(-varpi[4][i]+varpi[3][i]) for i in range(Nout)]

#######################################
##Plot the values as a function of time
#######################################
#Jupiter-Saturn 3:1 resonance
fig = plt.figure(figsize=(9,5))
ax = plt.subplot(211)
for i in range(Nplanets):
    plt.plot(times,x[i],label=labels[i+1])
ax.set_xlabel("")
ax.set_ylabel("Distance to the c.o.m. (AU)")
plt.legend();
ax = plt.subplot(212)
plt.plot(times,thetaJupSat,label="Resonant argument")
plt.plot(times,pheriheliondiffJupSat,label="Secular resonant argument")
ax.set_xlabel("Time (days)")
ax.set_ylabel("Resonant Argument (1:3)")
ax.set_ylim([-180.,180.])
plt.legend();
fig.savefig("SolarSystem_JupSatLibration.png")

fig = plt.figure(figsize=(9,5))
ax = plt.subplot(211)
for i in range(Nplanets):
    plt.plot(times,x[i],label=labels[i+1])
ax.set_xlabel("")
ax.set_ylabel("Distance to the c.o.m. (AU)")
plt.legend();
ax = plt.subplot(212)
plt.plot(times,thetaUraNep,label="Resonant argument")
plt.plot(times,pheriheliondiffUraNep,label="Secular resonant argument")
ax.set_xlabel("Time (days)")
ax.set_ylabel("Resonant Argument (1:2)")
ax.set_ylim([-180.,180.])
plt.legend();
fig.savefig("SolarSystem_UraNepLibration.png")

fig = plt.figure(figsize=(9,5))
ax = plt.subplot(211)
for i in range(Nplanets):
    plt.plot(times,x[i],label=labels[i+1])
ax.set_xlabel("")
ax.set_ylabel("Distance to the c.o.m. (AU)")
plt.legend();
ax = plt.subplot(212)
plt.plot(times,thetaNepPlu,label="Resonant argument")
plt.plot(times,pheriheliondiffNepPlu,label="Secular resonant argument")
ax.set_xlabel("Time (days)")
ax.set_ylabel("Resonant Argument (2:3)")
ax.set_ylim([-180.,180.])
plt.legend();
fig.savefig("SolarSystem_NepPluLibration.png")

energy_final=sim.calculate_energy()
energy_diff=abs(energy_initial-energy_final)
print("Energy absolute error: ", energy_diff/abs(energy_initial), ".")
final_time = tm.time()
print("Time taken by the code: ", final_time-start_time, ".")
