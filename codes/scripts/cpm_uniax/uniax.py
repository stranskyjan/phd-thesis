import sys
from yade import plot, pack

readParamsFromTable(noTableOk=True,
	young = 25e9,
	poisson = .2,
	epsCrackOnset = 1e-4,
	relDuctility = 30,
	sigmaT = 3e6,
	frictionAngle = atan(0.8),
	density = 4800.,

	intRadius = 1.5,
	dtSafety = .8,
	damping = 0.3,
	strainRateTension = .4,
	strainRateCompression = 3,

	specimenSize = 50e-3,

	radius = 1e-3,

	outBase = "/tmp/cpm_uniax",
)
from yade.params.table import *

if 'description' in O.tags.keys():
	outBase = "{}_{}".format(outBase,O.tags['description'])

O.materials.append(CpmMat(
	young = young,
	poisson = poisson,
	epsCrackOnset = epsCrackOnset,
	relDuctility = relDuctility,
	sigmaT = sigmaT,
	frictionAngle = frictionAngle,
))

s = specimenSize
sp = pack.randomDensePack(inAlignedBox((0,0,0),(s,s,s)),radius,spheresInCell=1000,memoizeDb="packing.db",returnSpherePack=True)
sp.toSimulation()

bb=uniaxialTestFeatures()
negIds,posIds,axis,crossSectionArea=bb['negIds'],bb['posIds'],bb['axis'],bb['area']
O.dt=dtSafety*SpherePWaveTimeStep(radius,density,max(50e9,young))

mm,mx=[pt[axis] for pt in aabbExtrema()]

O.engines=[
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor=intRadius,label='is2aabb'),],verletDist=.05*radius),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=intRadius,label='ss2sc')],
		[Ip2_CpmMat_CpmMat_CpmPhys()],
		[Law2_ScGeom_CpmPhys_Cpm()],
	),
	NewtonIntegrator(damping=damping),
	CpmStateUpdater(realPeriod=.5),
	UniaxialStrainer(strainRate=strainRateTension,axis=axis,asymmetry=0,posIds=posIds,negIds=negIds,crossSectionArea=crossSectionArea,blockDisplacements=False,blockRotations=False,setSpeeds=True,label='strainer'),
	PyRunner(iterPeriod=100,command='addPlotData()',label='plotDataCollector',initRun=True),
	PyRunner(iterPeriod=100,command='print O.iter,plot.data["sigma"][-1]'),
]

plot.plots={'eps':('sigma',)}

O.saveTmp('initial');

def addPlotData():
	yade.plot.addData({'t':O.time,'i':O.iter,'eps':strainer.strain,'sigma':strainer.avgStress,})

def initTest(mode):
	print "init"
	O.loadTmp('initial')
	if mode == "compression":
		print "Reversing plot data";
		plot.reverseData()
	strainer.strainRate = abs(strainRateTension) if mode=='tension' else -abs(strainRateCompression)
	O.step();
	ss2sc.interactionDetectionFactor=1.
	is2aabb.aabbEnlargeFactor=1.

def stopIfDamaged(mode):
	sigma,eps = plot.data['sigma'], plot.data['eps']
	mode = 'tension' if strainer.strainRate > 0 else 'compression'
	extremum = max(sigma) if mode == 'tension' else min(sigma)
	minMaxRatio = 0.2 if mode=='tension' else 0.7
	if abs(sigma[-1]/extremum) < minMaxRatio or abs(strainer.strain) > 5e-3:
		print "Damaged, stopping."
		return True

for mode in ('tension','compression'):
	initTest(mode)
	while True:
		O.run(100,True)
		if stopIfDamaged(mode):
			break
		if O.iter > 10000:
			break

sigma = plot.data["sigma"]
ft,fc = max(sigma),min(sigma)
print 'Strengths fc={}, ft={}, |fc/ft|={}'.format(fc,ft,abs(fc/ft))
plot.saveDataTxt("{}.dat".format(outBase))
print 'Bye.'
