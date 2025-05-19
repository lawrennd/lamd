#!/usr/bin/env python3

import os
import argparse
import sys

import lynguine.util.talk as nt
import lynguine.util.yaml as ny

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
    templates_dir = os.path.join(dirname, "templates")
    script_dir = os.path.join(dirname, "scripts")
    f = open('makefile', 'w+')
    f.write(f"BASE={base}\n")
    f.write(f"MAKEFILESDIR={make_dir}\n")
    f.write(f"INCLUDESDIR={includes_dir}\n")
    f.write(f"TEMPLATESDIR={templates_dir}\n")
    f.write(f"SCRIPTDIR={script_dir}\n")
    
    f.write(f"include $(MAKEFILESDIR)/make-talk-flags.mk\n")
    f.write(f"include $(MAKEFILESDIR)/make-talk.mk\n")
    f.close()

    # Check for _lamd.yml first
    if not os.path.exists("_lamd.yml"):
        print("Error: _lamd.yml configuration file not found.")
        print("Please create a _lamd.yml file in the current directory.")
        print("Note: _config.yml is deprecated and only supported for backwards compatibility.")
        sys.exit(1)

    # Load the interface to check for required fields
    iface = lamd.config.interface.Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")
    
    for field in ["snippetsdir", "bibdir"]:
        if field not in iface:
            print(f"Error: Required field '{field}' is not defined in your _lamd.yml configuration file.")
            print(f"Please add a '{field}' entry pointing to your {field.replace('dir', '')} directory.")
            print("Example:")
            print(f"{field}: ../_{field.replace('dir', '')}")
            sys.exit(1)
            
        answer = iface[field]
        
        # Check if the directory exists and is a git repo before pulling
        if not os.path.exists(answer):
            print(f"Error: Directory '{answer}' specified in _lamd.yml for '{field}' does not exist.")
            print(f"Please create the directory or update the '{field}' entry in your _lamd.yml file.")
            sys.exit(1)
        
        git_dir = os.path.join(answer, '.git')
        if os.path.isdir(git_dir):
            os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")
        else:
            print(f"Warning: {answer} is not a git repository. Skipping git pull.")

    os.system('git pull')
    os.system(f"make all")

if __name__ == "__main__":
    sys.exit(main())
