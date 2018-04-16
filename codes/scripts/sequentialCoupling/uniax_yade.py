import sys
sys.path.append("../randomPeriPack")
from randomPeriPack import myRandomPeriPack
from yade import plot, export

utils.readParamsFromTable(noTableOk = True,
	outBase = "/tmp/sequential_coupling_yade_plain",
	nSteps = (4000,),
	signs = (1,),
	strainRate = 2/1.,
)
from yade.params.table import *
assert len(nSteps) == len(signs)

radius = 1e-3
young = 27e9
ndz = 2
bcCoeff = 4.

cpmMat = CpmMat(young=young,poisson=.2,epsCrackOnset=.98e-4,relDuctility=30,sigmaT=3.0e6,frictionAngle=atan(1.2))
O.materials.append(cpmMat)

O.engines = [
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor=1.5,label='bo1')]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=1.5,label='ig2')],
		[Ip2_CpmMat_CpmMat_CpmPhys(cohesiveThresholdIter=1)],
		[Law2_ScGeom_CpmPhys_Cpm()],
	),
	NewtonIntegrator(damping=.3),
	PyRunner(iterPeriod=sum(nSteps)/50,command='plotAddData()'),
	#PyRunner(iterPeriod=sum(nSteps)/50,command='vtkExport()'),
	CpmStateUpdater(iterPeriod=sum(nSteps)/50),
]

sp = myRandomPeriPack(radius,1000,seed=1)#,memo="/tmp/sequential_coupling_uniax_yade.sp")
dx,dy,dz = sp.cellSize
sphs = [sphere(c+radius*Vector3.Ones+i*Vector3(0,0,dz),radius) for c,_ in sp for i in xrange(ndz)]
top, bot = [], []
size = dimx,dimy,dimz = [d*i + 2*radius for d,i in zip((dx,dy,dz),(1,1,ndz))]
dimz = dz*ndz + 2*radius
vel = strainRate * dimz
for s in sphs:
	z = s.state.pos[2]
	if z < bcCoeff*radius:
		s.state.blockedDOFs = 'zXYZ'
		s.shape.color = (1,0,0)
		bot.append(s)
	elif z > dimz - bcCoeff*radius:
		s.state.blockedDOFs = 'zXYZ'
		s.shape.color = (0,1,0)
		top.append(s)
	else:
		s.shape.color = (0,0,1)
O.bodies.append(sphs)

O.dt = .5*PWaveTimeStep()
O.step()
bo1.aabbEnlargeFactor = 1.
ig2.interactionDetectionFactor = 1.

vtk = export.VTKExporter(outBase)
def vtkExport():
	vtk.exportSpheres(useRef=True,what=[('dmg','b.state.normDmg'),('dspl','b.state.displ()')])

def plotAddData():
	dimx,dimy,dimz = size
	area = dimx*dimy
	dspl = 2*top[0].state.displ()[2]
	strain = dspl / dimz
	stress = averageStress()[2,2]
	dmgTensor = averageDamageTensor()
	dmg3,dmg2,dmg1 = sorted(dmgTensor.spectralDecomposition()[1])
	plot.addData(
		i = O.iter,
		stress = stress,
		strain = strain,
		dmg1 = dmg1,
		dmg2 = dmg2,
		dmg3 = dmg3,
	)
plot.plots = dict(strain=("stress"))

def stressOfParticle(bid):
	b = O.bodies[bid]
	ret = Matrix3.Zero
	for i in b.intrs():
		f = i.phys.normalForce + i.phys.shearForce
		if b.id == i.id1:
			f *= -1
		x = i.geom.contactPoint - b.state.pos
		ret += x.outer(f)
	return ret
def averageStress():
	topids = set(b.id for b in top)
	botids = set(b.id for b in bot)
	ids = set(b.id for b in O.bodies) - topids - botids
	vol = size[0] * size[1] * size[2]
	nb = len(O.bodies)
	vol *= (nb-len(top)-len(bot))/float(nb)
	stress = sum((stressOfParticle(i) for i in ids),Matrix3.Zero) / vol
	return stress

def damageOfParticle(bid):
	b = O.bodies[bid]
	ret = Matrix3.Zero
	intrs = b.intrs()
	n = len(intrs)
	term1 = -3./(2*n)*sum((1.-i.phys.relResidualStrength) for i in intrs)*Matrix3.Identity
	term2 = 12./(2*n)*sum(((1.-i.phys.relResidualStrength)*i.geom.normal.outer(i.geom.normal) for i in intrs),Matrix3.Zero)
	return term1 + term2
def averageDamageTensor():
	topids = set(b.id for b in top)
	botids = set(b.id for b in bot)
	ids = set(b.id for b in O.bodies) - topids - botids
	dmg = sum((damageOfParticle(i) for i in ids),Matrix3.Zero) / len(ids)
	return dmg


for ns,sign in zip(nSteps,signs):
	calm()
	vel = Vector3(0,0,sign*strainRate*size[2])
	for b in top:
		b.state.vel = -vel
	for b in bot:
		b.state.vel = vel
	O.run(ns,True)

plot.saveDataTxt(outBase+".dat")

stress = averageStress()
stress = [.5*(stress[i,j]+stress[j,i]) for i,j in ((0,0),(1,1),(2,2),(1,2),(2,0),(0,1))]
dmg3,dmg2,dmg1 = sorted(averageDamageTensor().spectralDecomposition()[1])
dmg = (dmg1,dmg2,dmg3)
with open("{}_final.dat".format(outBase),"w") as f:
	for arry in stress,dmg:
		f.write("{}\n".format(" ".join(str(v) for v in arry)))
