import sys
import subprocess
from math import log
from minieigen import Vector6,Matrix6

yadeBatch = "yade-2017.01a-batch -j 4 --job-threads 1 --log /tmp/$.%.log --disable-pynotify"
oofem = "oofem-2.3"
extractor = "extractor-2.3"

nSteps = (
	(500 ,),
	(1000,),
	(1500,),
	(2000,),
	(2500,),
	(3000,),
	(3500,),
	#
	(1500,-2000),
	(2000,-2000),
	(2500,-2000),
	(3000,-1350),
	(3500,-900),
)
nStepsMax = 4000.

class Mapper:
	def __init__(self,name="sequential_coupling"):
		self.name = name
	def writeLinesToFile(self,fName,lines):
		with open(fName,"w") as f:
			f.writelines(l+"\n" for l in lines)
	def writeToFile(self,fName,content):
		with open(fName,"w") as f:
			f.write(content)
	def readFile(self,fName):
		with open(fName) as f:
			ret = f.read()
		return ret
	def runCommand(self,cmd,**kw):
		r = subprocess.Popen(cmd.split(),**kw).wait()
		if r:
			sys.exit()
	#
	def yadeTab(self):
		return "/tmp/{}.tab".format(self.name)
	def yadeOut(self,i):
		return "/tmp/{}_yade_{:03d}".format(self.name,i)
	def oofemBase(self,i):
		return "/tmp/{}_oofem_{:03d}".format(self.name,i)
	def runYade(self):
		tabname = self.yadeTab()
		nStepsStr = lambda ns: str(tuple(abs(n) for n in ns)).replace(" ","")
		signsStr  = lambda ns: str(tuple(-.5 if n<0 else 1 for n in ns)).replace(" ","")
		tablines = ["outBase nSteps signs"] + ["'{}' {} {}".format(self.yadeOut(i),nStepsStr(ns),signsStr(ns)) for i,ns in enumerate(nSteps)]
		self.writeLinesToFile(tabname,tablines)
		self.runCommand("{} {} uniax_yade.py".format(yadeBatch,tabname))
	def doMapping(self):
		oofeminin = self.readFile("uniax_oofem.in.in")
		oofemgpin = self.readFile("uniax_oofem.gp.in")
		#
		for i,ns in enumerate(nSteps):
			base = self.oofemBase(i)
			stress,damage,kappaP = self.dem2fem(i)
			oofemSteps = int(100*(nStepsMax - ns[0] + (-.125*ns[1] if len(ns)==2 else 0))/nStepsMax)
			oofemSteps = min(110,oofemSteps+20)
			oofemin = oofeminin.format(base+".out",oofemSteps,base+".gp")
			oofemgp = oofemgpin.format(
				" ".join(str(v) for v in stress),
				damage,
				kappaP,
			)
			self.writeToFile(base+".in",oofemin)
			self.writeToFile(base+".gp",oofemgp)
	def dem2fem(self,index):
		stress,dmgs = [line.split() for line in self.readFile("/tmp/{}_yade_{:03d}_final.dat".format(self.name,index)).splitlines()]
		stress = Vector6([float(w) for w in stress])
		dmg1,dmg2,dmg3 = [float(w) for w in dmgs]
		dmgv = (dmg1+dmg2+dmg3)/3.
		dmg = .85*dmg1 + .15*dmg3
		dmg = max(0,dmg)
		dmg = (2.09*dmg)**4.7
		dmg = min(1,dmg)
		kappaP = 0.
		if dmg < 0.0005:
			kappaP = .3+.45*dmg/0.0005
			dmg = 0.
		else:
			pass
		print index, dmg, kappaP
		return stress,dmg,kappaP
	def runOofem(self):
		for i,ns in enumerate(nSteps):
			base = self.oofemBase(i)
			with open("{}.redirect".format(base),"w") as out:
				self.runCommand("{} -f {}.in".format(oofem,base),stdout=out)
			#self.runCommand("{} -f {}.in".format(oofem,base))
			with open("{}.dat".format(base),"w") as out:
				self.runCommand("{} -f {}.in".format(extractor,base),stdout=out)
	def __call__(self):
		self.runYade()
		self.doMapping()
		self.runOofem()

mapper = Mapper()
mapper()
