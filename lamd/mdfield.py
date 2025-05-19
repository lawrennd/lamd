#!/usr/bin/env python3
"""
Utility to extract fields from markdown document headers.

This script extracts metadata fields from markdown document frontmatter (YAML headers)
or falls back to configuration files if the field isn't found in the document.
"""

import sys
import os
import argparse
import lynguine.util.talk as nt
import lynguine.util.yaml as ny

from lamd.config.interface import Interface

def main():
    """
    Extract field values from markdown frontmatter.
    
    This function parses command line arguments, extracts the requested field
    from the specified markdown file's frontmatter, or falls back to configuration
    files if the field isn't found in the document. It first checks _lamd.yml for
    the field, and only if not found there, checks the markdown file itself.
    
    Returns:
        int: 0 for success, non-zero for failure
    """
    parser = argparse.ArgumentParser(
        description="Extract field values from markdown document headers.",
        epilog="Examples:\n"
               "  mdfield title document.md         # Extract the title\n"
               "  mdfield date document.md          # Extract the date\n"
               "  mdfield categories document.md    # Extract categories as a formatted list",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("field",
                        type=str,
                        help="The field to extract from the markdown header")
    
    parser.add_argument("filename",
                        type=str,
                        help="The markdown file to extract the field from")
    
    args = parser.parse_args()

    # First check _lamd.yml for the field
    try:
        iface = Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")
        if args.field in iface:
            answer = iface[args.field]
        else:
            # If not in _lamd.yml, try the markdown file
            try:
                answer = nt.talk_field(args.field, args.filename, user_file=["_lamd.yml", "_config.yml"])
            except ny.FileFormatError:
                answer = ''
    except Exception as e:
        # If we can't access config files, return empty string
        sys.stderr.write(f"Error accessing configuration: {e}\n")
        answer = ''
    
    # Handle different types of output
    if type(answer) is str:
        # Expand environment variables in paths
        answer = os.path.expandvars(answer)
        print(answer)
    elif args.field == 'categories' and isinstance(answer, list):
        # Format categories as a string list
        print("['" + "', '".join(answer) + "']")
    else:
        # Print other types as-is
        print(answer)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
