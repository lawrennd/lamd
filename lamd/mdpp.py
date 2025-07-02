#!/usr/bin/env python3
"""
Markdown Preprocessor for academic content.

This module provides a command-line tool for preprocessing markdown files with the Generic Preprocessor (gpp).
It handles macros, includes, and conditional content for different output formats, supporting generation of
slides, notes, and code outputs from a single source.

:requires: gpp (the generic preprocessor) to be installed https://math.berkeley.edu/~auroux/software/gpp.html
"""

import argparse
import os
import sys
from typing import Any

import frontmatter as fm

from lamd.config.interface import Interface
from lamd.validation import (
    ValidationError,
    validate_code_level,
    validate_directory_exists,
    validate_file_exists,
    validate_include_paths,
    validate_metadata,
    validate_output_format,
)

MACROS = os.path.join(os.path.dirname(__file__), "macros")
INCLUDES = os.path.join(os.path.dirname(__file__), "includes")

VALID_FORMATS = ["notes", "slides", "code"]
VALID_CODE_LEVELS = ["none", "sparse", "ipynb", "diagnostic", "plot", "full"]
VALID_OUTPUT_FORMATS = ["pptx", "html", "docx", "ipynb", "svg", "tex", "python"]


def setup_gpp_arguments(args: argparse.Namespace, iface: dict[str, Any]) -> list[str]:
    """Set up arguments for gpp.

    Args:
        args: Command line arguments.
        iface: Interface configuration.

    Returns:
        list[str]: List of gpp arguments.
    """
    gpp_args = ["+n", '-U "\\\\" "" "{" "}{" "}" "{" "}" "#" ""']

    # Add format-specific arguments
    if args.to == "html":
        gpp_args.append("-DHTML=1")
    if args.format == "slides":
        gpp_args.append("-DSLIDES=1")
    if args.exercises:
        gpp_args.append("-DEXERCISES=1")
    if args.assignment:
        gpp_args.append("-DASSIGNMENT=1")
    if args.edit_links:
        gpp_args.append("-DEDIT=1")
    if args.draft:
        gpp_args.append("-DDRAFT=1")

    # Add metadata arguments
    for meta in args.meta_data:
        gpp_args.append(f"-D{meta}")

    # Add code-specific arguments
    if args.code == "ipynb":
        gpp_args.extend(["-DCODE=1", "-DDISPLAYCODE=1", "-DPLOTCODE=1", "-DHELPERCODE=1", "-DMAGICCODE=1"])

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

    gpp_args.append(f"-DdiagramsDir={diagrams_dir}")
    gpp_args.append(f"-DscriptsDir={scripts_dir}")
    gpp_args.append(f"-DwriteDiagramsDir={write_diagrams_dir}")

    # Add include paths
    gpp_args.append(f"-Dtalksdir={os.path.dirname(os.path.abspath(__file__))}")
    gpp_args.append("-DgithubBaseUrl=https://github.com/lawrennd/snippets/edit/main/")
    if args.include_path:
        for include_dir in args.include_path.split(":"):
            gpp_args.append(f"-I{include_dir}")

    if args.snippets_path:
        for snippet_dir in args.snippets_path.split(":"):
            gpp_args.append(f"-I{snippet_dir}")
    gpp_args.append("-I.")

    if args.macros_path:
        for macro_dir in args.macros_path.split(":"):
            gpp_args.append(f"-I{macro_dir}")

    # Add output file
    gpp_args.append(f"-o {args.output}")

    return gpp_args


def process_includes(args: argparse.Namespace) -> tuple[str, str]:
    """Process include files and return before/after text.

    :param args: Command line arguments
    :type args: argparse.Namespace
    :return: Tuple of (before_text, after_text)
    :rtype: tuple
    """
    # Process before-body includes
    before_text = ""
    if args.include_before_body:
        with open(args.include_before_body, "r") as fd:
            before_text = fd.read()

    # Handle LaTeX notation replacement
    if args.replace_notation:
        before_text += "\n\n"
        with open(os.path.join(INCLUDES, "talk-notation.tex"), "r") as fd:
            before_text += fd.read()

    # Search for talk-macros.gpp in the macros path
    try:
        talk_macros_file = next(
            os.path.join(macros_dir, "talk-macros.gpp")
            for macros_dir in args.macros_path.split(":")
            if os.path.isfile(os.path.join(macros_dir, "talk-macros.gpp"))
        )
        with open(talk_macros_file) as f:
            before_text += f.read()
    except StopIteration:
        raise FileNotFoundError("talk-macros.gpp not found in any directory in macros_path")

    # Process after-body includes
    after_text = ""
    if args.include_after_body:
        with open(args.include_after_body, "r") as fd:
            after_text = fd.read()

    return before_text, after_text


def load_config() -> dict[str, Any]:
    """Load interface configuration from files.

    :return: Interface configuration
    :rtype: dict
    """
    try:
        config: dict[str, Any] = Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")
        return config
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("Continuing with default settings...", file=sys.stderr)
        return {"url": "", "baseurl": "", "diagramsdir": "diagrams", "scriptsdir": "scripts", "writediagramsdir": "diagrams"}


def process_content(args: argparse.Namespace, before_text: str, after_text: str) -> fm.Post:
    """Process content from input file and includes.

    :param args: Command line arguments
    :type args: argparse.Namespace
    :param before_text: Text to include before content
    :type before_text: str
    :param after_text: Text to include after content
    :type after_text: str
    :return: Processed post object
    :rtype: frontmatter.Post
    """
    # Load default configuration
    default_files = ["_lamd.yml", "_config.yml"]
    found_file = False
    for file in default_files:
        if os.path.isfile(file):
            found_file = True
            with open(file, "r") as f:
                writepost = fm.load(f)
            break
    if not found_file:
        writepost = fm.loads("")

    # Load content
    if args.no_header:
        with open(args.filename) as f:
            writepost.content = f.read()
    else:
        with open(args.filename) as f:
            post = fm.load(f)
        writepost.metadata.update(post.metadata)
        writepost.content = post.content

    # Combine content
    writepost.content = before_text + writepost.content + after_text
    return writepost


def main() -> int:
    """Markdown Preprocessor for academic content.

    This utility preprocesses markdown files with the Generic Preprocessor (gpp),
    handling macros, includes, and conditional content for different output formats.
    It supports generating slides, notes, and code outputs from a single source.

    :return: Exit code (0 for success, 1 for error)
    :rtype: int

    :example:
        Process a markdown file for HTML slides::

            mdpp input.md -o output.md -t html -F slides

        Generate notes with code examples::

            mdpp input.md -o output.md -F notes -c ipynb

        Include exercises in the output::

            mdpp input.md -o output.md -e
    """
    parser = argparse.ArgumentParser(
        description="Preprocess markdown files with macros and conditionals for academic content.",
        epilog="For full documentation, visit: https://github.com/lawrennd/lamd",
    )

    parser.add_argument("filename", type=str, help="Input markdown file to process")

    parser.add_argument("-o", "--output", type=str, help="Output filename (defaults to stdout if not specified)")

    parser.add_argument(
        "--no-header", default=False, action="store_true", help="Do not search for a YAML header in the input file"
    )

    parser.add_argument("-B", "--include-before-body", type=str, help="File to include before the main content body")

    parser.add_argument("-A", "--include-after-body", type=str, help="File to include after the main content body")

    parser.add_argument(
        "-t",
        "--to",
        type=str,
        choices=VALID_OUTPUT_FORMATS,
        help="Target output file format (affects conditional content)",
    )

    parser.add_argument(
        "-w", "--whitespace", default=True, action="store_true", help="Remove excess whitespace from preprocessed files"
    )

    parser.add_argument("-I", "--include-path", type=str, help="Colon-separated list of directories to search for includes")

    parser.add_argument(
        "-S", "--snippets-path", type=str, help="Colon-separated list of directories to search for code snippets"
    )

    parser.add_argument(
        "-M", "--macros-path", type=str, help="Colon-separated list of directories to search for *.gpp macro files"
    )

    parser.add_argument(
        "-F",
        "--format",
        type=str,
        choices=VALID_FORMATS,
        help="Target content format: 'notes' for detailed text, 'slides' for presentations, 'code' for code-focused output",
    )

    parser.add_argument(
        "-c",
        "--code",
        type=str,
        default="none",
        choices=VALID_CODE_LEVELS,
        help=(
            """Code inclusion level: 'none' omits code, 'sparse' """
            """includes minimal code, 'ipynb' for notebook """
            """code, 'diagnostic' for debugging, 'plot' for """
            """visualization code, 'full' for all code"""
        ),
    )

    parser.add_argument(
        "-e", "--exercises", default=False, action="store_true", help="Include exercise sections in the output"
    )

    parser.add_argument(
        "-a",
        "--assignment",
        default=False,
        action="store_true",
        help="Format the document as an assignment rather than regular notes",
    )

    parser.add_argument("-d", "--diagrams-dir", type=str, help="Directory containing diagram files referenced in the content")

    parser.add_argument("-s", "--scripts-dir", type=str, help="Directory containing JavaScript files for interactive content")

    parser.add_argument("-W", "--write-diagrams-dir", type=str, help="Directory where generated diagrams should be written")

    parser.add_argument(
        "-D",
        "--draft",
        default=False,
        action="store_true",
        help="Mark the document as a draft, which may affect styling and add draft watermarks",
    )

    parser.add_argument(
        "-E", "--edit-links", default=False, action="store_true", help="Include edit links in the output for online editing"
    )

    parser.add_argument(
        "-r",
        "--replace-notation",
        default=False,
        action="store_true",
        help="Replace LaTeX macros in the files rather than retaining them for later processing",
    )

    parser.add_argument(
        "-m",
        "--meta-data",
        nargs="*",
        default=[],
        help="Additional metadata definitions to pass to the preprocessor (format: KEY=VALUE)",
    )

    parser.add_argument(
        "-x",
        "--extract-material",
        type=str,
        default="all",
        choices=["all", "reading", "references", "exercises"],
        help=(
            """Extract only specific material: 'all' for """
            """everything, 'reading' for reading material, """
            """'references' for citations, 'exercises' for """
            """practice problems"""
        ),
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output for detailed processing information"
    )

    args = parser.parse_args()

    # If only help was requested, we can return now without loading config
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        return 0

    try:
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
            validate_include_paths(args.include_path, "include paths")
        if args.snippets_path:
            validate_include_paths(args.snippets_path, "snippets paths")
        if args.macros_path:
            validate_include_paths(args.macros_path, "macro paths")
        else:
            raise ValidationError(
                "The '--macros-path' option must be specified to indicate the directory containing *.gpp files."
            )

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


if __name__ == "__main__":
    sys.exit(main())
