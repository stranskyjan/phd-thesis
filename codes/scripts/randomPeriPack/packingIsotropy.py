from randomPeriPack import myRandomPeriPack

zFactor = .7
nSegments = 32

O.materials.append(CpmMat(neverDamage=True))
O.engines = [
	ForceResetter(),
	InsertionSortCollider([Bo1_Sphere_Aabb(aabbEnlargeFactor=1.5)]),
	InteractionLoop(
		[Ig2_Sphere_Sphere_ScGeom(interactionDetectionFactor=1.5)],
		[Ip2_CpmMat_CpmMat_CpmPhys()],
		[Law2_ScGeom_CpmPhys_Cpm()],
	),
	NewtonIntegrator(),
]
sp = myRandomPeriPack(.1234,4000,1,memo="/tmp/packingIsotropy.sp")
sp.toSimulation()
O.step()
normals = [i.geom.normal for i in O.interactions]
print len(normals)
normals = [n for n in normals if abs(n[2]) <= zFactor]
print len(normals)
bins = [0 for _ in xrange(nSegments)]
for n in normals:
	n = Vector3(n[0],n[1],0).normalized()
	a = atan2(n[1],n[0])
	a += .5*pi
	i = int(nSegments*a/pi)
	bins[i] += 1
print bins
with open("/tmp/packingIsotropy.dat","w") as f:
	f.write("# angle numIntrs\n")
	f.writelines("{} {}\n".format((i+.5)*pi/nSegments,b) for i,b in enumerate(bins))
	f.write("\n")
	f.write("# avgNumIntrs\n")
	r = sum(bins)/float(len(bins))
	n = 64
	f.writelines("{} {}\n".format(i*pi/n,r) for i in xrange(n+1))
