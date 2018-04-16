import os
from minieigen import *

rfile = lambda f: "{}.dat".format(f)

######################################################################
def matFromFile(fName,block=0):
	ret = Matrix6.Zero
	with open(fName) as f:
		flines = f.readlines()
	if block > 0:
		pass
	for i,l in enumerate(flines):
		if not l.startswith("#"):
			break
	lines = flines[i:i+6]
	vals = [[float(w) for w in l.split()] for l in lines]
	for r in xrange(6):
		for c in xrange(6):
			ret[r,c] = vals[r][c]
	return ret

def analyzeStiffnessMatrix(m):
	return analyzeComplianceMatrix(m.inverse())

def analyzeComplianceMatrix(m):
	es = [1/m[i,i] for i in (0,1,2)]
	eAvg = sum(es)/3.
	dE = max(abs(e-eAvg) for e in es)/eAvg
	nus = [-m[i,j]*es[i] for i,j in ((1,0),(2,0),(0,1),(2,1),(0,2),(1,2))]
	nuAvg = sum(nus)/6.
	#dNu = abs(max(abs(nu-nuAvg) for nu in nus)/nuAvg)
	dNu = max(abs(nu-nuAvg) for nu in nus)
	gs = [1/m[i,i] for i in (3,4,5)]
	gAvg = sum(gs)
	gi = eAvg/(2*(1+nuAvg))
	dG = max(abs(g-gi) for g in gs)/gi
	mi = m.inverse()
	dD = max(abs(mi[i,j]) for i,j in (
		(0,3),(0,4),(0,5),
		(1,3),(1,4),(1,5),
		(2,3),(2,4),(2,5),
		(3,0),(3,1),(3,2),(3,4),(3,5),
		(4,0),(4,1),(4,2),(4,3),(4,5),
		(5,0),(5,1),(5,2),(5,3),(5,4),
	)) / eAvg
	return OrthotropicMatProps(eAvg,dE,nuAvg,dNu,dG,dD)

class OrthotropicMatProps:
	def __init__(self,eAvg,dE,nuAvg,dNu,dG,dD):
		self.eAvg = eAvg
		self.dE = dE
		self.nuAvg = nuAvg
		self.dNu = dNu
		self.dG = dG
		self.dD = dD
def averageOrthotropicMatProps(props):
	n = len(props)
	return OrthotropicMatProps(
		eAvg = sum(p.eAvg for p in props) / n,
		dE = sum(p.dE for p in props) / n,
		nuAvg = sum(p.nuAvg for p in props) / n,
		dNu = sum(p.dNu for p in props) / n,
		dG = sum(p.dG for p in props) / n,
		dD = sum(p.dD for p in props) / n,
	)

def analyzeMatFromRFile(rf,block=0):
	return analyzeStiffnessMatrix(matFromFile(rfile(rf),block))

#
key = "stiffnessMatrix_oofem_isotropy_"
keyo = "preprocessed_{}".format(key)
fsIsotropy = [f for f in os.listdir('.') if f.startswith(key) and f.endswith(".dat")]
part = lambda f,l: f.partition(l)[2].partition(".dat")[0].partition("_")[0]
nums     = sorted(set(part(f,"_N") for f in fsIsotropy))
irs      = sorted(set(part(f,"_I") for f in fsIsotropy))
poissons = sorted(set(part(f,"_P") for f in fsIsotropy))
js       = sorted(set(part(f,"_J") for f in fsIsotropy))
for ir in irs:
	for poisson in poissons:
		data = []
		for num in nums:
			ds = [analyzeMatFromRFile("{}N{}_I{}_P{}_J{}".format(key,num,ir,poisson,j)) for j in js]
			data.append(averageOrthotropicMatProps(ds))
		with open(rfile("{}I{}_P{}".format(keyo,ir,poisson)),'w') as f:
			f.write("# num eAvg nuAvg dE dNu dG dD\n")
			f.writelines("{} {} {} {} {} {} {}\n".format(num,d.eAvg,d.nuAvg,d.dE,d.dNu,d.dG,d.dD) for num,d in zip(nums,data))

#
key = "stiffnessMatrix_oofem_macromicro"
keyo = "preprocessed_{}".format(key)
fs = [f for f in os.listdir('.') if f.startswith(key) and f.endswith(".dat")]
part = lambda f,l: f.partition(l)[2].partition(".dat")[0].partition("_")[0]
irs      = sorted(set(part(f,"_I") for f in fs),key=lambda v: float(v))
poissons = sorted(set(part(f,"_P") for f in fs),key=lambda v: float(v))
for ir in irs:
	data = [analyzeMatFromRFile("{}_P{}_I{}".format(key,poisson,ir)) for poisson in poissons]
	with open(rfile("{}_I{}".format(keyo,ir)),'w') as f:
		f.write("# poisson eAvg nuAvg\n")
		f.writelines("{} {} {}\n".format(poisson,d.eAvg,d.nuAvg) for poisson,d in zip(poissons,data))

key = "stiffnessMatrix_yade_macromicro"
keyo = "preprocessed_{}".format(key)
fs = [f for f in os.listdir('.') if f.startswith(key) and f.endswith(".dat")]
part = lambda f,l: f.partition(l)[2].partition(".dat")[0].partition("_")[0]
irs      = sorted(set(part(f,"_I") for f in fs),key=lambda v: float(v))
poissons = sorted(set(part(f,"_P") for f in fs),key=lambda v: float(v))
for ir in irs:
	data = [analyzeMatFromRFile("{}_P{}_I{}".format(key,poisson,ir),block=0) for poisson in poissons]
	with open(rfile("{}_I{}".format(keyo,ir)),'w') as f:
		f.write("# poisson eAvg nuAvg\n")
		f.writelines("{} {} {}\n".format(poisson,d.eAvg,d.nuAvg) for poisson,d in zip(poissons,data))
	data = [analyzeMatFromRFile("{}_P{}_I{}".format(key,poisson,ir),block=1) for poisson in poissons]
	with open(rfile("{}_I{}_theor".format(keyo,ir)),'w') as f:
		f.write("# poisson eAvg nuAvg\n")
		f.writelines("{} {} {}\n".format(poisson,d.eAvg,d.nuAvg) for poisson,d in zip(poissons,data))
######################################################################



######################################################################
def getDataFromFile(fName):
	with open(fName) as f:
		f.readline()
		lines = f.readlines()
	stresses, strains = [], []
	for l in lines:
		ls = l.split()
		stresses.append(float(ls[2]))
		strains.append(float(ls[0]))
	ft = max(stresses)
	fc = abs(min(stresses))
	gf = sum(s for s in stresses if s > 0.)
	for i,s in enumerate(stresses):
		if s == 0:
			break
	es = [stresses[i-j]/strains[i-j] for j in (1,2,3,4,5)]
	e = sum(es) / len(es)
	assert all(abs(e-ei)/e<5e-2 for ei in es), "{} {}".format(e,es)
	return e,ft,fc,gf
keyo = "preprocessed_validationBeygi".format(key)
experiments = ('l','h')
gradingCurves = (95,125,190)
hGeomIndexes = (1,2,3)
params = (".5,.5,.1",".5,.5,.05")
for ps in params:
	for exp in experiments:
		c1s = [],[],[],[]
		for gc in gradingCurves:
			c2s = [],[],[],[]
			for hi in hGeomIndexes:
				fn = rfile("validationBeygi_({})_{}_{:03d}_{}".format(ps,exp,gc,hi))
				vs = getDataFromFile(fn)
				for c,v in zip(c2s,vs):
					c.append(v)
			c2s = [sum(c)/len(c) for c in c2s]
			for c1,c2 in zip(c1s,c2s):
				c1.append(c2)
		vs0 = [v[0] for v in c1s]
		with open(rfile("{}_({})_{}".format(keyo,ps,exp)),'w') as f:
			f.write("# maxAggreg e ft fc gf eRel ftRel fcRel gfRel\n")
			for i,gc in enumerate(gradingCurves):
				vs = e,ft,fc,gf = [v[i] for v in c1s]
				er,ftr,fcr,gfr = [v/v0 for v,v0 in zip(vs,vs0)]
				f.write("{} {} {} {} {} {} {} {} {}\n".format(gc,e,ft,fc,gf,er,ftr,fcr,gfr))
######################################################################
