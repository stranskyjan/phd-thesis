#!/bin/bash
set -e
name=PhD_thesis_Stransky_2018_statement
full=true

pdflatex="pdflatex -interaction=nonstopmode -halt-on-error"

if $full; then
	$pdflatex $name.tex
	printf "\nBIBER\n\n"
	biber --quiet $name
	$pdflatex $name.tex
	printf "\nFINAL RUN\n\n"
	$pdflatex $name.tex
else
	$pdflatex $name.tex
fi
