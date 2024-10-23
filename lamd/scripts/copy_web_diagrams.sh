#!/bin/bash

# Dependencies: mdfield, dependencies

# This script copies the diagrams from the source directory to the target directory.
# The arguments required are the source markdown file, the type of diagrams (slidediagrams or texdiagrams) and the target directory.
# Copy diagrams to the right subdirectory.
# Takes too arguments, first is the source markdown file, second is either slidediagrams or texdiagrams, third is new directory.
echo Slides Directory: $3

slides_dir=`mdfield slidesdir $1`
diagrams_dir=`mdfield diagramsdir $1`
snippets_dir=`mdfield snippetsdir $1`

echo Diagrams Directory: $diagrams_dir

# Loop over the dependencies and copy the diagrams
for file in $(dependencies $2 $1 --snippets-path $snippets_dir)
do
    # Copy the diagrams from slidesdir/diagrams to diagramsdir

    # Replace the slides directory with the diagrams directory
    # Strip the directory name from the file and prepend the new directory
    newfile=`echo $file | sed "s|$slides_dir|$diagrams_dir|"`
    # Make sure the directory exists
    mkdir -p `dirname $newfile`
    if ! cmp -s $file $newfile ; then
       echo "Copying $file to $newfile"
       cp $file $newfile
    else
    echo "Not copying $file to $newfile, they are the same."
    fi
done
