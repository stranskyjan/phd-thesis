#!/bin/bash
set -e
ext=-2.0
oofem=oofem$ext
extractor=extractor$ext
sourcedir=$HOME/programs/oofem/$oofem

cd $sourcedir
./configure \
	CXXFLAGS="-O3" \
	OOFEM_TARGET="oofem" \
	--enable-dss
make OOFEM_TARGET="oofem" $@

cd $HOME/bin
rm -f $oofem $extractor
ln -s $sourcedir/targets/oofem/bin/oofem $oofem
ln -s $sourcedir/tools/extractor.py $extractor
chmod 755 $extractor
