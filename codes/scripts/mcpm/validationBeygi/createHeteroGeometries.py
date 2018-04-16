from math import log, pi
from minieigen import Vector3
import random

fine = 917. + 205.
coarse = 750.
SSIZE = 50e-3

sieves = 4.75e-3, 9.5e-3, 12.5e-3, 19.0e-3

class Concrete:
	def __init__(self,a,w,c,p,unitWeight):
		self.a = a
		self.w = w
		self.c = c
		self.p = p
		self.unitWeight = unitWeight
		self.dw = 1000.
		self.dc = 3100.
		self.da = 2590.
		self.dp = 1000.
		self.m = self.v = None
		self.vw = self.vc = self.va = self.vp = self.vv = None
		self.update()
	def update(self):
		m = self.m = self.a + self.w + self.c + self.p
		v = m / self.unitWeight
		vv = self.vv = 1. - 1. / v
		vw = self.w / self.dw
		vc = self.c / self.dc
		va = self.a / self.da
		vp = self.p / self.dp
		v = vw + vc + va + vp
		f = (1.-vv)/v
		self.vw = vw * f
		self.vc = vc * f
		self.va = va * f
		self.vp = vp * f

class ExperimentalGradingCurve:
	def __init__(self,gradingCurve):
		self.gradingCurve = gradingCurve
	def findInterval(self,size):
		size = max(size,self.gradingCurve[0][0])
		for i in xrange(len(self.gradingCurve)-1):
			if self.gradingCurve[i+1][0] > size:
				return i
		return i
	def cdf(self,size):
		"""piecewise linear curve in semi-log scale -> piecewise log curve in real scale"""
		# y0 = a*log(x0) + b; y1 = a*log(x1) + b;
		# b = y0 - a*log(x0); y1 = a*log(x1) - a*log(x0) + y0; y1-y0 = a*(log(x1)-log(x0)); a = (y1-y0)/(log(x1)-log(x0))
		# b = y0 - a*log(x0);
		i = self.findInterval(size)
		x0 = self.gradingCurve[i][0]
		x1 = self.gradingCurve[i+1][0]
		y0 = self.gradingCurve[i][1]
		y1 = self.gradingCurve[i+1][1]
		assert size >= x0 and size <= x1, "{} {} {}".format(size,x0,x1)
		a = (y1-y0)/(log(x1)-log(x0))
		b = y0 - a*log(x0)
		return a*log(size) + b
	def computeSizes(self,delta0):
		dmin = self.gradingCurve[0][0]
		dmax = self.gradingCurve[-1][0]
		sizes = [dmin]
		size = dmin
		# compute relative number of particles in interval (dmin,dmin+delta0)
		n = (self.cdf(size+delta0)-self.cdf(size))/pow(size+delta0,3)
		while size < dmax: # fill sizes from dmin to dmax
			finish = False
			mmin = 0
			mmax = dmax-size
			kk = 0
			F = lambda d: (self.cdf(size+d)-self.cdf(size))/pow(size+d,3) - n
			# by bisection method, find delta such that relative number in interval (size,size+delta) is equal to precomputed value n
			while True:
				delta = .5*(mmin+mmax)
				vmin = F(mmin)
				vmax = F(mmax)
				if (vmin>0):
					raise RuntimeError, "Bisection method failed"
				if (vmax<0): # should only hapen at the end of interval
					# stop the method
					finish = True
					break
				vdelta = F(delta)
				if abs(vdelta) < 1e-12:
					break
				elif vdelta < 0:
					mmin = delta
				elif vdelta > 0:
					mmax = delta
				else:
					raise RuntimeError, "Bisection method failed" # this is impossible to happen if I am right
				kk += 1
				if kk > 100:
					raise RuntimeError, "Bisection method did not converge"
				#
				if mmin > 0. and mmax/mmin-1 <= 1e-9:
					break
			if finish:
				#sizes.append(self.gradingCurve[-1][0])
				break
			else:
				size += delta
				sizes.append(size)
		return sizes

class Sphere:
	def __init__(self,center,radius):
		self.center = center
		self.radius = radius
	def toLine(self):
		x,y,z = self.center
		return "{} {} {} {}\n".format(x,y,z,self.radius)

class SpherePack:
	def __init__(self):
		self.spheres = []
	def makeCloudFromSizes(self,sizes,seed=0,factor=1.05):
		random.seed(seed)
		sizes = sorted(sizes,key=lambda s: -s)
		for i,size in enumerate(sizes):
			r = .5*size
			sph = Sphere(None,r*factor)
			dmin,dmax = r, SSIZE-r
			ok = False
			for i in xrange(1000):
				pos = [dmin + (dmax-dmin)*random.random() for _ in (0,1,2)]
				pos = Vector3(pos)
				sph.center = pos
				if any((sph.center-sph2.center).squaredNorm() < pow(sph.radius+sph2.radius,2) for sph2 in self.spheres):
					continue
				else:
					ok = True
					break
			assert ok, "{} {}".format(i,size)
			self.spheres.append(sph)
		for s in self.spheres:
			s.radius /= factor
	def save(self,fileName):
		with open(fileName,"w") as f:
			f.writelines(s.toLine() for s in self.spheres)
		


def build(k,conc,gc,delta0,index):
	print gc.gradingCurve
	sizes = gc.computeSizes(delta0)
	print len(sizes),sizes[0],sizes[-1]
	sizesv = sum(4/3.*pi*pow(.5*s,3) for s in sizes)
	theorv = conc.va * coarse/(coarse+fine) * pow(SSIZE,3)
	assert abs(1-sizesv/theorv) < 5e-3, sizesv/theorv
	sp = SpherePack()
	sp.makeCloudFromSizes(sizes,index)
	sp.save("/tmp/heterogeom_{}_{}.sp".format(k,index))

def check(k,hGeomIndex):
	print
	print k,hGeomIndex
	fName = "/tmp/heterogeom_{}_{}.sp".format(k,hGeomIndex)
	with open(fName) as f:
		lines = f.readlines()
	radii = [float(l.split()[3]) for l in lines]
	mass = lambda radius: 4/3.*pi*pow(radius,3)
	mcoarse = sum(mass(r) for r in radii)
	print 'mcoarse',mcoarse
	mfine = mcoarse * fine / coarse
	print 'mfine',mfine
	mtot = mfine + mcoarse
	print 'mtot',mtot
	for sieve in sieves:
		m = mfine + sum(mass(r) for r in radii if 2*r <= sieve)
		passing = m / mtot
		print sieve,passing

def test():
	c = Concrete(1234., 123., 234., 12., 1234.+123.+234.+12.)
	assert c.vv == 0., c.vv
	v = c.vw+c.vc+c.va+c.vp+c.vv
	assert abs(v - 1.) < 1e-6, v
	#
	c.unitWeight *= .5
	c.update()
	assert abs(c.vv - .5) < 1e-6, c.vv
	v = c.vw+c.vc+c.va+c.vp+c.vv
	assert abs(v - 1.) < 1e-6, v
	#
	c.unitWeight *= .5
	c.update()
	assert abs(c.vv - .75) < 1e-6, c.vv
	v = c.vw+c.vc+c.va+c.vp+c.vv
	assert abs(v - 1.) < 1e-6, v

def main():
	import sys
	if "-t" in sys.argv or "--test" in sys.argv:
		test()
		return
	a = fine + coarse
	wl, cl = 187., 352.8
	wh, ch = 160.7, 422.4
	pl, ph = 4.4, 9.
	concretes = (
		Concrete(a,wl,cl,pl,2318.), # l 095
		Concrete(a,wl,cl,pl,2408.), # l 125
		Concrete(a,wl,cl,pl,2428.), # l 190
		Concrete(a,wh,ch,ph,2399.), # h 095
		Concrete(a,wh,ch,ph,2448.), # h 125
		Concrete(a,wh,ch,ph,2462.), # h 190
	)
	s0,s1,s2,s3 = sieves
	gCurves = ( # 095, 125, 190
		ExperimentalGradingCurve(((s0,fine/a),(s1,1.))),
		ExperimentalGradingCurve(((s0,fine/a),(s1,(fine+300.)/a),(s2,1.))),
		ExperimentalGradingCurve(((s0,fine/a),(s1,(fine+300.)/a),(s2,(fine+600.)/a),(s3,1.)))
	)
	deltas0 = (
		5.475e-6,
		1.3e-5,
		1.28e-5,
		5.4e-6,
		1.3e-5,
		1.3e-5
	)
	eks = ('l','h')
	gks = (95,125,190)
	ks = ["{}_{:03g}".format(e,g) for e in eks for g in gks]
	for i,(k,conc,gc,delta0) in enumerate(zip(ks,concretes,2*gCurves,deltas0)):
		for j in (1,2,3):
			print
			print k
			build(k,conc,gc,delta0,j)
			check(k,j)



if __name__ == "__main__":
	main()
