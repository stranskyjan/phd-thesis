#!/bin/bash
ext=-2.3
oofem=oofem$ext
extractor=extractor$ext
builddir=$HOME/programs/builds/oofem/$oofem
sourcedir=$HOME/programs/oofem/$oofem

[ -d $builddir ] || mkdir -p $builddir
cd $builddir
cmake \
	-DCMAKE_BUILD_TYPE=CMAKE_CXX_FLAGS_RELEASE \
	-DUSE_DSS=ON \
	-DUSE_IML=ON \
	$sourcedir
make $@

cd $HOME/bin
rm -f $oofem $extractor
ln -s $builddir/oofem $oofem
ln -s $sourcedir/tools/extractor.py $extractor
