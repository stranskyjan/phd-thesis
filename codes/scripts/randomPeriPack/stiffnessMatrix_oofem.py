from randomPeriPack import myRandomPeriPack
import subprocess

oofem = "oofem-2.0"

utils.readParamsFromTable(noTableOk = True,
	intRatio = 1.5,
	young = 25e9,
	#poisson = .2,
	poisson = 1e4,
	seed = 1,
	packing = "",
	outbase = '/tmp/randomPeriPack_oofem',
	radius = .12345,
	num = 300,
)
from yade.params.table import *

oofeminfile = "{}.in".format(outbase)

O.materials.append(CpmMat(young=young,poisson=poisson,epsCrackOnset=1e20,relDuctility=10,sigmaT=1e20))
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
sp.toSimulation()
for b in O.bodies:
	b.state.inertia *= poisson
O.engines = [
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor=intRatio,label='bo1')],
	verletDist=.05*radius),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=intRatio,label='ig2')],
		[Ip2_CpmMat_CpmMat_CpmPhys()],
		[Law2_ScGeom_CpmPhys_Cpm()]
	),
	NewtonIntegrator(damping=.8),
]
O.step()
#
nBodies = len(O.bodies)
nIntrs = len([i for i in O.interactions])
b0 = O.bodies[0]
p0 = b0.state.pos
cs = O.cell.size
lines = [
	"{}.out".format(outbase),
	"Cohesive particle model in 3D, periodic cell created by {}".format(__file__),
	"LinearStatic nsteps 6 lstype 4 smtype 9",
	"domain 3dShell",
	"OutputManager tstep_all dofman_all element_all",
	"ndofman {} nelem {} ncrosssect 1 nmat 1 nbc 7 nic 0 nltf 7 nbarrier 0".format(nBodies+1,nIntrs),
	"Particle 1 coords 3 {} {} {} rad {} bc 6 2 3 4 5 6 7".format(cs[0],cs[1],cs[2],radius),
	"Particle 2 coords 3 {} {} {} rad {} bc 6 1 1 1 0 0 0".format(p0[0],p0[1],p0[2],b0.shape.radius),
]
for i,b in enumerate(O.bodies):
	if i==0: continue
	p = b.state.pos
	r = b.shape.radius
	lines.append("Particle {} coords 3 {} {} {} rad {}".format(i+2,p[0],p[1],p[2],r))
area = pi*pow(radius,2)
for ii,i in enumerate(O.interactions):
	cd = i.cellDist
	if any(cd):
		kxkykz = " kx {} ky {} kz {}".format(*tuple(i.cellDist))
		lines.append("CohSur3d {} nodes 3 {} {} 1 mat 1 crossSect 1 area {} kx {} ky {} kz {}".format(
			ii+1,
			i.id1+2,
			i.id2+2,
			area,
			cd[0],
			cd[1],
			cd[2],
		))
	else:
		lines.append("CohSur3d {} nodes 2 {} {} mat 1 crossSect 1 area {}".format(ii+1,i.id1+2,i.id2+2,area))
lines.extend((
	"SimpleCS 1 thick 1.0 width 1.0",
	"CohInt 1 d 0 kn {} ks {}".format(young,young*poisson),
	"BoundaryCondition 1 loadTimeFunction 1 prescribedvalue 0.0",
))
for i in xrange(6):
	lines.append("BoundaryCondition {0} loadTimeFunction {0} prescribedvalue 1".format(i+2))
lines.append("ConstantFunction 1 f(t) 1")
for i in xrange(6):
	lines.append("PeakFunction {} t {} f(t) 1".format(i+2,i+1))
with open(oofeminfile,"w") as f:
	f.writelines(l+"\n" for l in lines)

cmd = "{} -f {}".format(oofem,oofeminfile)
#subprocess.Popen(cmd.split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
#subprocess.Popen(cmd.split(),stdout=subprocess.PIPE).communicate()
subprocess.Popen(cmd.split()).wait()

def getResults(fName):
	ret = [[None for i in xrange(6)] for j in xrange(6)]
	with open(fName) as f:
		reactions = [l for l in f if 'reaction' in l]
	reactions = [r.split() for r in reactions]
	reactions = [r for r in reactions if r[1] == '1']
	assert len(reactions) == 36, len(reactions)
	for c in xrange(6):
		for r in xrange(6):
			l = reactions[6*c+r]
			v = float(l[5])
			ret[r][c] = v
	return ret

d = getResults("{}.out".format(outbase))
d = Matrix6(d)
d /= O.cell.volume

# print and save
def printAndSave(m):
	with open("{}.dat".format(outbase),'w') as f:
		fun = lambda e: "{}{:.3e}".format("" if e<0 else " ",e).ljust(10)
		for r in xrange(6):
			row = m.row(r)
			s = " ".join(map(fun,row))
			print s
			f.write(s+"\n")
printAndSave(d)
