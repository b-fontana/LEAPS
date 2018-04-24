import rebound
sim = rebound.Simulation()
labels = ["Sun","Mercury","Venus","Earth","Mars","Jupiter","Saturn","Uranus","Neptun","Pluto"]
#labels = ["Sun","Mercury"]
sim.add(labels)

f=open("PlanetProperties.dat",'w')
particles=sim.particles
orbits=sim.calculate_orbits()
for iObject in range(len(labels)):
    f.write(labels[iObject]+"\t"+str(particles[iObject].m)+"\t"+str(particles[iObject].x)+"\t"+str(particles[iObject].y)+"\t"+str(particles[iObject].z)+"\t"+str(particles[iObject].vx)+"\t"+str(particles[iObject].vy)+"\t"+str(particles[iObject].vz)+"\t")
    if iObject != 0: f.write(str(orbits[iObject-1].a)+"\t"+str(orbits[iObject-1].e)+"\n")
    else: f.write("\n")
f.close()

sim2=rebound.Simulation()
f2=open("PlanetProperties.dat",'r')
for iObject in range(len(labels)):
    line=f2.readline()
    sim2.add(m=float(line.split()[1]),x=float(line.split()[2]),y=float(line.split()[3]),z=float(line.split()[4]),vx=float(line.split()[5]),vy=float(line.split()[6]),vz=float(line.split()[7]))
sim2.status()
