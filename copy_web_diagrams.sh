#!/bin/bash


SLIDEDIR=$(../talkfield.py slidedir $1)
echo Slides Directory: $SLIDEDIR
for file in $(../dependencies.py slidediagrams $1)
do
    mkdir -p `dirname $SLIDEDIR/$file`
    if ! cmp -s $file $SLIDEDIR/$file ; then
       echo "Copying $file to $SLIDEDIR/$file"
       cp $file $SLIDEDIR/$file
    else
	echo "Not copying $file"
    fi
done
