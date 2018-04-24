import numpy as np
import time as tm
start_time = tm.time()
import rebound
sim = rebound.Simulation()
sim.units = ('AU', 'days', 'Msun')
#labels=["Sun","Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptun"]
labels=["Sun","Jupiter","Saturn","Uranus","Neptun"]
Nplanets=len(labels)-1
sim.add(labels)
energy_initial=sim.calculate_energy()
sim.status()

orbits=sim.calculate_orbits()
for t in range(0,Nplanets):
    print("P = %6.3f" % (orbits[t].P))

sim.integrator="whfast"
#sim.ri_whfast.safe_mode = 0
#sim.ri_whfast.corrector = 11
sim.dt=0.05*orbits[0].P
tmax=100000*365.25
Nout=1000
sim.move_to_com()

import matplotlib as mpl
mpl.use('tkagg')
import matplotlib.pyplot as plt
fig=rebound.OrbitPlot(sim, trails=True, unitlabel="[AU]", color=True)
fig.savefig("SolarSystem_initialorbits.png")

######################################
##Iterate and store interesting values
######################################
a=np.zeros((Nplanets,Nout))
ecc=np.zeros((Nplanets,Nout))
times = np.linspace(0.,tmax,Nout)
particles=sim.particles
for i,time in enumerate(times):
    sim.integrate(time, exact_finish_time=0)
    print(time)
    orbits=sim.calculate_orbits()
    for j in range(Nplanets):
        a[j][i]=orbits[j].a
        ecc[j][i]=orbits[j].e

#######################################
##Plot the values as a function of time
#######################################
fig = plt.figure(figsize=(12,5))
ax = plt.subplot(111)
for i in range(Nplanets):
    plt.plot(times,ecc[i],label=labels[i+1])
ax.set_xlabel("Time (days)")
ax.set_ylabel("Eccentricity")
plt.legend();
fig.savefig("SolarSystem_eccentricities.png")

fig = plt.figure(figsize=(12,5))
ax = plt.subplot(111)
for i in range(Nplanets):
    plt.plot(times,a[i],label=labels[i+1])
ax.set_xlabel("Time (days)")
ax.set_ylabel("Semi-major axis")
plt.legend();
fig.savefig("SolarSystem_semimajoraxis.png")

energy_final=sim.calculate_energy()
energy_diff=abs(energy_initial-energy_final)
print("Energy relative error: ", energy_diff, "(MSun*AU**2)/days**2.")
print("Energy relative error: ", energy_diff*0.59633, "J/10^43.")
print("Energy absolute error: ", energy_diff/abs(energy_initial), ".")
final_time = tm.time()
print("Time taken by the code: ", final_time-start_time, ".")
