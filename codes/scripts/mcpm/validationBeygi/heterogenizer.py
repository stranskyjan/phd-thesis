from math import tan
from yade import pack

def aggregateNumber(body,aggregs):
	p = body.state.pos
	r = body.shape.radius
	for i,a in enumerate(aggregs):
		if a(p,.5*r):
			return i
	return -1

def isITZ(i,bid2aggreg):
	id1,id2 = i.id1,i.id2
	b1,b2 = O.bodies[id1], O.bodies[id2]
	mat1,mat2 = b1.mat,b2.mat
	a1,a2 = [bid2aggreg[b.id] for b in b1,b2]
	#
	if mat1 is mat2:
		if a1 == a2:
			return False
		return True
	#
	assert set((mat1.id,mat2.id)) == set((0,1))
	return True

def setup(aggregs,physCoeffs):
	mortarMat,aggregMat = [O.materials[i] for i in (0,1)]
	#
	bid2aggreg = [-1 for b in O.bodies]
	for b in O.bodies:
		ia = aggregateNumber(b,aggregs)
		a = ia >= 0
		if a:
			b.mat = aggregMat
			bid2aggreg[b.id] = ia
		else:
			b.mat = mortarMat
	#
	O.step()
	#
	m = mortarMat
	c1,c2,c3 = [float(v) for v in physCoeffs]
	for i in O.interactions:
		if not isITZ(i,bid2aggreg):
			continue
		p = i.phys
		#
		p.E = m.young * c1
		p.G = p.E * m.poisson
		p.tanFrictionAngle = tan(m.frictionAngle)
		p.undamagedCohesion = m.sigmaT * c2
		p.epsCrackOnset = m.epsCrackOnset * c2/c1
		p.relDuctility = m.relDuctility * c3
		p.epsFracture = p.epsCrackOnset * p.relDuctility
		#
		p.kn = p.E * p.crossSection / p.refLength
		p.ks = p.G * p.crossSection / p.refLength

def heterogenize(specimenSize,spfile,physCoeffs):
	sp = pack.SpherePack()
	sp.load(spfile)
	aggregs = [pack.inSphere(c,r) for c,r in sp]
	setup(aggregs,physCoeffs)


