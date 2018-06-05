import numpy as np
import time as tm
import matplotlib as mpl
mpl.use('tkagg')
mpl.rc('axes.formatter', useoffset=False)
import matplotlib.pyplot as plt
from matplotlib import gridspec
import math

import rebound
start_time = tm.time()
sim = rebound.Simulation()
sim.units=('AU','days','Msun')
labels=["Sun","Pseudo-Jupiter","Companion"]
sim.add(m=1.)
sim.add(m=0.009547919152112404,a=5.,e=0.,inc=0.)
sim.add(m=0.5,a=500.,e=0.,inc=np.pi/2)
sim.move_to_com()
sim.integrator = "whfast"
energy_initial=sim.calculate_energy()
orbits=sim.calculate_orbits() #it does not calculate the orbit of the Sun

sim.dt=0.1*orbits[0].P
tmax=130000000*365.25
Nout=700
sim.status()
print(orbits[0].P)
fig=rebound.OrbitPlot(sim, slices=True, unitlabel="[AU]", color=True, periastron=True)
fig.savefig("Companion_initialorbits.png")

######################################
##Iterate and store interesting values
######################################
Nobjects=len(labels)-1
ecc=np.zeros((Nobjects,Nout))
inc=np.zeros((Nobjects,Nout))
Lz=np.zeros((Nobjects,Nout))
empty_list=np.zeros((Nobjects,Nout))

times = np.linspace(0.,tmax,Nout)
particles=sim.particles
for i,time in enumerate(times):
    sim.integrate(time, exact_finish_time=0)
    time_str = "{:.2f}".format(time/365.25/1.0e6)
    print(time_str, " My have passed.")
    orbits=sim.calculate_orbits()
    for j in range(Nobjects):
        ecc[j][i]=orbits[j].e
        inc[j][i]=orbits[j].inc
        Lz[j][i]=math.sqrt(1.-ecc[j][i]*ecc[j][i])*math.cos(inc[j][i])
        
######################################
##Store values in a file
######################################
def write_data(filename, y1, y2, y3, y4, y5):
    with open(filename,'w') as f:
        for (a, b, c, d, e) in zip(y1, y2, y3, y4, y5):
            print("%.10g\t%.10g\t%.10g\t%.10g\t%.10g" % (a, b, c, d, e), file=f)
write_data("saved_data.data", times, ecc[0], ecc[1], inc[0], inc[1]);
write_data("saved_data2.data", times, Lz[0], Lz[1], empty_list[0], empty_list[1]);

energy_final=sim.calculate_energy()
energy_diff=abs(energy_initial-energy_final)
print("Energy absolute error: ", energy_diff/abs(energy_initial), ".")
final_time = tm.time()
print("Time taken by the code: ", final_time-start_time, ".")
