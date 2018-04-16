# Seed was not used in the end. The rerun will not produce exactly the same results, but should give very similar results
import sys
from yade import pack, plot

utils.readParamsFromTable(noTableOk = True,
	nums = (50,100,200,400),
	radius = .1234,
	seed = 1,
)
from yade.params.table import *

for num in nums:
	print num
	sys.stdout.flush()
	O.reset()
	#sp = myRandomPeriPack(radius,num,seed=seed,initSizeFactor=2.4+.0002*num)
	sp = pack.randomPeriPack(radius,2.4*num**(1/3.)*radius*Vector3.Ones)
	seed += 1
	sp.toSimulation()
	n = len(O.bodies)
	v = O.cell.volume
	f = n*4/3.*pi*pow(radius,3) / v
	plot.addData(
		numberOfParticles = n,
		packingFraction = f,
	)
plot.saveDataTxt('/tmp/randomPeriPack_packingFraction.dat')
