#!/bin/sh
rootdir="/cloud"

cp -n $rootdir/source/run.sh $rootdir/workdir/run.sh
cp -n $rootdir/source/run.py $rootdir/workdir/run.py
cp -n $rootdir/source/config.json $rootdir/workdir/config.json

# run backup programe
sh $rootdir/workdir/run.sh
# stand by with bash
/bin/bash