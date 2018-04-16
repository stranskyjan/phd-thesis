#!/bin/bash
set -e
name=PhD_thesis_Stransky_2018_poster

pdflatex="pdflatex -interaction=nonstopmode -halt-on-error"

$pdflatex $name.tex
$pdflatex $name.tex
printf "\nFINAL RUN\n\n"
$pdflatex $name.tex
