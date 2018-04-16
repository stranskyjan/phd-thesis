import sys
import subprocess

oofemBase = "/tmp/sequential_coupling_oofem_plain"
yadeBase = "/tmp/sequential_coupling_yade_plain"

def readFile(fName):
	with open(fName) as f:
		ret = f.read()
	return ret

def writeFile(fName,content):
	with open(fName,"w") as f:
		f.write(content)

def runCommand(cmd,**kw):
	r = subprocess.Popen(cmd.split(),**kw).wait()
	if r:
		sys.exit()

if 1:
	oofeminin = readFile("uniax_oofem.in.in")
	oofemin = oofeminin.format(oofemBase+".out",100,oofemBase+".gp")
	#
	oofemgpin = readFile("uniax_oofem.gp.in")
	z = "0"
	oofemgp = oofemgpin.format(" ".join(z for _ in xrange(6)),z,z)
	#
	writeFile(oofemBase+".in",oofemin)
	writeFile(oofemBase+".gp",oofemgp)
	#
	with open(oofemBase+".redirect","w") as out:
		runCommand("oofem-2.3 -f {}.in".format(oofemBase),stdout=out)
	with open(oofemBase+".dat","w") as out:
		runCommand("extractor-2.3 -f {}.in".format(oofemBase),stdout=out)

if 1:
	runCommand("yade-2017.01a -x uniax_yade.py")
