#!/bin/bash
set -e
name=PhD_thesis_Stransky_2018_presentation
full=true

pdflatex="pdflatex -interaction=nonstopmode -halt-on-error"

$pdflatex $name.tex
if $full; then
	$pdflatex $name.tex
	printf "\nFINAL RUN\n\n"
	$pdflatex $name.tex
fi
