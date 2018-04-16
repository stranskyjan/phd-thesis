# computes component by component analytically integrals over solid angle of special tensorial functions presented in the appendix
import sympy as s
pi = s.pi

a,z = s.symbols('a z') # azimuth and zenith angles
nx = s.sin(z)*s.cos(a) # x component of unit vector expressed in spherical coordinates
ny = s.sin(z)*s.sin(a) # y component of unit vector expressed in spherical coordinates
nz = s.cos(z)          # z component of unit vector expressed in spherical coordinates
n = (nx,ny,nz)         # unit vector

def integralOverSolidAngle(f):
	"""Returns integral over solid angle of scalar function f"""
	return s.simplify( s.integrate( f*s.sin(z), (a,0,2*pi), (z,0,pi) ) )

def delta(i,j):
	"""Returns value of Kronoecker's delta / ij component od unit 2nd order tensor"""
	return 1 if i==j else 0

def i4sym(i,j,k,l):
	"""Returns ijkl component of symmetric 4th order unit tensor"""
	return s.sympify( delta(i,k)*delta(j,l) + delta(i,l)*delta(j,k) ) / 2

def i4vol(i,j,k,l):
	"""Returns ijkl component of volumetric 4th order unit tensor"""
	return s.sympify("{}/3".format(delta(i,j)*delta(k,l)))

def i4nni4(i,j,k,l):
	"""Returns ijkl component of (I.n).(n.I)"""
	e = 0
	for a in xrange(3):
		for b in xrange(3):
			for c in xrange(3):
				ee = i4sym(i,j,a,b) * n[b] * n[c] * i4sym(c,a,k,l)
				e += s.sympify( ee )
				e = s.simplify( e )
	return s.sympify( e )

tsep = 70*"="
tint = "int(f)"
teq = "="

print
print tsep
print "f = 1"
res = integralOverSolidAngle(1)
theor = 4*pi
assert res == theor
print tint, teq, res

print
print tsep
print 'f = ni * nj'
for i,ni in enumerate(n):
	for j,nj in enumerate(n):
		res = integralOverSolidAngle(ni*nj)
		theor = 4*pi/3 * delta(i,j)
		assert res == theor
		print "{}_{}{}".format(tint,i+1,j+1), teq, res

print
print tsep
print 'f = ni * nj * nk * nl'
for i,ni in enumerate(n):
	for j,nj in enumerate(n):
		for k,nk in enumerate(n):
			for l,nl in enumerate(n):
				res = integralOverSolidAngle(ni*nj*nl*nk)
				theor = 4*pi/3 * (i4vol(i,j,k,l)*3/5 + i4sym(i,j,k,l)*2/5)
				theor2 = 4*pi/15*(delta(i,j)*delta(k,l)+delta(i,k)*delta(j,l)+delta(i,l)*delta(j,k))
				assert res == theor and theor == theor2
				print "{}_{}{}{}{}".format(tint,i+1,j+1,k+1,l+1), teq, res

# this one takes some time ...
print
print tsep
print 'f = Is_ijab * nb * nc * Is_cakl'
for i,ni in enumerate(n):
	for j,nj in enumerate(n):
		for k,nk in enumerate(n):
			for l,nl in enumerate(n):
				res = integralOverSolidAngle(i4nni4(i,j,k,l))
				theor = 4*pi/3 * i4sym(i,j,k,l)
				assert res == theor
				print "{}_{}{}{}{}".format(tint,i+1,j+1,k+1,l+1), teq, res
