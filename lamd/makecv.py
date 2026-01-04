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
from lamd.profiler import BuildProfiler


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
    parser = argparse.ArgumentParser(
        description="Convert CV from markdown to other formats",
        epilog="Examples:\n"
        "  makecv my-cv.md                # Standard build (fast mode)\n"
        "  makecv my-cv.md --no-server    # Disable server mode (slower)\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("filename", type=str, help="The markdown file containing the CV content")
    
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

    parser.add_argument(
        "--git-cache-minutes",
        type=int,
        default=5,
        help="Cache git fetch results for N minutes (default: 5). Set to 0 to always check remote."
    )

    args = parser.parse_args()
    
    # Convert git cache minutes to seconds for internal use
    git_cache_seconds = args.git_cache_minutes * 60
    
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

    # Setup paths
    dirname = os.path.dirname(lamd.__file__)
    make_dir = os.path.join(dirname, "makefiles")
    includes_dir = os.path.join(dirname, "includes")
    script_dir = os.path.join(dirname, "scripts")

    # Create makefile with configuration
    with profiler.measure("Makefile generation"):
        with open("makefile", "w+") as f:
            f.write(f"BASE={base}\n")
            f.write(f"MAKEFILESDIR={make_dir}\n")
            f.write(f"INCLUDESDIR={includes_dir}\n")
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
            f.write("include $(MAKEFILESDIR)/make-cv-flags.mk\n")
            f.write("include $(MAKEFILESDIR)/make-lists.mk\n")
            f.write("include $(MAKEFILESDIR)/make-cv.mk\n")

    # Update external dependencies if needed
    with profiler.measure("Dependency git pulls"):
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
                # Smart pull: only pull if not recently checked (within last hour)
                # This avoids repeated network calls for short build cycles
                import subprocess
                import time
                
                fetch_head = os.path.join(git_dir, "FETCH_HEAD")
                should_check_remote = True
                
                # If FETCH_HEAD exists and is recent enough, skip remote check
                if os.path.exists(fetch_head):
                    fetch_age = time.time() - os.path.getmtime(fetch_head)
                    if fetch_age < git_cache_seconds:
                        should_check_remote = False
                
                if should_check_remote:
                    try:
                        # Fetch remote info to update FETCH_HEAD
                        subprocess.run(
                            ["git", "-C", answer, "fetch"],
                            capture_output=True,
                            timeout=10,
                            check=False
                        )
                        
                        # Check if behind remote
                        result = subprocess.run(
                            ["git", "-C", answer, "status", "-uno", "-sb"],
                            capture_output=True,
                            text=True,
                            timeout=5,
                            check=False
                        )
                        
                        # Only pull if behind
                        if "behind" in result.stdout.lower():
                            os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")
                        
                    except (subprocess.TimeoutExpired, Exception):
                        # If check fails, do safe pull
                        os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")
                # else: recently checked, skip pull
            else:
                print(f"Warning: {answer} is not a git repository. Skipping git pull.")

    # Check for postsdir
    with profiler.measure("Config validation (postsdir)"):
        if "postsdir" not in iface:
            print("Error: 'postsdir' is not defined in your _lamd.yml configuration file.")
            print("Please add a 'postsdir' entry pointing to your posts directory.")
            print("Example:")
            print("postsdir: ../_posts")
            sys.exit(1)

    # Make sure we have the latest files if in a git repo
    with profiler.measure("Local git pull"):
        # Smart pull: only pull if not recently checked (within last hour)
        import subprocess
        import time
        
        # Find git root directory (might be in parent dir)
        try:
            git_root = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                timeout=1,
                check=False
            )
            git_dir = git_root.stdout.strip() if git_root.returncode == 0 else None
        except:
            git_dir = None
        
        should_check_remote = False
        
        if git_dir and os.path.isdir(git_dir):
            fetch_head = os.path.join(git_dir, "FETCH_HEAD")
            should_check_remote = True
            
            # If FETCH_HEAD exists and is recent enough, skip remote check
            if os.path.exists(fetch_head):
                fetch_age = time.time() - os.path.getmtime(fetch_head)
                if fetch_age < git_cache_seconds:
                    should_check_remote = False
        
        if should_check_remote:
            try:
                # Fetch remote info
                subprocess.run(
                    ["git", "fetch"],
                    capture_output=True,
                    timeout=10,
                    check=False
                )
                
                # Check if behind remote
                result = subprocess.run(
                    ["git", "status", "-uno", "-sb"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False
                )
                
                # Only pull if behind
                if "behind" in result.stdout.lower():
                    os.system("git pull")
                
            except (subprocess.TimeoutExpired, Exception):
                # If check fails, do safe pull
                os.system("git pull")
        # else: recently checked or not in git repo, skip pull

    # Enable server mode by default (4x faster), unless --no-server is specified
    if not args.no_server:
        os.environ["LAMD_USE_SERVER_CLIENT"] = "1"

    # Final build step (this is where most of the time is spent)
    with profiler.measure("Make execution (total)"):
        result = os.system("make all")
    
    # Generate profiling report if enabled
    if args.profile:
        profiler.report()
        profiler.cleanup()
    
    return result


if __name__ == "__main__":
    sys.exit(main())
