#!/bin/sh
rootdir="/cloud"
nohup python $rootdir/workdir/run.py > $rootdir/workdir/run.py.log &
 