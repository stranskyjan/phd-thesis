import os
import subprocess
import shutil

fn = "/tmp/plottext.tex"
tmpplots = "/tmp/plots"
lines = [
	r"\documentclass[12pt]{report}",
	r"\usepackage[showframe,inner=1in,outer=1in,top=1in,bottom=1in,a4paper]{geometry}",
	r"\usepackage[T1]{fontenc}",
	r"\usepackage[utf8]{inputenc}",
	"\usepackage{graphicx}",
	"\usepackage{xcolor}",
	"\usepackage{xstring}",
	r"\graphicspath{{plots/}}",
	r"\usepackage{times}",
	r"\renewcommand{\familydefault}{\sfdefault}",
	r"\usepackage[scaled]{helvet}",
	r"\usepackage{sfmath}",
	r"\usepackage{cmap}% pdf file search",
	r"\usepackage[multidit]{grffile}",
	r"\input{common}",
	r"\input{commands}",
	""
	r"\begin{document}",
	""
]

plots = sorted(f for f in os.listdir("plots") if f.endswith(".tex"))
for p in plots:
	lines.extend((
		r"{}\\".format(p.replace("_",r"\_")),
		r"\input{{plots/{}}}".format(p),
		"",
	))

lines.append(r"\end{document}")

with open(fn,"w") as f:
	f.writelines(l+"\n" for l in lines)
if os.path.exists(tmpplots):
	shutil.rmtree(tmpplots)
shutil.copytree("plots",tmpplots)
shutil.copy("../commands.tex","/tmp")
shutil.copy("../common.tex","/tmp")
os.chdir("/tmp")
subprocess.Popen("pdflatex {}".format(fn).split()).wait()
