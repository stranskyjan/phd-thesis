#!/bin/bash
rm -f *.pdf
base=PhD_thesis_Stransky_2018_
python figs.py
mypwd=`pwd`
cd /tmp
for f in $base*.svg; do
	rsvg-convert -f pdf -o ${f/.svg/.pdf} $f
done
cd $mypwd
cp /tmp/$base*.pdf .
for f in *.pdf; do
	mv $f ${f/$base/}
done
