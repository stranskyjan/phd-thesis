from minieigen import Vector3, Matrix3

class Interaction:
	def __init__(self,normal,damage):
		self.normal = Vector3(normal)
		self.damage = float(damage)

class Particle:
	def __init__(self,interactions):
		self.interactions = list(interactions)
	def computeDamageTensor(self):
		n = len(self.interactions)
		I = Matrix3.Identity
		sumdmg = sum(i.damage for i in self.interactions)
		sumdngnn = sum((i.damage*i.normal.outer(i.normal) for i in self.interactions),Matrix3.Zero)
		return -I*3./(2.*n)*sumdmg + 15./(2.*n)*sumdngnn

def intrs(damages):
	vs = (
		 Vector3.UnitX,
		 Vector3.UnitY,
		 Vector3.UnitZ,
	)
	return [Interaction(v,d) for v,d in zip(vs,damages)]

def intrs2(damages):
	vs = (
		 (Vector3.UnitX+Vector3.UnitY).normalized(),
		 (Vector3.UnitX-Vector3.UnitY).normalized(),
		 Vector3.UnitZ,
	)
	return [Interaction(v,d) for v,d in zip(vs,damages)]

def particle(damages):
	return Particle(intrs(damages))

def particle2(damages):
	return Particle(intrs2(damages))

def dmgTensor(damages,p=particle):
	print
	print 'damages', damages
	d = p(damages).computeDamageTensor()
	print 'damage tensor', d
	eigvals = d.spectralDecomposition()[1]
	print 'eigvals', eigvals
	avg1 = sum(damages)/float(len(damages))
	avg2 = sum(eigvals)/3.
	assert abs(avg1-avg2) < 1e-12
	print 'avgDmg',avg1

h = .5
for p in (particle,):#particle2):
	dmgTensor((0,0,0),p)
	dmgTensor((1,1,1),p)
	dmgTensor((h,h,h),p)
	dmgTensor((1,1,0),p)
	dmgTensor((h,h,0),p)
	dmgTensor((1,0,0),p)
	dmgTensor((h,0,0),p)

print
print 'test many intrs'
import random
random.seed(1)
normals = []
while len(normals) < 10000:
	x,y,z = [2*random.random()-1 for _ in (0,1,2)]
	if x*x+y*y+z*z > 1:
		continue
	normals.append(Vector3(x,y,z).normalized())
dd = Matrix3(1,0,0, 0,0,0, 0,0,0)
dd = Matrix3(1,0,0, 0,1,0, 0,0,1)
dd = Matrix3(1,0,.5, 0,.5,0, 0,.8,.25)
dd = .5*(dd+dd.transpose())
intrs = [Interaction(n,0) for n in normals]
for i in intrs:
	n = i.normal
	i.damage = n.dot(dd*n)
p = Particle(intrs)
d = p.computeDamageTensor()
print dd
print d
print sorted(dd.spectralDecomposition()[1])
print sorted( d.spectralDecomposition()[1])
