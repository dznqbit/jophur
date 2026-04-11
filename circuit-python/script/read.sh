#!/bin/sh
DEPLOY=/Volumes/CIRCUITPY
LOCAL=`pwd`
cp -r $DEPLOY/code.py $DEPLOY/lib $LOCAL

echo "Copied `date`" > $LOCAL/copy.txt
