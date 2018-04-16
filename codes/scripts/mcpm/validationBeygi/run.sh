#!/bin/bash
set -e

python createHeteroGeometries.py --test
python createHeteroGeometries.py

yadebatch="yade-2017.01a-batch --disable-pynotify -j 4 --job-threads 1 --log /tmp/$.%.log"

declare -a coeffss=(
	"( .5, .5, .1)"
	"( .5, .5, .05)"
)
tmp=""
for coeffs in "${coeffss[@]}"; do
	w=${coeffs// /}
	tmp="$tmp $w"
done
coeffss=$tmp

tab=/tmp/validationBeygi.tab
echo "outBase experiment gradingCurve hGeomIndex physCoeffs" > $tab
for coeffs in $coeffss; do
	#for hGeomIndex in 1; do
	for hGeomIndex in 1 2 3; do
		#for experiment in l; do
		for experiment in l h; do
			#for gradingCurve in 95 190; do
			for gradingCurve in 95 125 190; do
				gradingCurveS=$(printf "%03d" "$gradingCurve")
				echo "'/tmp/validationBeygi_${coeffs}_${experiment}_${gradingCurveS}_${hGeomIndex}' '$experiment' $gradingCurve $hGeomIndex $coeffs" >> $tab
			done
		done
	done
done
$yadebatch $tab uniax.py
