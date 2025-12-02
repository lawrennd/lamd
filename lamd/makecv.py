#!/usr/bin/env python3
"""
Module for generating CV documents from markdown files.

This module provides functionality to convert CV documents from markdown
to various formats (PDF, HTML, etc.) using LaTeX and other tools.
It creates a makefile with appropriate configurations and runs build commands.
"""

import argparse
import os
import sys

import lamd


def main() -> int:
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
    parser.add_argument("filename", type=str, help="The markdown file containing the CV content")

    args = parser.parse_args()

    basename = os.path.basename(args.filename)
    base = os.path.splitext(basename)[0]

    # Check for _lamd.yml first
    if not os.path.exists("_lamd.yml"):
        print("Error: _lamd.yml configuration file not found.")
        print("Please create a _lamd.yml file in the current directory.")
        print("Note: _config.yml is deprecated and only supported for backwards compatibility.")
        sys.exit(1)

    # Load the interface to check for required fields
    iface = lamd.config.interface.Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")

    # Setup paths
    dirname = os.path.dirname(lamd.__file__)
    make_dir = os.path.join(dirname, "makefiles")
    includes_dir = os.path.join(dirname, "includes")
    script_dir = os.path.join(dirname, "scripts")

    # Create makefile with configuration
    with open("makefile", "w+") as f:
        f.write(f"BASE={base}\n")
        f.write(f"MAKEFILESDIR={make_dir}\n")
        f.write(f"INCLUDESDIR={includes_dir}\n")
        f.write(f"SCRIPTDIR={script_dir}\n")
        f.write("include $(MAKEFILESDIR)/make-cv-flags.mk\n")
        f.write("include $(MAKEFILESDIR)/make-lists.mk\n")
        f.write("include $(MAKEFILESDIR)/make-cv.mk\n")

    # Update external dependencies if needed
    for field in ["snippetsdir", "bibdir"]:
        if field not in iface:
            print(f"Error: Required field '{field}' is not defined in your _lamd.yml configuration file.")
            print(f"Please add a '{field}' entry pointing to your {field.replace('dir', '')} directory.")
            print("Example:")
            print(f"{field}: ../_{field.replace('dir', '')}")
            sys.exit(1)

        # Get the path and expand environment variables
        answer = os.path.expandvars(iface[field])

        # Check if the directory exists
        if not os.path.exists(answer):
            print(f"Error: Directory '{answer}' specified in _lamd.yml for '{field}' does not exist.")
            print(f"Please create the directory or update the '{field}' entry in your _lamd.yml file.")
            sys.exit(1)

        git_dir = os.path.join(answer, ".git")
        if os.path.isdir(git_dir):
            os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")
        else:
            print(f"Warning: {answer} is not a git repository. Skipping git pull.")

    # Check for postsdir
    if "postsdir" not in iface:
        print("Error: 'postsdir' is not defined in your _lamd.yml configuration file.")
        print("Please add a 'postsdir' entry pointing to your posts directory.")
        print("Example:")
        print("postsdir: ../_posts")
        sys.exit(1)

    # Make sure we have the latest files if in a git repo
    if os.path.isdir(".git"):
        os.system("git pull")

    # Final build step
    return os.system("make all")


if __name__ == "__main__":
    sys.exit(main())
