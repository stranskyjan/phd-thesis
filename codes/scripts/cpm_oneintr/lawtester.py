#!yade-2017.01a
from yade import plot

outbase = "/tmp/cpm_law_tester_{}.dat"

class MyPhys:
	def __init__(self):
		self.epsN = self.sigmaN = self.omega = self.kappaD = 0.
class MyInteraction:
	def __init__(self):
		self.phys = MyPhys()

def plotAddData(iter0=False):
	if iter0:
		i = MyInteraction()
	else:
		i = O.interactions[0,1]
	plot.addData(
		strainN = i.phys.epsN,
		stressN = i.phys.sigmaN,
		damage = i.phys.omega,
		kappa = i.phys.kappaD,
	)

def engines():
	O.engines = [
		ForceResetter(),
		InsertionSortCollider([Bo1_Sphere_Aabb()]),
		InteractionLoop(
			[Ig2_Sphere_Sphere_ScGeom()],
			[Ip2_CpmMat_CpmMat_CpmPhys()],
			[Law2_ScGeom_CpmPhys_Cpm()],
		),
		NewtonIntegrator(),
		PyRunner(iterPeriod=1,command='plotAddData()'),
	]
	O.dt = 1.

def spheres(length=1):
	r = .5*length
	b1 = sphere((0,0,0),r)
	b2 = sphere((length,0,0),r)
	for b in b1,b2:
		b.state.blockedDOFs = 'xyzXYZ'
	O.bodies.append((b1,b2))
	i = createInteraction(0,1)
	return b1,b2,i

def cpmMat(young=1e9,shear=1e9,strain0=1e-4,strainF=2e-4,c0=1e6,fa=atan(.5)):
	mat = CpmMat(young=young,poisson=shear/young,epsCrackOnset=strain0,relDuctility=strainF/strain0,sigmaT=c0,frictionAngle=fa)
	O.materials.append(mat)
	return mat

def reset(**kw):
	plot.data = {}
	O.reset()
	engines()
	cpmMat(**kw)
	plotAddData(True)
	return spheres()

# normal direction tension
b0,b1,i = reset(young=1e9,strain0=1e-4,strainF=1.5e-4)
b1.state.vel = (1e-5,0,0)
O.run(30,True)
plot.saveDataTxt(outbase.format("normal_simple_tension"))

# normal direction cyclic
b0,b1,i = reset(young=1e9,strain0=1e-4,strainF=1.5e-4)
b1.state.vel = (1e-5,0,0)
O.run(15,True)
b1.state.vel = (-1e-5,0,0)
O.run(12,True)
b1.state.vel = (1e-5,0,0)
O.run(25,True)
b1.state.vel = (-1e-5,0,0)
O.run(35,True)
plot.saveDataTxt(outbase.format("normal_cyclic"))
