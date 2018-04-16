from randomPeriPack import myRandomPeriPack

utils.readParamsFromTable(noTableOk = True,
	intRatio = 1.5,
	young = 25e9,
	poisson = .2,
	seed = 1,
	outbase = '/tmp/stiffnessMatrix_yade',
	radius = .12345,
	num = 300,
	strain = 1e-6,
	packing = "",

	ftol = 1e-6,
	ttol = 1e-6,
	dt0 = 1e-20,
)
from yade.params.table import *

if packing:
	sp = pack.SpherePack()
	sp.load(packing)
	with open(packing) as f:
		l = f.readline()
	assert l.startswith("##PERIODIC:: ")
	sp.isPeriodic = True
	sp.cellSize = Vector3(*[float(w) for w in l.split()[1:]])
else:
	sp = myRandomPeriPack(radius,num,seed=seed)
volume = reduce(lambda r,v: r*v, sp.cellSize, 1.)

def initSimulation():
	O.reset()
	O.materials.append(CpmMat(young=young,poisson=poisson,epsCrackOnset=1e99,relDuctility=10,sigmaT=1e99))
	sp.toSimulation()
	O.engines = [
		ForceResetter(),
		InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor=intRatio,label='bo1')],
		verletDist=.05*radius),
		InteractionLoop(
			[Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=intRatio,avoidGranularRatcheting=False,label='ig2')],
			[Ip2_CpmMat_CpmMat_CpmPhys()],
			[Law2_ScGeom_CpmPhys_Cpm()]
		),
		NewtonIntegrator(damping=.1),
	]
	O.dt = dt0
	O.step()
	bo1.aabbEnlargeFactor = ig2.interactionDetectionFactor = 1.0
	O.bodies[0].state.blockedDOFs = 'xyz'

def evalStiffnessTheor():
	def kd(i,j):
		return 1 if i==j else 0
	def is4(i,j,k,l):
		return .5*(kd(i,k)*kd(j,l)+kd(i,l)*kd(j,k))
	def nnn(n,i,j,k):
		return n[i]*n[j]*n[k]
	def nnnn(n,i,j,k,l):
		return n[i]*n[j]*n[k]*n[l]
	def tttt(n,i,j,k,l):
		ret = 0.
		for a in (0,1,2):
			for b in (0,1,2):
				for c in (0,1,2):
					ret += is4(i,j,a,b)*n[b]*n[c]*is4(c,a,k,l)
		return ret - nnnn(n,i,j,k,l)
	def d(length,normal,area,e,g,i,j,k,l):
		return length*area*(e*nnnn(normal,i,j,k,l)+g*tttt(normal,i,j,k,l))
	#
	ret = Matrix6.Zero
	for i in O.interactions:
		length = i.phys.refLength
		normal = i.geom.normal
		area = i.phys.crossSection
		e = i.phys.E
		g = i.phys.G
		dd = Matrix6.Zero
		for ii in xrange(6):
			for jj in xrange(6):
				i,j = ((0,0),(1,1),(2,2),(1,2),(0,2),(0,1))[ii]
				k,l = ((0,0),(1,1),(2,2),(1,2),(0,2),(0,1))[jj]
				dd[ii,jj] += d(length,normal,area,e,g,i,j,k,l)
		ret += dd
	ret /= volume
	return ret

def evalSumladiv3v():
	return sum(i.phys.refLength*i.phys.crossSection for i in O.interactions) / (3*volume)

def setStrain(component):
	trsf = Matrix3.Identity
	if component in (0,1,2):
		trsf[component,component] += strain
	else:
		i = (component+1)%3
		j = (component+2)%3
		trsf[i,j] = trsf[j,i] = .5*strain
	O.cell.velGrad = (trsf-Matrix3.Identity)/O.dt
	O.step()
	O.cell.velGrad = Matrix3.Zero
	O.step()

def evalStiffnessColumn(component):
	s = getStress()
	ret = Vector6.Zero
	for i in (0,1,2):
		ret[i] = s[i,i]
	for i in (3,4,5):
		ret[i] = s[(i+1)%3,(i+2)%3]
	return ret / strain

def pp(m,out=None):
	if out is None:
		out = sys.stdout
	f = lambda e: "{}{:.3e}".format("" if e<0 else " ",e).ljust(10)
	for r in xrange(6):
		row = m.row(r)
		out.write(" ".join(map(f,row))+"\n")

def setGlobalStiffnessTimeStepper():
	ts = GlobalStiffnessTimeStepper(timeStepUpdateInterval=10)
	O.engines = O.engines[:-1] + [ts] + O.engines[-1:]
	ts()

def evalStiffness(theor=False):
	ret = Matrix6.Zero
	for component in xrange(6):
		print "  component",component
		initSimulation()
		if component == 0 and theor:
			stiffnessTheor = evalStiffnessTheor()
			sumladiv3v = evalSumladiv3v()
		setStrain(component)
		setGlobalStiffnessTimeStepper()
		breaked = False
		for i in xrange(10000):
			O.run(100,True)
			mass = sum(b.state.mass for b in O.bodies)
			f = sum(O.forces.f(b.id).norm() for b in O.bodies) / mass
			t = sum(O.forces.t(b.id).norm() for b in O.bodies) / mass
			print i,f,t,kineticEnergy(),unbalancedForce()
			if f < ftol and t < ttol:
				breaked = True
				break
		if not breaked:
			raise RuntimeError
		column = evalStiffnessColumn(component)
		for i in xrange(6):
			ret[i,component] = column[i]
	return (ret,stiffnessTheor,sumladiv3v) if theor else ret

stiffness,theor,sumladiv3v = evalStiffness(True)
with open("{}.dat".format(outbase),"w") as sys.stdout:
	print '# stiffnessNum'
	pp(stiffness)
	print
	print '# stiffnessTheor'
	pp(theor)
	print
	print '# sumladiv3v'
	print sumladiv3v
	sys.stdout.flush()
sys.stdout = sys.__stdout__
