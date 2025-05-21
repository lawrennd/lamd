import os
import sys
import argparse
import subprocess
import shutil

def setup_gpp_arguments(args: argparse.Namespace, iface: dict) -> list:
    """Set up GPP arguments based on command line args and interface config.
    
    :param args: Command line arguments
    :type args: argparse.Namespace
    :param iface: Interface configuration
    :type iface: dict
    :return: List of GPP arguments
    :rtype: list
    """
    # Basic arguments
    arglist = ["+n", '-U "\\" "" "{" "}{" "}" "{" "}" "#" ""']
    
    # Add format-specific arguments
    if args.to:
        arglist.append(f"-D{args.to.upper()}=1")
    if args.format:
        arglist.append(f"-D{args.format.upper()}=1")
    
    # Add feature flags
    feature_flags = {
        "exercises": "EXERCISES",
        "assignment": "ASSIGNMENT",
        "edit_links": "EDIT",
        "draft": "DRAFT"
    }
    for arg_name, flag in feature_flags.items():
        if getattr(args, arg_name):
            arglist.append(f"-D{flag}=1")
    
    # Add metadata
    if args.meta_data:
        for a in args.meta_data:
            arglist.append(f"-D{a}")
    
    # Handle code inclusion options
    if args.code is not None and args.code != "none":
        arglist.append("-DCODE=1")
        code_flags = {
            "ipynb": ["DISPLAYCODE", "PLOTCODE", "HELPERCODE", "MAGICCODE"],
            "diagnostic": ["DISPLAYCODE", "HELPERCODE", "PLOTCODE", "MAGICCODE"],
            "full": ["DISPLAYCODE", "HELPERCODE", "PLOTCODE", "MAGICCODE"],
            "plot": ["HELPERCODE", "PLOTCODE"]
        }
        if args.code in code_flags:
            arglist.extend([f"-D{flag}=1" for flag in code_flags[args.code]])
    
    # Add directory definitions
    url = iface.get("diagramsurl", iface.get("url", "") + iface.get("baseurl", ""))
    diagrams_dir = url + iface.get("diagramsdir", "diagrams") if args.to in ["html", "ipynb"] else iface.get("diagramsdir", "diagrams")
    scripts_dir = iface.get("scriptsdir", "scripts")
    write_diagrams_dir = iface.get("writediagramsdir", "diagrams")
    
    # Override with command line arguments
    if args.diagrams_dir:
        diagrams_dir = args.diagrams_dir
    if args.scripts_dir:
        scripts_dir = args.scripts_dir
    if args.write_diagrams_dir:
        write_diagrams_dir = args.write_diagrams_dir
    
    arglist.extend([
        f"-DdiagramsDir={diagrams_dir}",
        f"-DscriptsDir={scripts_dir}",
        f"-DwriteDiagramsDir={write_diagrams_dir}",
        "-Dtalksdir=/Users/neil/lawrennd/talks",
        "-DgithubBaseUrl=https://github.com/lawrennd/snippets/edit/main/"
    ])
    
    # Add include paths
    if args.include_path:
        for include_dir in args.include_path.split(":"):
            arglist.append(f"-I{include_dir}")
    arglist.append(f"-I{MACROS}")
    
    # Add snippets directories
    if args.snippets_path:
        for snippet_dir in args.snippets_path.split(":"):
            arglist.append(f"-I{snippet_dir}")
    arglist.append("-I.")
    
    # Set output file if specified
    if args.output:
        arglist.append(f"-o {args.output}")
    
    return arglist

def check_dependency(dependency_name: str) -> bool:
    """Check if a dependency is installed and accessible.

    :param dependency_name: Name of the dependency to check
    :type dependency_name: str
    :return: True if the dependency is available, False otherwise
    :rtype: bool
    """
    return shutil.which(dependency_name) is not None

def check_dependencies() -> None:
    """Check if all required dependencies are installed and accessible.

    :raises RuntimeError: If any required dependency is missing
    """
    required_dependencies = ["gpp"]
    missing_dependencies = [dep for dep in required_dependencies if not check_dependency(dep)]
    if missing_dependencies:
        raise RuntimeError(f"Missing required dependencies: {', '.join(missing_dependencies)}")

def main() -> int:
    """Markdown Preprocessor for academic content.

    This utility preprocesses markdown files with the Generic Preprocessor (gpp),
    handling macros, includes, and conditional content for different output formats.
    It supports generating slides, notes, and code outputs from a single source.

    :return: Exit code (0 for success, 1 for error)
    :rtype: int
    """
    parser = argparse.ArgumentParser(
        description="Preprocess markdown files with macros and conditionals for academic content.",
        epilog="For full documentation, visit: https://github.com/lawrennd/lamd",
    )


    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output for detailed processing information")

    args = parser.parse_args()

    # If only help was requested, we can return now without loading config
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        return 0

    try:
        # Check dependencies
        check_dependencies()

        # Validate input file
        validate_file_exists(args.filename, "input markdown file")

        # Validate output format if specified
        if args.to:
            validate_output_format(args.to, VALID_OUTPUT_FORMATS)

        # Validate content format if specified
        if args.format:
            validate_output_format(args.format, VALID_FORMATS)

        # Validate code level
        validate_code_level(args.code, VALID_CODE_LEVELS)

        # Validate include paths and snippets path
        if args.include_path:
            validate_include_paths(args.include_path)
        if args.snippets_path:
            validate_directory_exists(args.snippets_path, "snippets directory")

        # Validate metadata
        if args.meta_data:
            validate_metadata(args.meta_data)

        # Load configuration
        iface = load_config()

        # Set up GPP arguments
        arglist = setup_gpp_arguments(args, iface)

        # Process includes
        before_text, after_text = process_includes(args)

        # Process content
        writepost = process_content(args, before_text, after_text)

        # Write temporary file
        tmp_file, ext = os.path.splitext(args.filename)
        tmp_file += ".gpp.markdown"
        with open(tmp_file, "wb") as fd:
            fm.dump(writepost, fd, sort_keys=False, default_flow_style=False)

        # Run GPP
        runlist = ["gpp"] + arglist + [tmp_file]
        run_command = " ".join(runlist)
        if args.verbose:
            print(f"Running command: {run_command}")
        os.system(run_command)
        return 0

    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1 