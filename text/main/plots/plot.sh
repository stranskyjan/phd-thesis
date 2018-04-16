#!/bin/bash
set -e
rm -rf plots
mkdir plots
gnuplot plot.gpi
