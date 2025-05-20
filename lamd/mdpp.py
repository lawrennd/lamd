#!/usr/bin/env python3
# Markdown Preprocessor for talks.
# Requries gpp (the generic preprocessor) to be installed https://math.berkeley.edu/~auroux/software/gpp.html.

import argparse
import os
import sys

import frontmatter as fm

from lamd.config.interface import Interface

MACROS = os.path.join(os.path.dirname(__file__), "macros")
INCLUDES = os.path.join(os.path.dirname(__file__), "includes")


def main() -> int:
    """
    Markdown Preprocessor for academic content.

    This utility preprocesses markdown files with the Generic Preprocessor (gpp),
    handling macros, includes, and conditional content for different output formats.
    It supports generating slides, notes, and code outputs from a single source.

    Examples:
        # Process a markdown file for HTML slides
        mdpp input.md -o output.md -t html -F slides

        # Generate notes with code examples
        mdpp input.md -o output.md -F notes -c ipynb

        # Include exercises in the output
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
        choices=["pptx", "html", "docx", "ipynb", "svg", "tex", "python"],
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
        "-F",
        "--format",
        type=str,
        choices=["notes", "slides", "code"],
        help="Target content format: 'notes' for detailed text, 'slides' for presentations, 'code' for code-focused output",
    )

    parser.add_argument(
        "-c",
        "--code",
        type=str,
        default="none",
        choices=["none", "sparse", "ipynb", "diagnostic", "plot", "full"],
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
        "-m", "--meta-data", nargs="*", help="Additional metadata definitions to pass to the preprocessor (format: KEY=VALUE)"
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

    args = parser.parse_args()

    # If only help was requested, we can return now without loading config
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        return 0

    # Now load the interface configuration
    try:
        iface = Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        print("Continuing with default settings...", file=sys.stderr)
        # Create a minimal default configuration
        iface = {}
        iface.setdefault("url", "")
        iface.setdefault("baseurl", "")
        iface.setdefault("diagramsdir", "diagrams")
        iface.setdefault("scriptsdir", "scripts")
        iface.setdefault("writediagramsdir", "diagrams")

    # Processing URL and paths
    if "diagramsurl" in iface:
        url = iface["diagramsurl"]
    else:
        url = iface.get("url", "") + iface.get("baseurl", "")

    # Set up diagram directory based on output format
    if args.to == "html" or args.to == "ipynb":
        diagrams_dir = url + iface.get("diagramsdir", "diagrams")
    else:
        diagrams_dir = iface.get("diagramsdir", "diagrams")

    scripts_dir = iface.get("scriptsdir", "scripts")
    write_diagrams_dir = iface.get("writediagramsdir", "diagrams")

    # Override with command line arguments if provided
    if args.diagrams_dir:
        diagrams_dir = args.diagrams_dir

    if args.scripts_dir:
        scripts_dir = args.scripts_dir

    if args.write_diagrams_dir:
        write_diagrams_dir = args.write_diagrams_dir

    # Set up GPP arguments
    arglist = ["+n", '-U "\\" "" "{" "}{" "}" "{" "}" "#" ""']
    if args.to:
        arglist.append("-D{to}=1".format(to=args.to.upper()))
    if args.format:
        arglist.append("-D{format}=1".format(format=args.format.upper()))
    if args.exercises:
        arglist.append("-DEXERCISES=1")
    if args.assignment:
        arglist.append("-DASSIGNMENT=1")
    if args.edit_links:
        arglist.append("-DEDIT=1")
    if args.draft:
        arglist.append("-DDRAFT=1")
    if args.meta_data:
        for a in args.meta_data:
            arglist.append("-D" + a)

    if args.extract_material is not None and args.code != "all":
        pass

    # Handle code inclusion options
    if args.code is not None and args.code != "none":
        arglist.append("-DCODE=1")
        if args.code == "ipynb":
            arglist.append("-DDISPLAYCODE=1")
            arglist.append("-DPLOTCODE=1")
            arglist.append("-DHELPERCODE=1")
            arglist.append("-DMAGICCODE=1")
        elif args.code == "diagnostic":
            arglist.append("-DDISPLAYCODE=1")
            arglist.append("-DHELPERCODE=1")
            arglist.append("-DPLOTCODE=1")
            arglist.append("-DMAGICCODE=1")
        elif args.code == "full":
            arglist.append("-DDISPLAYCODE=1")
            arglist.append("-DHELPERCODE=1")
            arglist.append("-DPLOTCODE=1")
            arglist.append("-DMAGICCODE=1")
        if args.code == "plot":
            arglist.append("-DHELPERCODE=1")
            arglist.append("-DPLOTCODE=1")

    # Add directory definitions
    arglist.append(f"-DdiagramsDir={diagrams_dir}")
    arglist.append(f"-DscriptsDir={scripts_dir}")
    arglist.append(f"-DwriteDiagramsDir={write_diagrams_dir}")
    talks_dir = "/Users/neil/lawrennd/talks"
    arglist.append(f"-Dtalksdir={talks_dir}")
    github_baseurl = "https://github.com/lawrennd/snippets/edit/main/"
    arglist.append(f"-DgithubBaseUrl={github_baseurl}")

    # Set up include paths
    if args.include_path:
        for include_dir in args.include_path.split(":"):
            arglist.append(f"-I{include_dir}")
    arglist.append("-I{macro_path}".format(macro_path=MACROS))

    # Add snippets directories
    if args.snippets_path:
        for snippet_dir in args.snippets_path.split(":"):
            arglist.append(f"-I{snippet_dir}")
    arglist.append("-I.")

    # Set output file if specified
    if args.output:
        arglist.append("-o {}".format(args.output))

    # Process include files
    if args.include_before_body:
        with open(args.include_before_body, "r") as fd:
            before_text = fd.read()
    else:
        before_text = ""

    # Handle LaTeX notation replacement
    if args.replace_notation:
        before_text += "\n\n"
        with open(os.path.join(INCLUDES, "talk-notation.tex"), "r") as fd:
            before_text += fd.read()

    # Read in talk-macros.gpp which loads in the other macro files
    with open(os.path.join(MACROS, "talk-macros.gpp")) as f:
        before_text += f.read()

    # Process after-body includes
    if args.include_after_body:
        with open(args.include_after_body, "r") as fd:
            after_text = fd.read()
    else:
        after_text = ""

    # Try _lamd.yml for default entries then _config.yml
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

    if args.no_header:
        with open(args.filename) as f:
            writepost.content = f.read()

    else:
        with open(args.filename) as f:
            post = fm.load(f)
        writepost.metadata.update(post.metadata)
        writepost.content = post.content

    writepost.content = before_text + writepost.content + after_text

    tmp_file, ext = os.path.splitext(args.filename)
    tmp_file += ".gpp.markdown"

    with open(tmp_file, "wb") as fd:
        fm.dump(writepost, fd, sort_keys=False, default_flow_style=False)

    runlist = ["gpp"] + arglist + [tmp_file]
    run_command = " ".join(runlist)
    print(run_command)
    os.system(run_command)
    return 0


if __name__ == "__main__":
    sys.exit(main())
