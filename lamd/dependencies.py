#!/usr/bin/env python3
r"""
Dependencies Module - Extract dependencies from markdown files.

This module identifies and extracts various types of dependencies from markdown files,
including diagrams, input files, bibliography files, and code snippets. It helps track
what files are needed to fully process a markdown document.

Dependencies that can be extracted include:
- All dependencies combined
- Diagrams (PNG, SVG, etc.)
- Special diagram types for different output formats (slides, TeX, Word)
- Input files (included via \include{} commands)
- Bibliography inputs (referenced via \cite{} commands)
- Code snippets (included via macros)

The module leverages lynguine utilities to perform the extraction and outputs
the results as space-separated lists of filenames.

Usage:
    dependencies DEPENDENCY_TYPE FILENAME [options]

Where:
    DEPENDENCY_TYPE: The type of dependency to extract (all, diagrams, inputs, etc.)
    FILENAME: The markdown file to analyze

Options:
    -d, --diagrams-dir DIR: Specify the directory containing diagrams
    -S, --snippets-path DIR: Specify the directory containing snippet files
"""

import sys
import argparse
import lynguine.util.talk as nt
import lynguine.util.yaml as ny


def main():
    """
    Extract dependencies from markdown files based on specified type.

    This function:
    1. Parses command-line arguments for dependency type and filename
    2. Configures paths for diagrams and snippets
    3. Calls the appropriate extraction function based on dependency type
    4. Outputs a space-separated list of dependencies to stdout

    Dependency types:
        all: All dependencies of any type
        diagrams: All diagram files
        slidediagrams: SVG diagrams for slide output
        texdiagrams: PDF diagrams for TeX output
        docxdiagrams: EMF diagrams for Word output
        inputs: Included markdown files
        bibinputs: Bibliography input files
        snippets: Code snippets (temporarily disabled)

    Returns:
        None (prints the list of dependencies to stdout)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dependency",
        type=str,
        choices=[
            "all",
            "diagrams",
            "inputs",
            "bibinputs",
            "slidediagrams",
            "texdiagrams",
            "docxdiagrams",
            # "snippets", # Temporarily disabled as extract_snippets function is not implemented
        ],
        help="The type of dependency that is required",
    )
    parser.add_argument("filename", type=str, help="The filename where dependencies are being searched")

    parser.add_argument("-d", "--diagrams-dir", type=str, help="Directory to find the diagrams in")
    parser.add_argument("-S", "--snippets-path", type=str, help="Directory to find the snippets in")

    args = parser.parse_args()

    diagrams_dir = "/Users/neil/lawrennd/slides/diagrams"
    if args.diagrams_dir:
        diagrams_dir = args.diagrams_dir

    snippets_path = ".."
    if args.snippets_path:
        snippets_path = args.snippets_path

    if args.dependency == "all":
        try:
            # Check if posts: true is set
            fields = ny.header_fields(args.filename)
            posts_enabled = False
            try:
                posts_enabled = ny.header_field("posts", fields, ["_lamd.yml", "_config.yml"])
            except ny.FileFormatError:
                posts_enabled = False
            if posts_enabled:
                # Now check for postsdir
                iface = ny.Interface.from_file(["_lamd.yml", "_config.yml"], directory=".")
                if "postsdir" not in iface:
                    print("Error: 'postsdir' is not defined in your _lamd.yml configuration file.")
                    print("Please add a 'postsdir' entry pointing to your posts directory.")
                    print("Example:")
                    print("postsdir: ../_posts")
                    sys.exit(1)
            listfiles = nt.extract_all(args.filename, user_file=["_lamd.yml", "_config.yml"])
        except ny.FileFormatError as e:
            print(f"Error: {e}")
            sys.exit(1)
        print(" ".join(listfiles))

    elif args.dependency == "diagrams":
        listfiles = nt.extract_diagrams(args.filename, diagrams_dir=diagrams_dir, snippets_path=snippets_path)
        print(" ".join(listfiles))

    elif args.dependency == "slidediagrams":
        listfiles = nt.extract_diagrams(
            args.filename, absolute_path=False, diagram_exts=["svg"], diagrams_dir=diagrams_dir, snippets_path=snippets_path
        )
        print(" ".join(listfiles))

    elif args.dependency == "texdiagrams":
        listfiles = nt.extract_diagrams(
            args.filename, absolute_path=False, diagram_exts=["pdf"], diagrams_dir=diagrams_dir, snippets_path=snippets_path
        )
        print(" ".join(listfiles))

    elif args.dependency == "docxdiagrams":
        listfiles = nt.extract_diagrams(
            args.filename, absolute_path=False, diagram_exts=["emf"], diagrams_dir=diagrams_dir, snippets_path=snippets_path
        )
        print(" ".join(listfiles))

    elif args.dependency == "inputs":
        listfiles = nt.extract_inputs(args.filename, snippets_path=snippets_path)
        if len(listfiles) > 0:
            print(" ".join(listfiles))
        else:
            print("")

    elif args.dependency == "bibinputs":
        listfiles = nt.extract_bibinputs(args.filename)
        print(" ".join(listfiles))

    # Temporarily commented out as extract_snippets function is not implemented in lynguine.util.talk
    # elif args.dependency == "snippets":
    #     listfiles = nt.extract_snippets(args.filename,
    #                                     absolute_path=False,
    #                                     snippets_path=snippets_path)
    #     print(" ".join(listfiles))


if __name__ == "__main__":
    sys.exit(main())
