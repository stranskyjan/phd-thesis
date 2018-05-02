#!/bin/bash
set -e

preproc=true
main=true
statement=true
poster=true
cd=true
presentation=true

script_dir=`dirname $0`
script_dir=`realpath $script_dir`

if $preproc; then
	echo "PREPROC"
	# test prerequisites
	python -c "import raphaelpy"
	python -c "import minieigen"
	hash rsvg-convert
	# figs
	cd $script_dir/text/figs/raphaelpy
	bash figs.sh > /tmp/figs.out
	# results
	cd $script_dir/results
	python preproc.py
fi

# main
if $main; then
	echo "MAIN"
	cd $script_dir/text/main
	rm -f common.tex
	ln -s ../common/common.tex .
	ln -s ../common/commands.tex .
	cd plots
	bash plot.sh
	cd ..
	bash compile.sh > /tmp/main.out
fi

# statement
if $statement; then
	echo "STATEMENT"
	cd $script_dir/text/statement
	rm -f common.tex
	ln -s ../common/common.tex .
	ln -s ../common/commands.tex .
	cd plots
	bash plot.sh
	cd ..
	bash compile.sh > /tmp/statement.out
fi

# poster
if $poster; then
	echo "POSTER"
	cd $script_dir/text/poster
	rm -f common.tex
	ln -s ../common/common.tex .
	ln -s ../common/commands.tex .
	cd plots
	rm -rf plots
	mkdir plots
	bash plot.sh
	cd ..
	bash compile.sh > /tmp/poster.out
fi

# cd
if $cd; then
	echo "CD"
	cd $script_dir/text/cd
	rm -f common.tex
	ln -s ../common/common.tex .
	ln -s ../common/commands.tex .
	bash compile.sh > /tmp/cd.out
fi

# presentation
if $presentation; then
	echo "PRESENTATION"
	cd $script_dir/text/presentation
	rm -f common.tex
	ln -s ../common/common.tex .
	ln -s ../common/commands.tex .
	#
	cd figs
	figstodownload=/tmp/figstodownload.txt
	echo "" > $figstodownload
	for f in concrete.jpg contact1.gif multi1.gif oofem-logo.png packing.png packing_with_links.png surf1.gif vol1.gif yade-logo.png; do
		echo "http://mech.fsv.cvut.cz/~stransky/phdthesis/presentation/figs/$f" >> $figstodownload
	done
	wget -i $figstodownload -o /tmp/figswget.out
	cd ..
	#
	cd figs/raphaelpy
	bash figs.sh > /tmp/presentationfigs.out
	cd ../..
	cd plots
	rm -rf plots
	mkdir plots
	bash plot.sh
	cd ..
	bash compile.sh > /tmp/presentation.out
fi

echo
echo OK
