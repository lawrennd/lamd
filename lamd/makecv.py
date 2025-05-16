#!/usr/bin/env python3
"""
Module for generating CV documents from markdown files.

This module provides functionality to convert CV documents from markdown
to various formats (PDF, HTML, etc.) using LaTeX and other tools.
It creates a makefile with appropriate configurations and runs build commands.
"""

import os
import sys
import argparse

import lynguine.util.talk as nt
import lynguine.util.yaml as ny

import lamd

def main():
    """
    Main function for the makecv tool.
    
    This function:
    1. Parses command line arguments for the markdown file
    2. Creates a makefile with appropriate paths and configurations
    3. Pulls dependencies from git repositories
    4. Runs make commands to generate the CV in various formats
    
    Returns:
        int: 0 for successful execution
    """
    parser = argparse.ArgumentParser(description="Convert CV from markdown to other formats")
    parser.add_argument("filename",
                        type=str,
                        help="The markdown file containing the CV content")

    args = parser.parse_args()

    basename = os.path.basename(args.filename)
    base = os.path.splitext(basename)[0]
    
    dirname = os.path.dirname(lamd.__file__)
    make_dir = os.path.join(dirname, "makefiles")
    includes_dir = os.path.join(dirname, "includes")
    script_dir = os.path.join(dirname, "scripts")

    # Pull latest changes
    os.system('git pull')
    os.system('make all')
    
    # Create makefile with configuration
    f = open('makefile', 'w+')
    f.write(f"BASE={base}\n")
    f.write(f"MAKEFILESDIR={make_dir}\n")
    f.write(f"INCLUDESDIR={includes_dir}\n")
    f.write(f"SCRIPTDIR={script_dir}\n")
    
    f.write(f"include $(MAKEFILESDIR)/make-cv-flags.mk\n")
    f.write(f"include $(MAKEFILESDIR)/make-cv.mk\n")
    f.close()
    
    # Handle dependency directories
    for field in ["snippetsdir", "bibdir"]:
        try:
            answer = nt.talk_field(field, f"{base}.md", user_file=["_lamd.yml", "_config.yml"])
        except ny.FileFormatError:
            iface = lamd.config.interface.Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")
            if field in iface:
                answer = iface[field]
            else:
                answer = ''
    
        # Pull latest changes from dependency repositories
        os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")

    # Final build steps
    os.system('git pull')
    os.system(f"make all")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
