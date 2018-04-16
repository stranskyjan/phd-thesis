import sys, os
from yade import *
from yade import pack, Vector3

def myRandomPeriPack(radius,num,seed=1,memo="",initSizeFactor=3.):
	if memo and os.path.exists(memo):
		ret = pack.SpherePack()
		ret.load(memo)
		return ret
	O.switchScene(); O.resetThisScene()
	sp = pack.SpherePack()
	O.periodic = True
	O.cell.setBox(num**(1/3.)*initSizeFactor*radius*Vector3(1,1,1))
	sp.makeCloud(Vector3().Zero,O.cell.refSize,radius,0,num,True,seed=seed)
	O.engines = [
		ForceResetter(),
		InsertionSortCollider([Bo1_Sphere_Aabb()],verletDist=0),#allowBiggerThanPeriod=True),
		InteractionLoop(
			[Ig2_Sphere_Sphere_ScGeom()],
			[Ip2_FrictMat_FrictMat_FrictPhys()],
			[Law2_ScGeom_FrictPhys_CundallStrack()]
		),
		PeriIsoCompressor(charLen=2*radius,stresses=[-100e9,-1e8],maxUnbalanced=1e-2,doneHook='O.pause();',globalUpdateInt=20,keepProportions=True),
		NewtonIntegrator(damping=.1)
	]
	O.materials.append(FrictMat(young=30e9,frictionAngle=.0,poisson=.3,density=1e3))
	for s in sp:
		O.bodies.append(utils.sphere(s[0],s[1]))
	O.dt=.3*utils.PWaveTimeStep()
	O.timingEnabled = True
	O.run()
	O.wait()
	p0 = O.bodies[0].state.pos
	for b in O.bodies:
		p = b.state.pos - p0
		b.state.pos = O.cell.wrapPt(p)
	ret = pack.SpherePack()
	ret.fromSimulation()
	O.switchScene()
	if memo:
		ret.save(memo)
	return ret

if sys.argv[0] == "randomPeriPack.py":
	radius = num = None
	seed = 1
	memo = ""
	for i,a in enumerate(sys.argv):
		if a == "--radius":
			radius = float(sys.argv[i+1])
		if a == "--memo":
			memo = sys.argv[i+1]
		if a == "--seed":
			seed = int(sys.argv[i+1])
		if a == "--num":
			num = int(sys.argv[i+1])
	if radius and num:
		packing = myRandomPeriPack(radius,num,seed,memo)
