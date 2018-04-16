# used for text/main/plots/aux/validationBeygi_experiment*.dat
e = (
	28.1,
	31.0,
	32.3,
	38.6,
	39.5,
	40.0,
)

ft = (
	3.38,
	3.27,
	3.16,
	4.59,
	4.43,
	3.93,
)

fc = (
	38.2,
	44.9,
	48.0,
	75.9,
	76.9,
	80.0,
)

gf = (
	107.3,
	118.7,
	144.2,
	114.2,
	128.0,
	152.2,
)

def splitAndNormalize(v):
	vlo = v[:3]
	vho = v[3:]
	vln,vhn = [[v/vs[0] for v in vs] for vs in (vlo,vho)]
	return (vlo,vln),(vho,vhn)
ess  = splitAndNormalize(e)
ftss = splitAndNormalize(ft)
fcss = splitAndNormalize(fc)
gfss = splitAndNormalize(gf)

names = ["/tmp/validationBeygi_experiment_{}.dat".format(v) for v in ("l","h")]
for name,es,fts,fcs,gfs in zip(names,ess,ftss,fcss,gfss):
	with open(name,"w") as f:
		f.write("# maxAggreg e ft fc gf erel ftrel fcrel gfrel\n")
		vs = (es,fts,fcs,gfs)
		vs0 = [v[0] for v in vs]
		vs1 = [v[1] for v in vs]
		vs = vs0 + vs1
		for i,(e,ft,fc,gf,er,ftr,fcr,gfr) in enumerate(zip(*vs)):
			gc = (95,125,190)[i]
			f.write("{} {} {} {} {} {} {} {} {}\n".format(gc,e,ft,fc,gf,er,ftr,fcr,gfr))
