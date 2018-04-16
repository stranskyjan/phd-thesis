#!/bin/bash
set -e
yade=yade-2017.01a
tab=/tmp/packingFraction.tab
echo nums > $tab
printf "(" >> $tab
for (( run=0 ; run<3 ; run++ )); do
	for (( n=50 ; $n<=4000 ; n=$n+50 )); do
		printf "$n," >> $tab
	done
done
echo ")" >> $tab
$yade-batch --log /tmp/$.@.log $@ $tab packingFraction.py
