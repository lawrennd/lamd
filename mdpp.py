import os
import sys
import argparse
import subprocess
import shutil
import yaml
from lamd.validation import (
    ValidationError,
    FileNotFoundError,
    DirectoryNotFoundError,
    ArgumentValidationError,
    DependencyError,
    validate_file_exists,
    validate_directory_exists,
    validate_include_paths,
    validate_output_format,
    validate_code_level,
    validate_metadata,
    resolve_dependencies,
)

# Constants for validation
VALID_OUTPUT_FORMATS = ["html", "pdf", "ipynb"]
VALID_FORMATS = ["slides", "notes", "article"]
VALID_CODE_LEVELS = ["none", "ipynb", "diagnostic", "full", "plot"]


def load_config() -> dict:
    """Load configuration from _lamd.yml file.

    :return: Configuration dictionary
    :rtype: dict
    """
    config_file = "_lamd.yml"
    if not os.path.exists(config_file):
        return {}

    with open(config_file, "r") as f:
        return yaml.safe_load(f) or {}


def process_includes(args: argparse.Namespace) -> tuple[str, str]:
    """Process include files.

    :param args: Command line arguments
    :type args: argparse.Namespace
    :return: Tuple of (before_text, after_text)
    :rtype: tuple[str, str]
    """
    return "", ""  # Placeholder implementation


def process_content(args: argparse.Namespace, before_text: str, after_text: str) -> dict:
    """Process content with GPP.

    :param args: Command line arguments
    :type args: argparse.Namespace
    :param before_text: Text to insert before content
    :type before_text: str
    :param after_text: Text to insert after content
    :type after_text: str
    :return: Processed content
    :rtype: dict
    """
    return {}  # Placeholder implementation


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
    feature_flags = {"exercises": "EXERCISES", "assignment": "ASSIGNMENT", "edit_links": "EDIT", "draft": "DRAFT"}
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
            "plot": ["HELPERCODE", "PLOTCODE"],
        }
        if args.code in code_flags:
            arglist.extend([f"-D{flag}=1" for flag in code_flags[args.code]])

    # Add directory definitions
    url = iface.get("diagramsurl", iface.get("url", "") + iface.get("baseurl", ""))
    diagrams_dir = (
        url + iface.get("diagramsdir", "diagrams") if args.to in ["html", "ipynb"] else iface.get("diagramsdir", "diagrams")
    )
    scripts_dir = iface.get("scriptsdir", "scripts")
    write_diagrams_dir = iface.get("writediagramsdir", "diagrams")

    # Override with command line arguments
    if args.diagrams_dir:
        diagrams_dir = args.diagrams_dir
    if args.scripts_dir:
        scripts_dir = args.scripts_dir
    if args.write_diagrams_dir:
        write_diagrams_dir = args.write_diagrams_dir

    arglist.extend(
        [
            f"-DdiagramsDir={diagrams_dir}",
            f"-DscriptsDir={scripts_dir}",
            f"-DwriteDiagramsDir={write_diagrams_dir}",
            "-Dtalksdir=/Users/neil/lawrennd/talks",
            "-DgithubBaseUrl=https://github.com/lawrennd/snippets/edit/main/",
        ]
    )

    # Add include paths
    if args.include_path:
        for include_dir in args.include_path.split(":"):
            arglist.append(f"-I{include_dir}")

    # Add snippets directories
    if args.snippets_path:
        for snippet_dir in args.snippets_path.split(":"):
            arglist.append(f"-I{snippet_dir}")

    arglist.append("-I.")

    # Add macros path after -I.
    macros_path = str(args.macros)
    arglist.append(f"-I{macros_path}")

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


def check_version(dependency_name: str, required_version: str) -> bool:
    """Check if a dependency meets the required version.

    :param dependency_name: Name of the dependency to check
    :type dependency_name: str
    :param required_version: Required version of the dependency
    :type required_version: str
    :return: True if the dependency version is compatible, False otherwise
    :rtype: bool
    """
    try:
        result = subprocess.run([dependency_name, "--version"], capture_output=True, text=True)
        installed_version = result.stdout.strip()
        return installed_version >= required_version
    except subprocess.CalledProcessError:
        return False


def check_dependencies() -> None:
    """Check if all required dependencies are installed and accessible.

    :raises RuntimeError: If any required dependency is missing or has an incompatible version
    """
    required_dependencies = {"gpp": "2.24"}
    missing_dependencies = [dep for dep in required_dependencies if not check_dependency(dep)]
    if missing_dependencies:
        raise RuntimeError(f"Missing required dependencies: {', '.join(missing_dependencies)}")

    incompatible_versions = [dep for dep, version in required_dependencies.items() if not check_version(dep, version)]
    if incompatible_versions:
        raise RuntimeError(f"Incompatible versions for dependencies: {', '.join(incompatible_versions)}")


def write_tmp_file(content: dict, filename: str) -> None:
    """Write content to a temporary file.

    :param content: Content to write
    :type content: dict
    :param filename: Name of the file to write
    :type filename: str
    """
    with open(filename, "wb") as fd:
        yaml.dump(content, fd, sort_keys=False, default_flow_style=False)


def run_gpp(args: list) -> None:
    """Run GPP with the given arguments.

    :param args: List of arguments to pass to GPP
    :type args: list
    """
    runlist = ["gpp"] + args
    run_command = " ".join(runlist)
    os.system(run_command)


def cleanup_tmp_file(filename: str) -> None:
    """Clean up temporary file.

    :param filename: Name of the file to clean up
    :type filename: str
    """
    if os.path.exists(filename):
        os.remove(filename)


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

    # Add macros argument
    parser.add_argument("--macros", default="macros", help="Path to macros directory (default: macros)")

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output for detailed processing information"
    )

    parser.add_argument("--auto-install", action="store_true", help="Automatically install missing dependencies")

    # Add positional filename argument
    parser.add_argument("filename", help="Input markdown file")

    args = parser.parse_args()

    # If only help was requested, we can return now without loading config
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        return 0

    try:
        # Check dependencies
        required_dependencies = {
            "gpp": "2.24",  # This should be in pyproject.toml
            "lynguine": "^0.1.0",  # Add other dependencies as needed
        }
        resolve_dependencies(required_dependencies, args.auto_install)

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
        write_tmp_file(writepost, tmp_file)

        # Run GPP
        run_gpp(arglist)
        return 0

    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1
