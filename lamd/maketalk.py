#!/usr/bin/env python3

import os
import argparse

import ndlpy.talk as nt
import ndlpy.yaml as ny

import lamd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        type=str,
                        help="The filename where dependencies are being searched")

    args = parser.parse_args()
    basename = os.path.basename(args.filename)
    base = os.path.splitext(basename)[0]

    dirname = os.path.dirname(lamd.__file__)
    include_dir = os.path.join(dirname, "makefiles")
    script_dir = os.path.join(dirname, "scripts")
    f = open('makefile', 'w+')
    f.write(f"BASE={base}\n")
    f.write(f"INCLUDEDIR={include_dir}\n")
    f.write(f"SCRIPTDIR={script_dir}\n")
    
    f.write(f"include $(INCLUDEDIR)/make-talk-flags.mk\n")
    f.write(f"include $(INCLUDEDIR)/make-talk.mk\n")
    f.close()
    field = "snippetsdir"
    try:
        answer = nt.talk_field(field, f"{base}.md")
    except ny.FileFormatError:
        if field in ny.config:
            answer= ny.config[field]
        else:
            answer = ''
        answer = nt.talk_field(field, filename)
    
    # Hacky way to make sure snippets are pulled down
    os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")

    os.system('git pull')
    os.system(f"make --include-dir {include_dir} all")

if __name__ == "__main__":
    sys.exit(main())
