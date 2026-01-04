#!/usr/bin/env python3
"""
Script to process markdown files into various output formats.

This script generates a makefile based on the input markdown file
and runs the appropriate commands to convert it to the requested formats.
"""

import argparse
import os
import sys

import lamd
from lamd.profiler import BuildProfiler


def main() -> int:
    """
    Process a markdown file and generate various output formats.

    This function creates a makefile customized for the specific input file,
    and then runs 'make' to generate the output formats. It supports formats
    like slides, notes, and more.

    Returns:
        int: 0 for success, non-zero for failure
    """
    parser = argparse.ArgumentParser(
        description="Process markdown files into various output formats.",
        epilog="Examples: \n"
        "  maketalk talk.md                    # Create all output formats (fast mode)\n"
        "  maketalk talk.md --format slides    # Create slides only\n"
        "  maketalk talk.md --format notes     # Create notes only\n"
        "  maketalk talk.md --to html          # Output to HTML format\n"
        "  maketalk talk.md --no-server        # Disable server mode (slower)\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("filename", type=str, help="The markdown file to process")

    parser.add_argument(
        "--format", "-F", type=str, choices=["slides", "notes"], help="The content format to produce (slides, notes)"
    )

    parser.add_argument("--to", "-t", type=str, choices=["html", "pptx", "docx", "pdf", "tex"], help="The output file format")

    parser.add_argument(
        "--no-server",
        action="store_true",
        help="Disable server mode (use direct mode, slower but more compatible)"
    )

    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable detailed performance profiling (shows where build time is spent)"
    )

    args = parser.parse_args()
    
    # Check if the markdown file exists FIRST (before any other work)
    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found.")
        print(f"Please check the filename and try again.")
        sys.exit(1)
    
    # Initialize profiler
    profiler = BuildProfiler(enabled=args.profile)
    profiler.start()
    
    # Enable Makefile-level profiling if requested
    if args.profile:
        profiler.enable_makefile_profiling()

    # Extract the base filename without extension
    basename = os.path.basename(args.filename)
    base = os.path.splitext(basename)[0]

    # Check for _lamd.yml first
    with profiler.measure("Config file existence check"):
        if not os.path.exists("_lamd.yml"):
            print("Error: _lamd.yml configuration file not found.")
            print("Please create a _lamd.yml file in the current directory.")
            print("Note: _config.yml is deprecated and only supported for backwards compatibility.")
            sys.exit(1)

    # Load the interface to check for required fields
    with profiler.measure("Config file loading"):
        iface = lamd.config.interface.Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")

    # Update external dependencies if needed
    with profiler.measure("Dependency git pulls"):
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

            git_dir = os.path.join(answer, ".git")
            if os.path.isdir(git_dir):
                os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")
            else:
                print(f"Warning: {answer} is not a git repository. Skipping git pull.")

    # Set up directories
    dirname = os.path.dirname(lamd.__file__)
    make_dir = os.path.join(dirname, "makefiles")
    includes_dir = os.path.join(dirname, "includes")
    templates_dir = os.path.join(dirname, "templates")
    script_dir = os.path.join(dirname, "scripts")

    # Create the makefile
    with profiler.measure("Makefile generation"):
        with open("makefile", "w+") as f:
            f.write(f"BASE={base}\n")
            f.write(f"LAMDDIR={dirname}\n")
            f.write(f"MAKEFILESDIR={make_dir}\n")
            f.write(f"INCLUDESDIR={includes_dir}\n")
            f.write(f"TEMPLATESDIR={templates_dir}\n")
            f.write(f"SCRIPTDIR={script_dir}\n")
            
            # Add profiling configuration if enabled
            if args.profile:
                f.write("\n# Profiling enabled\n")
                f.write(f"PROFILE=1\n")
                f.write(f"PROFILE_FILE={profiler.profile_file}\n")
                f.write(f"TIME_CMD=$(SCRIPTDIR)/profile-command\n")
            else:
                f.write("\n# Profiling disabled\n")
                f.write("TIME_CMD=\n")
            
            f.write("\n")
            f.write("include $(MAKEFILESDIR)/make-talk-flags.mk\n")
            f.write("include $(MAKEFILESDIR)/make-talk.mk\n")

    # Make sure we have the latest files
    with profiler.measure("Local git pull"):
        os.system("git pull")

    # Enable server mode by default (4x faster), unless --no-server is specified
    if not args.no_server:
        os.environ["LAMD_USE_SERVER_CLIENT"] = "1"

    # Build the make command based on format and output options
    make_cmd = "make"

    if args.format and args.to:
        # Build specific format and output type
        target = f"{base}.{args.format}.{args.to}"
        make_cmd += f" {target}"
    elif args.format:
        # Build all formats of a specific type
        if args.format == "slides":
            make_cmd += " slides"
        elif args.format == "notes":
            make_cmd += " notes"
    elif args.to:
        # Build all content in a specific output format
        if args.to == "html":
            make_cmd += " html"
        elif args.to == "pptx":
            make_cmd += " pptx"
        elif args.to == "pdf":
            make_cmd += " pdf"
        elif args.to == "tex":
            make_cmd += " tex"
        elif args.to == "docx":
            make_cmd += " docx"
    else:
        # Build everything
        make_cmd += " all"

    # Run the make command (this is where most of the time is spent)
    with profiler.measure("Make execution (total)"):
        result = os.system(make_cmd)
    
    # Generate profiling report if enabled
    if args.profile:
        profiler.report()
        profiler.cleanup()
    
    return result


if __name__ == "__main__":
    sys.exit(main())
