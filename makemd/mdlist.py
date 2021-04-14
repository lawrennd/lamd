#!/usr/bin/env python3

import sys
import os
import argparse

import frontmatter as fm

import ndlpy.talk as nt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output",
                        type=str,
                        choices=['talks', 'grants', 'extalks', 'teaching', 'students', 'exstudents', 'pdras', 'expdras'],
                        help="The type of output markdown list")

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+',
                        help="The file names to read in")
    
    args = parser.parse_args()


    entries = []
    for file in args.file:
        name, ext = os.path.splitext(file.name)
        print(name, ext)
        if ext == 'yaml' or ext == 'md' or ext == 'markdown':
            print("Markdown")
            print(file.read())
            metadata, _ = fm.parse(file.read())
            print(metadata)
            entries.append(metadata)
        elif ext == 'csv':
            csv_entries = csv.DictReader(file)
            entries += csv_entries

    print(entries)


        
    #fields = ny.header_fields(filename)


if __name__ == "__main__":
    sys.exit(main())
