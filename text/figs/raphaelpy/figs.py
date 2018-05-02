from raphaelpy import *
from math import cos,sin,degrees,radians
from minieigen import Vector2, MatrixX, Matrix3, Vector3

def Matrix2(a,b,c,d):
	return MatrixX([a,b],[c,d])
Matrix2_Identity = Matrix2(1,0,0,1)
Matrix2_Zero = Matrix2(0,0,0,0)

PLOTTEXT = True
PLOTTEXT = False

######################################################################
# common settings
######################################################################
def Paper(f,w=640,h=480):
	print
	print f
	if not f.endswith('.svg'):
		f += '.svg'
	f = "/tmp/PhD_thesis_Stransky_2018_"+f
	ret = Raphael(f,w,h)
	return ret

Raphael.el.stroke = lambda self,v: self.attr(stroke=v)
Raphael.el.fill = lambda self,v: self.attr(fill=v)
Raphael.el.normal = lambda self: self.attr(stroke_width=2)
Raphael.el.mediumThick = lambda self: self.attr(stroke_width=3)
Raphael.el.thick = lambda self: self.attr(stroke_width=5)
Raphael.el.ultraThick = lambda self: self.attr(stroke_width=8)
def _arrow(self,mask=1):
	arrow = "classic-long"
	if mask & 1:
		self.attr(arrow_end=arrow)
	if mask & 2:
		self.attr(arrow_start=arrow)
	return self
Raphael.el.arrow = _arrow
Raphael.el.dotted = lambda self: self.attr(stroke_dasharray=(2,2))
Raphael.el.dashed = lambda self: self.attr(stroke_dasharray=(5,3))

def _sphere(self,x,y,r,color="#000"):
	ret = self.circle(x,y,r).stroke(null).fill("r(.3,.3)#fff-{}".format(color))
	ret._gradient.attr(cx=.3,cy=.3)
	return ret
Raphael.fn.sphere = _sphere

def papertext(x,y,text):
	if PLOTTEXT:
		paper.text(x,y,text)
	else:
		w,h = [float(v) for v in (paper.width, paper.height)]
		x = (x-w) / w
		y = (h-y) / w
		print r"\put({},{}){{\makebox(0,0){{{}}}}}".format(x,y,text)
def papertext2(xy,text):
	x,y = xy
	papertext(x,y,text)

######################################################################


######################################################################
# testing picture
######################################################################
paper = Paper("test")
paper.rect(0,0,640,480)
# lines
x,y,l,dy = 90,10,40,10
paper.path(["M",x,y,"h",l])
y += dy
paper.path(["M",x,y,"h",l]).normal()
y += dy
paper.path(["M",x,y,"h",l]).mediumThick()
y += dy
paper.path(["M",x,y,"h",l]).thick()
y += dy
paper.path(["M",x,y,"h",l]).normal().dotted()
y += dy
paper.path(["M",x,y,"h",l]).normal().dashed()
y += dy
paper.path(["M",x,y,"h",l]).normal().arrow()
y += dy
paper.path(["M",x,y,"h",l]).normal().arrow(2)
y += dy
paper.path(["M",x,y,"h",l]).normal().arrow(3)
y += dy
paper.path(["M",x,y,"h",l]).normal().dotted().stroke('red')
y += dy
paper.path(["M",x,y,"h",l]).normal().arrow().stroke('red')
#
paper.sphere(200,100,50,"#440")
#
paper.save()
######################################################################


######################################################################
# periodic packing
######################################################################
w,h = 520,500
d = 200
trans = Vector2(165,350)
ps = (
	Vector2(0, 0),
	Vector2(d, 0),
	Vector2(d,-d),
	Vector2(0,-d),
)
cs1 = (
	Vector2( 35, -50),
	Vector2(135, -65),
	Vector2(150,-165),
	Vector2( 50,-150),
)
kss = (
	((1,0),(0,-1),(1,-1)),
	((-1,0),(0,-1)),
	((-1,0),(0,1),(-1,1)),
	((1,0),(0,1)),
)
rs = (50, 50, 50, 50)
links1 = (
	(0,4),
	(4,7),
	(7,11),
	(11,0),
	(4,11),
)
links2 = (
	(0,5),(0,10),(0,13),
	(4,1),(4,9),
	(7,3),(7,6),(7,12),
	(11,2),(11,8),
)
links3 = (
	(1,12),(1,9),
	(3,12),(3,6),
	(2,6),(2,8),
	(5,8),(5,10),
	(13,10),(13,9),
)
for index in (0,1):
	trsf = Matrix2_Identity if index == 0 else Matrix2(1.1,-.2, 0,1.1)
	paper = Paper("peri_packing_2d_illustration_{}".format(index),w,h)
	p0,p1,p2,p3 = [trsf*p+trans for p in ps]
	paper.path(["M",p0[0],p0[1],"L",p1[0],p1[1],"L",p2[0],p2[1],"L",p3[0],p3[1],"Z"]).normal().dotted()
	cs = []
	for ii,(c,r,ks) in enumerate(zip(cs1,rs,kss)):
		c = c + trans
		cs.append(c)
		paper.circle(c[0],c[1],r).normal().fill("#bbb")
		if ii == 0:
			papertext(c[0],c[1],r"$\particleA$")
		if ii == 2:
			papertext(c[0],c[1],r"$\particleB$")
		for ik,k in enumerate(ks):
			k = Vector2(k[0],k[1])
			cc = c + trsf*(d*k)
			cs.append(cc)
			paper.circle(cc[0],cc[1],r).fill("#eee")
			if ii==0 and ik == 2:
				papertext(cc[0],cc[1],r"$\particleA'$")
			if ii==2 and ik == 2:
				papertext(cc[0],cc[1],r"$\particleB'$")
	for ij in links1:
		c1,c2 = [cs[i] for i in ij]
		paper.path(["M",c1[0],c1[1],"L",c2[0],c2[1]]).thick()
	for ij in links2:
		c1,c2 = [cs[i] for i in ij]
		paper.path(["M",c1[0],c1[1],"L",c2[0],c2[1]]).normal()
	for ij in links3:
		c1,c2 = [cs[i] for i in ij]
		paper.path(["M",c1[0],c1[1],"L",c2[0],c2[1]])
	paper.save()


######################################################################
# contact displacements
######################################################################
w,h = 550,200
c1 = Vector2(100,100)
c2 = c1 + (100,0)
r = 50
dd = Vector2(250,0)
u1 = Vector2(0,20)
u2 = Vector2(20,-20)
p1 = .1
p2 = .2
def circ(ce,d,u,p):
	c,s = [f(p) for f in cos,sin]
	for v in (d,u):
		if v is not None:
			ce = ce + v
	paper.circle(ce[0],ce[1],r).stroke(null).fill("#bbb")
	paper.path([
		"M",ce[0]-r*c,ce[1]-r*s,"L",ce[0]+r*c,ce[1]+r*s,
		"M",ce[0]-r*s,ce[1]+r*c,"L",ce[0]+r*s,ce[1]-r*c,
	]).dotted()
def line(p1,p2):
	return paper.path(["M",p1[0],p1[1],"L",p2[0],p2[1]])
cc1,cc2 = [c+dd+u for c,u in zip((c1,c2),(u1,u2))]
for mode in ("normal","shear"):
	paper = Paper("contact_displacement_{}".format(mode),w,h)
	#
	circ(c1,None,None,0)
	circ(c2,None,None,0)
	line(c1,c2).normal()
	papertext(c1[0],c1[1],r"$\particlePosition_\particleA^0$")
	papertext(c2[0],c2[1],r"$\particlePosition_\particleB^0$")
	#
	circ(c1,dd,u1,p1)
	circ(c2,dd,u2,p2)
	line(cc1,cc2).normal()
	papertext(cc1[0],cc1[1],r"$\particlePosition_\particleA$")
	papertext(cc2[0],cc2[1],r"$\particlePosition_\particleB$")
	#
	if mode == "normal":
		cc = (cc2-cc1).normalized()
		v1 = cc1 + cc*r
		v2 = cc2 - cc*r
		line(v1,v2).ultraThick()
		cc = .5*(cc1+cc2)
		papertext(cc[0],cc[1],r"$\linkDisplacementNormal$")
	else:
		ccd = (cc2-cc1).normalized()
		t = Vector2(ccd[1],-ccd[0])
		cc = .5*(cc1+cc2)
		d = 50
		line(cc+d*t,cc-d*t).dotted()
		ds = (25,27)
		vs = [None,None]
		ss = [None,None]
		for i,(cc,p,d) in enumerate(zip((cc1,cc2),(p1,p2),ds)):
			c,s = [f(p) for f in cos,sin]
			c,s = [v*(1 if i==0 else -1) for v in (c,s)]
			v = Vector2(c,s)
			dot = v.dot(ccd)
			if i == 1:
				dot *= -1
			d = .5*(cc2-cc1).norm()
			d = d/dot - r
			s = cc + r*v
			v = s + d*v
			ss[i] = s
			vs[i] = v
		v1,v2 = vs
		s1,s2 = ss
		line(v1,v2).ultraThick()
		line(s1,v1).dotted()
		line(s2,v2).dotted()
		papertext(v2[0],v2[1],r"$\linkDisplacementShearVector$")
	#
	paper.save()


######################################################################
# link gcs lcs
######################################################################
w,h = 900,280
dx = Vector2(450,0)
c1 = Vector2(170,150)
c2 = Vector2(340,100)
n = (c2-c1).normalized()
t = Vector2(n[1],-n[0])
cc = .5*(c1+c2)
ccd = cc + dx
r = 80
O1 = Vector2(20,250)
O2 = O1 + dx
paper = Paper("link_gcs_lcs",w,h)
da = 50
xlabels = (
	(r"$\displacement_{\particleA1}$",r"$\displacement_{\particleB1}$"),
	(r"$\linkDisplacementNormal_\particle$",r"$\linkDisplacementShear[1]")
)
ylabels = (
	(r"$\displacement_{\particleA2}$",r"$\displacement_{\particleB2}$"),
	(r"$\linkDisplacementNormal$",r"$\linkDisplacementShear[1]")
)
for di,d in enumerate((Vector2.Zero,dx)):
	for ci,c in enumerate((c1,c2)):
		c = c+d
		paper.circle(c[0],c[1],r).fill("#ddd")
		if di == 0:
			e = c + da*Vector2.UnitX
			line(c,e).arrow().mediumThick()
			papertext(e[0],e[1],xlabels[di][ci])
			e = c - da*Vector2.UnitY
			line(c,e).arrow().mediumThick()
			papertext(e[0],e[1],ylabels[di][ci])
	if di == 1:
		e = ccd+da*n
		line(ccd,e).arrow().mediumThick()
		papertext(e[0],e[1],r"$\linkDisplacementNormal$")
		e = ccd+da*t
		line(ccd,e).arrow().mediumThick()
		papertext(e[0],e[1],r"$\linkDisplacementShear[1]$")
	line(c1+d,c2+d)
#
line(O1,O1+da*Vector2.UnitX).mediumThick().arrow()
papertext(O1[0]+da,O1[1],"$x_1$")
line(O1,O1-da*Vector2.UnitY).mediumThick().arrow()
papertext(O1[0],O1[1]-da,"$x_2$")
e = O2 + da*n
line(O2,e).mediumThick().arrow()
papertext(e[0],e[1],r"$\linkGlobToLocE_\normalComponent$")
e = O2 + da*t
line(O2,e).mediumThick().arrow()
papertext(e[0],e[1],r"$\linkGlobToLocE_{\shearComponent1}$")
#
papertext(c1[0],c1[1],r"$\particlePosition_\particleA$")
papertext(c2[0],c2[1],r"$\particlePosition_\particleB$")
#
paper.save()



######################################################################
# link gcs lcs
######################################################################
w,h = 800,400
paper = Paper("virtual_work_of_internal_forces",w,h)
paper.save()


######################################################################
# coupling illustration surface
######################################################################

def particles(dd,scale=30):
	ps = (
		(2.3, 0.7, 1.0),
		(3.4, 0.0, 1.1),
		(2.1, 2.4, 1.0),
		(3.4, 2.1, 1.0),
		(2.1, 4.7, 1.0),
		(3.3, 4.0, 1.1),
		(2.2, 6.9, 1.0),
		(3.1, 6.4, 1.1),
		(0.5, 0.6, 1.0),
		(1.0, 0.1, 1.2),
		(0.3, 2.8, 1.0),
		(1.5, 2.2, 1.0),
		(0.0, 4.7, 1.0),
		(1.1, 4.1, 1.0),
		(0.5, 6.5, 1.0),
		(1.2, 6.4, 1.2),
	)
	s = scale
	for x,y,r in ps:
		y = 6-y
		x,y,r = [s*v for v in (x,y,r)]
		x,y = [v+d for v,d in zip((x,y),dd)]
		paper.sphere(x,y,r,"#777")

def box(O,fem=False,onlyLeft=False):
	w,h,tx,ty = 120,260,50,25
	if not onlyLeft:
		paper.path(["M",O[0],O[1],"h",w,"v",-h,"h",-w,"Z"]).normal().fill("#777")
		paper.path(["M",O[0],O[1]-h,"h",w,"l",-tx,-ty,"h",-w,"Z"]).normal().fill("#bbb")
		if fem:
			paper.path([
				"M",O[0],O[1]-.5*h,"l",w,+.5*h,
				"M",O[0],O[1]-.5*h,"l",w,    0,
				"M",O[0],O[1]-.5*h,"l",w,-.5*h,
				"M",O[0]+w,O[1]-h,"l",-w-tx,-ty,
			]).normal()
	paper.path(["M",O[0],O[1],"v",-h,"l",-tx,-ty,"v",h,"Z"]).normal().fill("#ddd")
	if fem:
		paper.path([
			"M",O[0],O[1]-.5*h,"l",-tx,+.5*h-ty,
			"M",O[0],O[1]-.5*h,"l",-tx,     -ty,
			"M",O[0],O[1]-.5*h,"l",-tx,-.5*h-ty,
		]).normal()

w,h = 650,750
paper = Paper("coupling_illustration_surface",w,h)
#
dw,dh = 150,400
O = Vector2(330,300)
Op = O - (140,220)
box(O)
particles(Op)
#
dd = 20
for sign,d in zip((-1,1),(40,0)):
	paper.path(["M",O[0],O[1]+dd,"v",30,"h",sign*(dw+d),"v",30]).thick().arrow()
#
ddd = Vector2(-dw,dh)
O += ddd
Op += ddd
box(O,onlyLeft=True,fem=True)
particles(Op)
#
O += (2*dw,0)
box(O,fem=True)
#
O += (20,30)
papertext(O[0],O[1],"FEM")
O += (-2*dw-90,0)
papertext(O[0],O[1],"DEM")
#
c = Vector2(310,540)
dx,dy = 80.,20.
ddy = 70.
r = 100.
paper.path(["M",c[0]-dx,c[1]-dy,"a",r,r,0,0,1,2*dx,0]).thick().arrow()
paper.path(["M",c[0]+dx,c[1]+dy,"a",r,r,0,0,1,-2*dx,0]).thick().arrow()
papertext(c[0],c[1]-dy-ddy,"load")
papertext(c[0],c[1]+dy+ddy,"displacement")
#
paper.save()


######################################################################
# coupling illustration volume
######################################################################

def particles(dd,scale=60):
	ps = (
		(+0.50, +0.37, 0.3),
		(+0.30, +1.00, 0.28),
		(+0.50, -0.40, 0.3),
		(+1.00, +0.00, 0.3),
		(+0.90, +0.90, 0.3),
		(+1.45, +1.06, 0.25),
		(+1.40, +0.50, 0.3),
		(+1.10, -0.60, 0.3),
		(+1.60, -0.10, 0.3),
		(+1.70, -0.70, 0.3),
		(+1.30, -1.20, 0.3),
		(+1.85, -1.40, 0.25),
		(+1.40, -1.75, 0.25),
		(+0.60, -1.00, 0.3),
		(+0.26, -1.45, 0.25),
		(+0.83, -1.60, 0.3),
		#
		(0., -0.80, 0.3,),
		(0., +0.57, 0.23,),
		(0., +0.00, 0.3),
	)
	s = scale
	for x,y,r in ps:
		y = 1-y
		x,y,r = [s*v for v in (x,y,r)]
		y += dd[1]
		paper.sphere(dd[0]+x,y,r,"#666")
		paper.sphere(dd[0]-x,y,r,"#666")

w,h = 450,300
paper = Paper("coupling_illustration_volume",w,h)
O = Vector2(.5*w,30)
w,h = 120,120
x0 = O[0]-1.5*w
for xi in (0,1,2):
	for yi in (0,1):
		if xi==1 and yi==0:
			continue
		x,y = x0+xi*w,O[1]+yi*h
		paper.rect(x,y,w,h).normal().fill("#ddd")
		paper.path(["M",x,y,"l",w,h]).normal()
particles(O)
paper.save()


######################################################################
# coupling illustration multiscale
######################################################################
c = (600,170)
scale=60
ps = (
	(+0.00, +0.00, 0.50),
	(+1.00, +0.20, 0.50),
	(-1.00, +0.10, 0.50),
	(+0.30, +1.00, 0.50),
	(+1.30, +1.20, 0.50),
	(-0.70, +1.10, 0.50),
	(+0.32, -1.00, 0.50),
	(+1.31, -0.80, 0.50),
	(-0.70, -0.90, 0.50),
)
ps2 = []
for x,y,r in ps:
	x += -.5
	y += -.4
	xy = Vector2(x,y)
	xy,r = [scale*v for v in (xy,r)]
	xy += c
	ps2.append((xy,r))
	x,y = xy
ps = ps2

w,h = 800,300
paper = Paper("coupling_illustration_multiscale",w,h)
d = 100
r = 170
dd = 2*.9*d
paper.path([
	"M",c[0]-.5*dd,c[1]-.5*dd,
	"a",r,r,0,0,1,+dd,0,
	"a",r,r,0,0,0,0,+dd,
	"a",r,r,0,0,0,-dd,0,
	"a",r,r,0,0,1,0,-dd,
	"Z",
]).fill("#ddd").normal()
edges = []
for i,j in (
		(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),
		(1,3),(1,4),(1,6),(1,7),
		(2,3),(2,5),(2,6),(2,8),
		(3,4),(3,5),(6,7),(6,8),
	):
	edges.append((ps[i][0],ps[j][0]))
for i,j in ((1,2),(4,5),(7,8),(1,5),(1,8),(4,2),(7,2)):
	edges.append((ps[i][0],ps[j][0]+(dd,0)))
	edges.append((ps[j][0],ps[i][0]-(dd,0)))
for i,j in ((3,6),(4,7),(5,8),(3,7),(3,8),(4,6),(5,6)):
	edges.append((ps[i][0],ps[j][0]+(0,dd)))
	edges.append((ps[j][0],ps[i][0]-(0,dd)))
edges.append((ps[4][0],ps[8][0]+(+dd,+dd)))
edges.append((ps[5][0],ps[7][0]+(-dd,+dd)))
edges.append((ps[7][0],ps[5][0]+(+dd,-dd)))
edges.append((ps[8][0],ps[4][0]+(-dd,-dd)))
for v1,v2 in edges:
	line(v1,v2).thick().stroke("#444")
for (x,y),r in ps:
	paper.sphere(x,y,r,"#666")
#
p1 = Vector2(30,50)
p2 = p1 + (250,100)
p3 = p1 + (20,200)
paper.path([
	"M",p1[0],p1[1],
	"L",p2[0],p2[1],
	"L",p3[0],p3[1],
	"Z",
]).mediumThick().fill("#bbb")
c = (p1+p2+p3)/3.
paper.circle(c[0],c[1],10).stroke(null).fill("black")
papertext(c[0],c[1],"IP")
dx,dy,ddy = 20,20,30
l = 300
r = 200
paper.path(["M",c[0]+dx,c[1]-dy,"a",r,r,0,0,1,l,-ddy]).mediumThick().arrow()
paper.path(["M",c[0]+dx,c[1]+dy,"a",r,r,0,0,0,l,+ddy]).mediumThick().arrow(2)
dy = 125
papertext(c[0]+dx+.6*l,c[1]-dy,"strain")
papertext(c[0]+dx+.6*l,c[1]+dy,"stress")
#
paper.save()


######################################################################
# coupling illustration multiscale
######################################################################
w,h = 600,320
paper = Paper("coupling_illustration_contact",w,h)
grains = (
	((0,0), (0,-2), (1,-1), (1,1), (0,1), (-1,1)),
	((1,0), (1,0), (2,1), (-2,1), (-1,-1)),
	((2,-1), (0,-1), (1,-1), (1,0), (0,2), (-1,1.5)),
	((4,1), (1,0), (1,1), (-2,1), (-1,-1)),
	((4,-1), (1,-1), (2,2), (-2,1), (-1,-1)),
	((7,0), (1,1), (0,1), (-1,1), (-1,0), (0,-2)),
	((.5,-3.5), (1,1), (1,0), (0,-1), (-1,-1)),
	((2.5,-3.5), (1,.5), (1,-1.5), (-2,0)),
	((4,-3), (1,1), (2,-1), (-1,-1), (-1,0), (-1,1)),
	((6,-1), (0,-1.5), (2,0), (0,.5), (-1.25,1.25)),
	((7.5,.5), (-.5,-1), (.5,-1), (1,0), (0,1), (-1,1)),
)
fem = (
	((-1.25,-2.5), (3.75,0)),
	((-2.5,-5), (7.5,0)),
	((-1.25,-7.5), (6.25,0)),
	((-1.25,-2.5), (1.25,-2.5), (2.5,2.5), (.25,-2.5)),
	((-1.25,-7.5), (1.25,2.5), (1.25,-2.5), (1.5,2.5), (2.25,-2.5)),
	((0,-10), (1.25,2.5), (1.75,-2.5), (2.0,2.5)),
)
macrograin = ((-2.5,-5), (2.5,-5), (5,0), (0,5), (-5,5))
#
s = 25
#
dd1 = Vector2(20,130)
for grain in grains:
	ps = [s*Vector2(p[0],-p[1]) for p in grain]
	p0 = dd1 + ps[0]
	paper.path(["M",p0[0],p0[1]]+sum((["l",p[0],p[1]] for p in ps[1:]),[])+["Z"]).fill("#ddd")
#
dd2 = Vector2(430,20)
paper.path(["M",dd2[0],dd2[1]] + sum((["l",s*v[0],-s*v[1]] for v in macrograin),[]) + ["Z"]).fill("#aaa")
for elem in fem:
	ps = [s*Vector2(p[0],-p[1]) for p in elem]
	p0 = dd2 + ps[0]
	paper.path(["M",p0[0],p0[1]]+sum((["l",p[0],p[1]] for p in ps[1:]),[]))
#
x,y,dx,dy,dy1,dy2 = 240,145,160,25,100,100
paper.path([
	"M",x,y-dy,"l",dx,-dy1,
	"M",x,y+dy,"l",dx,+dy2,
]).normal().dotted()
#
y = 300
papertext(dd1[0]+100,y,"DEM")
papertext(dd2[0]+50 ,y,"FEM")
paper.save()



######################################################################
# coupling seq per perticle damage
######################################################################
w,h = 600,600
paper = Paper("coupling_seq_per_particle_damage",w,h)
r = 90
r2 = 8
ns = ((0,-1),(1,-.3),(.7,1),(-.7,1),(-1,-.3))
ns = [Vector2(n).normalized() for n in ns]
ds = (1.10, 1.20, 1.15, 1.10, 1.20)
c = Vector2(300,300)
dn = .7
paper.circle(c[0],c[1],r).normal().fill("#ccc")
for i,(d,n) in enumerate(zip(ds,ns)):
	cc = c + 2*r*d*n
	paper.circle(cc[0],cc[1],r).normal().dashed()
	line(c,cc).normal().dotted()
	cc = .5*(c+cc)
	ne = cc + dn*r*n
	line(cc,ne).thick().arrow()
	paper.circle(cc[0],cc[1],r2).stroke(null).fill("black")
	if i==4:
		papertext(ne[0],ne[1],r"$\normalVector^\contact$")
		papertext(cc[0],cc[1],r"$\damageA^\contact$")
paper.save()


######################################################################
# myaxes
######################################################################
w,h = 130,110
paper = Paper("myaxes",w,h)
c = Vector2(.5*w,.65*h)
d = 50
paths = (
	paper.path(["M",c[0],c[1],"h",d]),
	paper.path(["M",c[0],c[1],"v",-d]),
	paper.path(["M",c[0],c[1],"l",-.5*d,.5*d]),
)
for p in paths:
	p.mediumThick().arrow()
paper.save()


######################################################################
# mcpm itz possibilites
######################################################################
w,h = 640,480
ellx,elly = 230,150
rot = -.4
r = .1
sp = (
	(0.192812 , 0.854125),
	(0.592402 , 0.731518),
	(0.812824 , 0.407699),
	(0.780618 , 0.210231),
	(0.0183325, 0.39559),
	(0.230402 , 0.0552411),
	(0.176044 , 0.257497),
	(0.149321 , 0.654116),
	(0.001989 , 0.789624),
	(0.835276 , 0.991985),
	(0.356561 , 0.606522),
	(0.597622 , 0.129374),
	(0.208029 , 0.462331),
	(0.402615 , 0.404237),
	(0.436309 , 0.0029154),
	(0.590816 , 0.334749),
	(0.748279 , 0.597032),
	(0.952525 , 0.584826),
	(0.988632 , 0.187589),
	(0.799175 , 0.79508),
	(0.0408217, 0.987251),
	(0.386354 , 0.200285),
	(0.556499 , 0.534499),
	(0.622893 , 0.929609),
	(0.405703 , 0.804813),
)
class Sphere:
	def __init__(self,c,r):
		self.center = Vector2(c)
		self.radius = r
		self.extra = {}
	def clone(self,shift=Vector2.Zero):
		return Sphere(self.center+shift,self.radius)
	def toTuple(self):
		return self.center,self.radius
	def toPaper(self,paper,**kw):
		x,y = self.center
		paper.circle(x,y,self.radius).attr(**kw)
	def isClose(self,other,factor):
		d = (self.center-other.center).norm()
		return d < factor*(self.radius+other.radius)
scale = 300
d0 = (125,55)
sphs = [Sphere(scale*Vector2(x,y)-d0,scale*r) for x,y in sp]
sphs = [s.clone(d) for s in sphs for d in ((0,0),(scale,0),(2*scale,0),(0,scale),(scale,scale),(2*scale,scale))]
c,s = [f(rot) for f in cos,sin]
m = Matrix2(c,s,-s,c)
for s in sphs:
	c = Vector2(s.center)
	c = c - (.5*w,.5*h)
	c = m*c
	x,y = c
	ell = pow(x/ellx,2) + pow(y/elly,2)
	if ell <= 1:
		s.extra["aggreg"] = True
n = len(sphs)
intrs = []
for i in xrange(n-1):
	s1 = sphs[i]
	for j in xrange(i+1,n):
		s2 = sphs[j]
		if s1.isClose(s2,1.5):
			intrs.append((s1,s2))
for index in (0,1,2):
	paper = Paper("mcpm_itz_possibilities_{}".format(index),w,h)
	for s in sphs:
		a = s.extra.get("aggreg")
		fill = "#999" if a and index in (0,2) else "#ddd"
		s.toPaper(paper,fill=fill)
	for s1,s2 in intrs:
		l = line(s1.center,s2.center)
		a1,a2 = [s.extra.get("aggreg") for s in (s1,s2)]
		if index in (0,1):
			continue
		if (a1 and not a2) or (not a1 and a2):
			l.attr(stroke_width=6.5)
	#
	e = paper.ellipse(.5*w,.5*h,ellx,elly).attr(transform="rotate({},{},{})".format(degrees(rot),.5*w,.5*h))
	if index == 1:
		e.thick().dashed()
	else:
		e.normal().dashed()
	paper.save()



######################################################################
# spherical coordinate system
######################################################################
w,h = 535,535
paper = Paper("spherical_coordinate_system",w,h)
u = 25
n = 5
dd = 1
O = Vector2(.36*w,.65*h)
paper.path(["M",O[0],O[1],"h", 2*n*u+2*dd*u]).mediumThick().arrow()
paper.path(["M",O[0],O[1],"v",-2*n*u-2*dd*u]).mediumThick().arrow()
paper.path(["M",O[0],O[1],"l",-n*u-dd*u,+n*u+dd*u]).mediumThick().arrow()
papertext(O[0]+2*n*u+2*dd*u,O[1],"$y$")
papertext(O[0],O[1]-2*n*u-2*dd*u,"$z$")
papertext(O[0]-n*u-dd*u,O[1]+n*u+dd*u,"$x$")
for dir in (0,1,2):
	for i in xrange(1,n+1):
		paper.path([
			"M",O[0]+2*i*u,O[1],"v",-2*n*u,
			"M",O[0]+2*i*u,O[1],"l",-n*u,n*u,
			"M",O[0],O[1]-2*i*u,"h",2*n*u,
			"M",O[0],O[1]-2*i*u,"l",-n*u,n*u,
			"M",O[0]-i*u,O[1]+i*u,"h",2*n*u,
			"M",O[0]-i*u,O[1]+i*u,"v",-2*n*u,
		]).dotted()
c0 = O + (2*2.5*u,2*1.5*u)
c1 = O + (2*2.5*u,2*1.5*u-2*5*u)
v = O + (0,2*5*u)
paper.path([
	"M",O[0],O[1],"L",c0[0],c0[1],
	"M",O[0],O[1],"L",c1[0],c1[1],
	"M",c0[0],c0[1],"L",c1[0],c1[1],
]).normal().dashed()
paper.circle(c1[0],c1[1],5).stroke(null).fill("black")
papertext(c1[0],c1[1],r"$(\rho,\zenithAngle,\azimuthAngle$)")
d = 5*u
e = O+.5*(c0-O)
paper.path(["M",O[0]-.5*d,O[1]+.5*d,"A",1.5*d,d,0,0,0,e[0],e[1]]).mediumThick().arrow()
papertext(O[0]+1.5*u,O[1]+3*u,r"$\azimuthAngle$")
d = 2*u
e = O+.5*(c1-O)
paper.path(["M",O[0],O[1]-3*d,"A",2*d,3*d,0,0,1,e[0],e[1]]).mediumThick().arrow()
papertext(O[0]+d,O[1]-3*d,r"$\zenithAngle$")
paper.save()


######################################################################
# cosserat stress
######################################################################
w,h, = 600,600
a = 50
r = 40
s = 90
s2 = 2*s
sd = s + 20
sd2 = sd + a + 40
O = Vector2(.5*w,.5*h)
def larrow(c,d,text=None):
	d = Vector2(d).normalized() * a
	paper.path(["M",c[0],c[1],"l",d[0],d[1]]).mediumThick().arrow()
	ret = c+d
	if text is not None:
		papertext(ret[0],ret[1],text)
	return ret
def aarrow(c,d,text=None,rev=False):
	d = Vector2(d).normalized()
	t = Vector2(-d[1],d[0])
	v0 = c + t*r
	v1 = c - t*r
	if rev:
		v0,v1 = v1,v0
	paper.path(["M",v0[0],v0[1],"A",r,r,0,0,1 if rev else 0,v1[0],v1[1]]).mediumThick().arrow()
	ret = c + r*d
	if text is not None:
		papertext(ret[0],ret[1],text)
	return c + r*d
paper = Paper("cosserat_stress",w,h)
paper.rect(O[0]-s,O[1]-s,s2,s2).normal().fill("#ddd")
larrow(O,(1,0),r"$\bodyForce_1$")
aarrow(O,(-1,0),r"$\bodyCouple_3$")
larrow(O+(sd,0),( 1, 0),r"$\stress_{11}(\Delta\position_1)$")
larrow(O+(sd,0),( 0,-1),r"$\stress_{12}(\Delta\position_1)$")
larrow(O-(sd,0),(-1, 0),r"$\stress_{11}(0)$")
larrow(O-(sd,0),( 0, 1),r"$\stress_{12}(0)$")
larrow(O-(0,sd),( 0,-1),r"$\stress_{21}(\Delta\position_2)$")
larrow(O-(0,sd),( 1, 0),r"$\stress_{22}(\Delta\position_2)$")
larrow(O+(0,sd),( 0,+1),r"$\stress_{21}(0)$")
larrow(O+(0,sd),(-1, 0),r"$\stress_{22}(0)$")
aarrow(O+(sd2,0),( 1, 0),r"$\coupleStress_{13}(\Delta\position_1)$")
aarrow(O-(sd2,0),(-1, 0),r"$\coupleStress_{13}(0)$")
aarrow(O-(0,sd2),( 0,-1),r"$\coupleStress_{23}(\Delta\position_1)$")
aarrow(O+(0,sd2),( 0, 1),r"$\coupleStress_{23}(0)$")
paper.save()



######################################################################
# cosserat strain
######################################################################
k = .2
us = Matrix2(0,-k,-k,0)
fM = Matrix2(0,-k,k,0)
fm = -fM
dim = 100
mo = Matrix2_Zero
def cell(o,us,ua,fm):
	m = Matrix2_Identity + us + ua
	d = dim
	vs = [Vector2(x,y) for x,y in ((0,0),(d,0),(d,-d),(0,-d))]
	vs = [m*v for v in vs]
	vs = [Vector2(o)+v for v in vs]
	(x1,y1),(x2,y2),(x3,y3),(x4,y4) = vs
	paper.path(["M",o[0],o[1],"h",+1.1*d])
	paper.path(["M",o[0],o[1],"v",-1.1*d])
	paper.path(["M",x1,y1,"L",x2,y2,"L",x3,y3,"L",x4,y4,"Z"]).normal().fill("#ddd")
	#
	d1,d3 = [dim*v for v in (.3,.7)]
	cs = [Vector2(x,y) for x,y in ((d1,-d1),(d3,-d1),(d3,-d3),(d1,-d3))]
	cs = [m*c for c in cs]
	cs = [Vector2(o)+c for c in cs]
	r = .15*d
	rr = .2*d
	a = -ua[0,1] - fm[0,1]
	co,si = [f(a) for f in cos,sin]
	for c in cs:
		paper.circle(c[0],c[1],r).fill("white")
		paper.path([
			"M",c[0],c[1],"l",+co*rr,+si*rr,
			"M",c[0],c[1],"l",-co*rr,-si*rr,
			"M",c[0],c[1],"l",-si*rr,+co*rr,
			"M",c[0],c[1],"l",+si*rr,-co*rr,
		]).normal()
y = 130
x = 20
ms = (
	(mo,mo,mo),
	(us,mo,mo),
	(mo,fM,mo),
	(mo,mo,fm),
	(us,fM,mo),
	(us,fM,fm),
)
w,h = 180,160
for i,(m1,m2,m3) in enumerate(ms):
	paper = Paper("cosserat_strain_{}".format(i),w,h)
	cell((x,y),m1,m2,m3)
	paper.save()


######################################################################
# virtual work of internal forces
######################################################################
def point(v,g=False):
	f = "#999" if g else "black"
	paper.circle(v[0],v[1],5).stroke(null).fill(f)
def rot(v,ce,a):
	c,s = [f(radians(-a)) for f in (cos,sin)]
	v = v - ce
	v = Matrix2(c,s,-s,c)*v
	return v + ce
def arrow(p,d,l):
	d = l * Vector2(d).normalized()
	d = p+d
	line(p,d).mediumThick().arrow()
def aarrow(p):
	r = ra
	paper.path(["M",p[0],p[1]+r,"a",r,r,0,0,0,0,-2*r]).mediumThick().arrow()
fdir = Vector2(1,1).normalized()
flen = 30
ra = 20
w,h = 500,600
rx,ry = 50,100
c0 = Vector2(100,200)
c1 = c0 + (0,2*ry)
u0 = (250,-70)
u1 = (250,+70)
p0,p1 = [Vector2(c0)+(0,ry) for _ in (0,1)]
r0,r1 = -30,-60
paper = Paper("virtual_work_of_internal_forces",w,h)
paper.ellipse(c0[0],c0[1],rx,ry).fill("#ddd")
paper.ellipse(c1[0],c1[1],rx,ry).fill("#ddd")
cc0 = c0 + u0
cc1 = c1 + u1
pp0 = p0 + u0
pp1 = p1 + u1
paper.ellipse(cc0[0],cc0[1],rx,ry).attr(transform="rotate({},{},{})".format(r0,cc0[0],cc0[1])).fill("#ddd")
paper.ellipse(cc1[0],cc1[1],rx,ry).attr(transform="rotate({},{},{})".format(r1,cc1[0],cc1[1])).fill("#ddd")
paper.ellipse(cc0[0],cc0[1],rx,ry).dotted()
paper.ellipse(cc1[0],cc1[1],rx,ry).dotted()
line(c0,cc0).mediumThick().arrow()
line(c1,cc1).mediumThick().arrow()
point(p0)
arrow(p0,fdir,flen)
arrow(p0,-fdir,flen)
point(pp0,True)
point(pp1,True)
pp0 = rot(pp0,cc0,r0)
pp1 = rot(pp1,cc1,r1)
point(pp0)
arrow(pp0,fdir,flen)
point(pp1)
arrow(pp1,-fdir,flen)
papertext2(.5*(c0+cc0),r"\ua")
papertext2(.5*(c1+cc1),r"\ub")
papertext2(c0,r"\pa")
papertext2(c1,r"\pb")
papertext2(p0,r"\cc")
papertext2(p0+fdir*flen,r"\fc")
papertext2(p0-fdir*flen,r"\fc")
papertext2(pp0+fdir*flen,r"\fc")
papertext2(pp1-fdir*flen,r"\fc")
aarrow(cc0)
papertext2(cc0+(0,-ra),r"\rota")
aarrow(cc1)
papertext2(cc1+(0,-ra),r"\rotb")
paper.save()



######################################################################
# discrete stress
######################################################################
class Cell:
	def __init__(self,f,c,sn,ss,cs):
		self.f = Vector3(f)
		self.c = c
		self.sn = list(sn)
		self.ss = list(ss)
		self.cs = list(cs)
	def __call__(self):
		d = 100
		c = (120,120)
		al = .3*d
		r = .25*d
		paper.rect(c[0]-.5*d,c[1]-.5*d,d,d).fill("#ddd")
		if self.f[0]:
			paper.path(["M",c[0]-.5*al,c[1],"h",al]).thick().arrow(1 if self.f[0] > 0 else 2)
		if self.f[1]:
			paper.path(["M",c[0],c[1]+.5*al,"v",-al]).thick().arrow(1 if self.f[1] > 0 else 2)
		if self.c:
			paper.path(["M",c[0],c[1]-r,"a",r,r,0,0,0,0,2*r]).thick().arrow(1 if self.c > 0 else 2)
		#
		dd = .58*d
		if self.sn[0]:
			paper.path(["M",c[0]+dd,c[1],"h",+al]).thick().arrow(1 if self.sn[0] > 0 else 2)
		if self.sn[1]:
			paper.path(["M",c[0]-dd,c[1],"h",-al]).thick().arrow(1 if self.sn[1] > 0 else 2)
		if self.sn[2]:
			paper.path(["M",c[0],c[1]+dd,"v",+al]).thick().arrow(1 if self.sn[2] > 0 else 2)
		if self.sn[3]:
			paper.path(["M",c[0],c[1]-dd,"v",-al]).thick().arrow(1 if self.sn[3] > 0 else 2)
		#
		if self.ss[0]:
			paper.path(["M",c[0]+dd,c[1]+.5*al,"v",-al]).thick().arrow(1 if self.ss[0] > 0 else 2)
		if self.ss[1]:
			paper.path(["M",c[0]-dd,c[1]-.5*al,"v",+al]).thick().arrow(1 if self.ss[1] > 0 else 2)
		if self.ss[2]:
			paper.path(["M",c[0]-.5*al,c[1]-dd,"h",+al]).thick().arrow(1 if self.ss[2] > 0 else 2)
		if self.ss[3]:
			paper.path(["M",c[0]+.5*al,c[1]+dd,"h",-al]).thick().arrow(1 if self.ss[3] > 0 else 2)
		#
		dd = .8*d
		if self.cs[0]:
			paper.path(["M",c[0]+dd,c[1]-r,"a",r,r,0,0,1,0,2*r]).thick().arrow(2 if self.cs[0] > 0 else 1)
		if self.cs[1]:
			paper.path(["M",c[0]-dd,c[1]-r,"a",r,r,0,0,0,0,2*r]).thick().arrow(1 if self.cs[1] > 0 else 2)
		if self.cs[2]:
			paper.path(["M",c[0]-r,c[1]-dd,"a",r,r,0,0,1,2*r,0]).thick().arrow(2 if self.cs[2] > 0 else 1)
		if self.cs[3]:
			paper.path(["M",c[0]-r,c[1]+dd,"a",r,r,0,0,0,2*r,0]).thick().arrow(1 if self.cs[3] > 0 else 2)
		#
		xs = [Vector3(x,y,0) for x,y in ((1,0),(-1,0),(0,1),(0,-1))] + [Vector3.Zero]
		ddd = Vector3(1,2,3)
		xs2 = [x + ddd for x in xs]
		dirs = xs
		fns = [d*f for d,f in zip(dirs,self.sn)]
		dirs = [Vector3(x,y,0) for x,y in ((0,1),(0,-1),(1,0),(-1,0))]
		fss = [d*f for d,f in zip(dirs,self.ss)]
		fs = [fn+fs for fn,fs in zip(fns,fss)] + [self.f]
		dirs = [Vector3(0,0,1) for _ in (1,2,3,4)]
		cs = [d*c for d,c in zip(dirs,self.cs)] + [Vector3(0,0,self.c)]
		stress = sum((x.outer(f) for x,f in zip(xs,fs)),Matrix3.Zero)
		stress2 = sum((x.outer(f) for x,f in zip(xs2,fs)),Matrix3.Zero)
		assert (stress-stress2).maxAbsCoeff() < 1e-12, "{} {}".format(stress,stress2)
		sa = .5*(stress-stress.transpose())
		sa = 2*Vector3(sa[1,2],sa[2,0],sa[0,1])
		cstress = sum((x.outer(c) for x,c in zip(xs,cs)),Matrix3.Zero)
		cstress2 = sum((x.outer(c) for x,c in zip(xs2,cs)),Matrix3.Zero) + ddd.outer(sa)
		assert (cstress-cstress2).maxAbsCoeff() < 1e-12, "{} {}".format(cstress,cstress2)
		print stress
		print cstress
v0 = Vector3.Zero
vx = Vector3.UnitX
vy = Vector3.UnitY
cells = (
	Cell( v0, 0,( 0, 0, 0, 0),( 0, 0, 0, 0),( 0, 0, 0, 0)),
	Cell( v0, 0,( 1, 1, 0, 0),( 0, 0, 0, 0),( 0, 0, 0, 0)),
	Cell( vx, 0,( 0, 1, 0, 0),( 0, 0, 0, 0),( 0, 0, 0, 0)),
	Cell( v0, 0,( 0, 0, 0, 0),( 1, 1, 1, 1),( 0, 0, 0, 0)),
	Cell( v0, 0,( 0, 0, 0, 0),( 0, 0, 0, 0),( 1,-1, 0, 0)),
	Cell( v0,-1,( 0, 0, 0, 0),( 0, 0, 0, 0),( 1, 0, 0, 0)),
	Cell( v0,-2,( 0, 0, 0, 0),( 1, 1, 0, 0),( 0, 0, 0, 0)),
	Cell(-vx, 1,( 0, 0, 0, 0),( 0, 0, 1, 0),( 0, 0, 0, 0)),
	Cell( v0, 0,( 0, 0, 0, 0),( 0, 0, 0, 0),( 0, 0, 0, 0)),
	Cell( v0, 0,( 0, 0, 0, 0),( 0, 0, 0, 0),( 0, 0, 0, 0)),
)
w,h = 240,240
for i,c in enumerate(cells):
	paper = Paper("discrete_stress_{}".format(i),w,h)
	c()
	paper.save()


######################################################################
# cpm dpm graphs
######################################################################
w,h = 600,400
dd = 60
e0 = 100
ef = 450
ee = 70
ff = 50
ft = 250
O = Vector2(dd,h-dd)
def axes():
	line(O,O+(w-2*dd,0)).mediumThick().arrow()
	line(O,O+(0,-h+2*dd)).mediumThick().arrow()
	papertext(w-dd,h-dd,r"$\strain$")
	papertext(dd,dd,r"$\stress$")
for i in (1,2):
	paper = Paper("coupling_seq_cpm_dpm_{}".format(i),w,h)
	axes()
	p = O + (e0,-ft)
	pp = Vector2(285,210)
	r = 500
	pf = O + (ef,-ff)
	paper.path(["M",p[0],p[1],"A",r,r,0,0,0,pf[0],pf[1]]).attr(stroke_width=4)
	paper.path(["M",O[0],p[1],"h",w-2*dd]).normal().dotted()
	if i==1:
		line(O,p).attr(stroke_width=4)
		line(pp,O).normal().dashed()
		e1 = O+.33*(pp-O)
		e2 = O+.66*(pp-O)
		paper.path(["M",e1[0],e1[1],"H",e2[0],"V",e2[1]]).normal()
		papertext(.5*(e1[0]+e2[0]),e1[1],"1")
		papertext(e2[0],.5*(e1[1]+e2[1]),r"$(1-\damage)\linkMaterialStiffnessNormal$")
		papertext(pp[0],.5*(pp[1]+p[1]),r"$\damageA f_t$")
		paper.path(["M",p[0],p[1],"V",O[1]]).normal().dotted()
		paper.path(["M",pp[0],pp[1],"V",O[1]]).normal().dotted()
		papertext(p[0],O[1],r"$\strainO$")
		papertext(pp[0],O[1],r"$\kappa$")
		paper.path(["M",pp[0],pp[1],"H",O[0]]).normal().dotted()
		papertext(O[0],pp[1],"$r$")
	else:
		paper.path(["M",w-dd,p[1],"H",p[0],"Q",O[0]+.5*e0,p[1],O[0],O[1]]).attr(stroke_width=4).stroke("#aaa")
		papertext(.9*w,p[1],"plasticity")
		papertext(.9*w,pf[1],"damage")
		papertext(pp[0],.5*(pp[1]+p[1]),r"$\damage f_t$")
		paper.path(["M",pp[0],pp[1],"L",O[0]+ee,O[1]]).normal().dashed()
	paper.path(["M",pp[0],pp[1],"V",p[1]]).mediumThick().arrow(3)
	papertext(O[0],p[1],"$f_t$")
	paper.save()
