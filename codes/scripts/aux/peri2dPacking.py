# used for text/figs/raphaelpy, section "mcpm itz possibilites"
import random
random.seed(1)

r = .1
n = 25
O.periodic = True
O.bodies.append([sphere((random.random(),random.random(),0),r) for _ in xrange(n)])
for b in O.bodies:
	b.state.blockedDOFs = 'zXYZ'
for i in xrange(20):
	O.run(20,True)
	calm()
for b in O.bodies:
	b.state.pos = O.cell.wrap(b.state.pos)
sp = SpherePack()
sp.fromSimulation()
sp.save("/tmp/2dpacking.sp")
