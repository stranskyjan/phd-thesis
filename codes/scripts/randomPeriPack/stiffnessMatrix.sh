#!/bin/bash
set -e
j=4
yade=yade-2017.01a
yadebatch="$yade-batch --disable-pynotify -j $j --job-threads 1"
radius=.1234

irs="1.05 1.25 1.50 2.00"
poissons="
	1.00e-3
	3.62e-3
	1.00e-2
	3.62e-2
	1.00e-1
	3.62e-1
	1.00e+0
	3.62e+0
	1.00e+1
	3.62e+1
	1.00e+2
	3.62e+2
	1.00e+3
	3.62e+3
	1.00e+4
"
poissonss="1.00e-1 1.00e+0 1.00e+1"

oofemout=/tmp/stiffnessMatrix_oofem
yadeout=/tmp/stiffnessMatrix_yade

if true; then
# OOFEM - isotropy
	tab=${oofemout}_isotropy.tab
	poisson=0.2
	echo "outbase num intRatio poisson packing" > $tab
	for num in 0100 0300 0500 0700 1000; do
		for j in 1 2 3 4 5; do
			packing=${oofemout}_isotropy_packing_${num}_${j}.packing
			$yade -n -x randomPeriPack.py --radius $radius --num $num --memo $packing --seed $j
		done
		for ir in $irs; do
			for poisson in $poissonss; do
				for j in 1 2 3 4 5; do
					packing=${oofemout}_isotropy_packing_${num}_${j}.packing
					echo "'${oofemout}_isotropy_N${num}_I${ir}_P${poisson}_J${j}' $num $ir $poisson '$packing'" >> $tab
				done
			done
		done
	done
	$yadebatch --log /tmp/$.isotropy.%.log $@ $tab stiffnessMatrix_oofem.py
fi

# for some reason, the rerun results and that from the actual thesis are slightly different (although seed=1 is used by default). Probably some change in the codes between gathering the results and this release
if true; then
	num=1000
	packing=/tmp/$omacromicro.packing
	$yade -n -x randomPeriPack.py --radius $radius --num $num --memo $packing

	# OOFEM - macromicro
	tab=${oofemout}_macromicro.tab
	echo "outbase poisson intRatio packing" > $tab
	for poisson in $poissons; do
		for ir in $irs; do
			echo "'${oofemout}_macromicro_P${poisson}_I$ir' $poisson $ir '$packing'" >> $tab
		done
	done
	$yadebatch --log /tmp/$.macromicro.%.log $@ $tab stiffnessMatrix_oofem.py

	# YADE - macromicro
	tab=${yadeout}_macromicro.tab
	echo "outbase poisson intRatio packing" > $tab
	for poisson in $poissons; do
		for ir in $irs; do
			echo "'${yadeout}_macromicro_P${poisson}_I$ir' $poisson $ir '$packing'" >> $tab
		done
	done
	$yadebatch --log /tmp/$.macromicro.%.log $@ $tab stiffnessMatrix.py
fi
