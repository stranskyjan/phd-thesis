import sys
from yade import plot, pack, export
from heterogenizer import heterogenize

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

	outBase = "/tmp/mcpm_uniax",

	experiment = 'l',
	gradingCurve = 190,
	physCoeffs = (.5,1,.5),

	hGeomIndex = 1,
)
from yade.params.table import *
assert experiment in 'lh'
assert gradingCurve in (95,125,190)

O.materials.append(CpmMat(
	young = young,
	poisson = poisson,
	epsCrackOnset = epsCrackOnset,
	relDuctility = relDuctility,
	sigmaT = sigmaT,
	frictionAngle = frictionAngle,
))
O.materials.append(CpmMat(
	young = 2.5*young,
	poisson = poisson,
	epsCrackOnset = 2*epsCrackOnset,
	#epsCrackOnset = 1e20,
	relDuctility = relDuctility,
	sigmaT = 5*sigmaT,
	#sigmaT = 1e20,
	frictionAngle = frictionAngle,
))

s = specimenSize
sp = pack.randomDensePack(inAlignedBox((0,0,0),(s,s,s)),radius,spheresInCell=1000,memoizeDb="packing.db",returnSpherePack=True)
sp.toSimulation()

bb=uniaxialTestFeatures()
negIds,posIds,axis,crossSectionArea=bb['negIds'],bb['posIds'],bb['axis'],bb['area']
O.dt=dtSafety*SpherePWaveTimeStep(radius,density,2.5*young)

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
	#PyRunner(iterPeriod=100,command='vtkExport()'),
]

plot.plots={'eps':('sigma',)}

O.saveTmp('initial');

vtk = export.VTKExporter(outBase)

def vtkExport():
	vtk.exportSpheres(useRef=True,what=[('mat','b.mat.id'),('dspl','b.state.displ()')])
	vtk.exportInteractions(useRef=True,what=[
		('epsCrackOnset','i.phys.epsCrackOnset'),
		('epsFracture','i.phys.epsFracture'),
		('undamagedCohesion','i.phys.undamagedCohesion'),
		('E','i.phys.E'),
		('G','i.phys.G'),
		('relResidualStrength','i.phys.relResidualStrength'),
		('epsN','i.phys.epsN'),
	])

def addPlotData():
	plot.addData({'t':O.time,'i':O.iter,'eps':strainer.strain,'sigma':strainer.avgStress,})
	plotSaveDataTxt()

def plotSaveDataTxt():
	plot.saveDataTxt("{}.dat".format(outBase))

def initTest(mode):
	print "init"
	O.loadTmp('initial')
	if mode == "compression":
		print "Reversing plot data";
		plot.reverseData()
	strainer.strainRate = abs(strainRateTension) if mode=='tension' else -abs(strainRateCompression)
	spfile = "/tmp/heterogeom_{}_{:03d}_{}.sp".format(experiment,gradingCurve,hGeomIndex)
	heterogenize(specimenSize,spfile,physCoeffs)
	ss2sc.interactionDetectionFactor=1.
	is2aabb.aabbEnlargeFactor=1.
	if mode == 'tension':
		vtkExport()
	if 0:
		print set(i.phys.epsCrackOnset for i in O.interactions)
		print set(i.phys.epsFracture for i in O.interactions)
		print set(i.phys.epsCrackOnset for i in O.interactions)
		print set(i.phys.undamagedCohesion for i in O.interactions)
		print set(i.phys.E for i in O.interactions)
		print set(i.phys.G for i in O.interactions)

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
		if O.iter > 30000:
			break

plotSaveDataTxt()
vtkExport()
