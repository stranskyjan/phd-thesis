#!/bin/bash
ext=2017.01a
sourcedir=$HOME/programs/yade/$ext
builddir=$HOME/programs/builds/yade/$ext
[ -d $builddir ] || mkdir -p $builddir
cd $builddir
cmake \
	-DSUFFIX=-$ext \
	-DCMAKE_INSTALL_PREFIX=$HOME \
	-DENABLE_LINSOLV=OFF \
	-DENABLE_PFVFLOW=OFF \
	-DENABLE_LBMFLOW=OFF \
	-DENABLE_GL2PS=OFF \
	-DUSE_QT5=ON \
	$sourcedir
make $@
make install
