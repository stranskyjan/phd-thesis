#!/bin/bash
set -e
name=PhD_thesis_Stransky_2018_cd

pdflatex="pdflatex -interaction=nonstopmode -halt-on-error"

$pdflatex $name.tex
