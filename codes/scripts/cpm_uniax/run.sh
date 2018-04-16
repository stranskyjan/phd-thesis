#!/bin/bash
yade-2017.01a-batch --disable-pynotify -j 4 --job-threads 1 --log /tmp/$.%.log uniax.tab uniax.py
