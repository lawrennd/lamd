#!/bin/bash

# Dependencies: dependencies

# This script copies the diagrams from the source directory to the target directory.
# Usage: copy_web_diagrams.sh <source_md_file> <diagram_type> <target_dir> <slides_dir> <diagrams_dir> <snippets_dir> [-v|--verbose]

# Parse command line arguments
VERBOSE=0
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        *)
            break
            ;;
    esac
done

if [ "$#" -ne 6 ]; then
    echo "Usage: $0 <source_md_file> <diagram_type> <target_dir> <slides_dir> <diagrams_dir> <snippets_dir> [-v|--verbose]"
    exit 1
fi

source_file=$1
diagram_type=$2
target_dir=$3
slides_dir=$4
diagrams_dir=$5
snippets_dir=$6

# Check if we're in _lamd directory and adjust input paths if they're relative
current_dir=$(basename "$PWD")
if [ "$current_dir" = "_lamd" ]; then
    # If we're in _lamd, adjust relative input paths to be relative to parent directory
    if [[ "$slides_dir" != /* ]]; then
        slides_dir="../$slides_dir"
    fi
    if [[ "$diagrams_dir" != /* ]]; then
        diagrams_dir="../$diagrams_dir"
    fi
    if [[ "$snippets_dir" != /* ]]; then
        snippets_dir="../$snippets_dir"
    fi
    if [[ "$source_file" != /* ]]; then
        source_file="../$source_file"
    fi
    [ $VERBOSE -eq 1 ] && echo "In _lamd directory, adjusting input paths to be relative to parent"
fi

# Check if required directories exist
if [ ! -d "$slides_dir" ]; then
    echo "Error: Slides directory '$slides_dir' does not exist"
    exit 1
fi

if [ ! -d "$diagrams_dir" ]; then
    echo "Error: Diagrams directory '$diagrams_dir' does not exist"
    exit 1
fi

if [ ! -d "$snippets_dir" ]; then
    echo "Error: Snippets directory '$snippets_dir' does not exist"
    exit 1
fi

if [ ! -f "$source_file" ]; then
    echo "Error: Source file '$source_file' does not exist"
    exit 1
fi

[ $VERBOSE -eq 1 ] && echo "Slides Directory: $slides_dir"
[ $VERBOSE -eq 1 ] && echo "Diagrams Directory: $diagrams_dir"
[ $VERBOSE -eq 1 ] && echo "Snippets Directory: $snippets_dir"

# Create target directory if it doesn't exist
mkdir -p "$target_dir"

# Loop over the dependencies and copy the diagrams
for file in $(dependencies $diagram_type $source_file --snippets-path $snippets_dir)
do
    # Get just the filename and its subdirectory structure after the last occurrence of diagrams/
    rel_path=$(echo "$file" | sed 's/.*diagrams\///')
    # Construct the new path using the target directory
    newfile="$target_dir/$rel_path"
    
    # Make sure the directory exists
    mkdir -p `dirname $newfile`
    if ! cmp -s $file $newfile ; then
       [ $VERBOSE -eq 1 ] && echo "Copying $file to $newfile"
       cp $file $newfile
    else
       [ $VERBOSE -eq 1 ] && echo "Not copying $file to $newfile, they are the same."
    fi
done
