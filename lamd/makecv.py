#!/usr/bin/env python3

import os
import argparse

import ndlpy.talk as nt
import ndlpy.yaml as ny
from ndlpy.settings import Settings

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
    make_dir = os.path.join(dirname, "makefiles")
    includes_dir = os.path.join(dirname, "includes")
    script_dir = os.path.join(dirname, "scripts")


    os.system('git pull')
    os.system('make all')
    
    f = open('makefile', 'w+')
    f.write(f"BASE={base}\n")
    f.write(f"MAKEFILESDIR={make_dir}\n")
    f.write(f"INCLUDESDIR={includes_dir}\n")
    f.write(f"SCRIPTDIR={script_dir}\n")
    
    f.write(f"include $(MAKEFILESDIR)/make-cv-flags.mk\n")
    f.write(f"include $(MAKEFILESDIR)/make-cv.mk\n")
    f.close()
    for field in ["snippetsdir", "bibdir"]:
        try:
            answer = nt.talk_field(field, f"{base}.md")
        except ny.FileFormatError:
            settings = Settings(user_file=["_lamd.yml", "_config.yml"], directory=".")
            if field in settings:
                answer = settings[field]
            else:
                answer = ''
    
        # Hacky way to make sure snippets are pulled down
        os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")

    os.system('git pull')
    os.system(f"make all")


if __name__ == "__main__":
    sys.exit(main())
