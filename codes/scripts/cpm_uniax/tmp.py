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

s = specimenSize
sp = pack.randomDensePack(inAlignedBox((0,0,0),(s,s,s)),radius,spheresInCell=1000,memoizeDb="packing.db",returnSpherePack=True)
sp.toSimulation()
sp.save("/tmp/aaa.ps")
