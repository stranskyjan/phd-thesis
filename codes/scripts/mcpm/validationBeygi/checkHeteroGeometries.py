from math import pi

experiments = ('l','h')
gradingCurves = (95,125,190)
hGeomIndexes = (1,2,3)

sieves = (4.75e-3, 9.5e-3, 12.5e-3, 19.0e-3)

fine = 917. + 205.
coarse = 750.
res = fine / (fine + coarse)

def check(experiment,gradingCurve,hGeomIndex):
	print
	print experiment,gradingCurve,hGeomIndex
	fName = "heterogeom_{}_{:03d}_{}.sp".format(experiment,gradingCurve,hGeomIndex)
	with open(fName) as f:
		lines = f.readlines()
	radii = [float(l.split()[3]) for l in lines]
	mass = lambda radius: 4/3.*pi*pow(radius,3)
	mtot = sum(mass(r) for r in radii)
	print 'mtot',mtot
	coeff = coarse / (fine + coarse) / mtot
	for sieve in sieves:
		m = sum(mass(r) for r in radii if 2*r <= sieve)
		passing = res + coeff * m
		print sieve,passing

	
for e in experiments:
	for g in gradingCurves:
		for i in hGeomIndexes:
			check(e,g,i)

print 'should be:'
tot = fine+coarse

print 95
s1,s2,s3,s4 = sieves
print s1,res
print s2,1

print 125
print s1,res
print s2,(fine+300)/tot
print s3,1

print 190
print s1,res
print s2,(fine+300)/tot
print s3,(fine+600)/tot
print s4,1
