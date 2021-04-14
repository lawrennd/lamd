#!/usr/bin/env python3

import sys
import os
import csv
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
        ext = ext[1:]
        if ext == 'yaml' or ext == 'md' or ext == 'markdown':
            metadata, _ = fm.parse(file.read())
            file.close()
            entries.append(metadata)
        elif ext == 'csv':
            csv_entries = csv.DictReader(file)
            file.close()
            entries += csv_entries

    text = ''
    if args.output=="talks":
        for entry in entries:
            text +=  "* **{venue}**, {month}, {year}\n".format(venue=entry['venue'], month=entry['data'].strftime('%m'), year=entry['data'].strftime('%Y'))


    print(text)

if __name__ == "__main__":
    sys.exit(main())
