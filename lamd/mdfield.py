#!/usr/bin/env python3
"""
Utility to extract fields from markdown document headers.

This script extracts metadata fields from markdown document frontmatter (YAML headers)
or falls back to configuration files if the field isn't found in the document.

Supports server mode for fast repeated access via lynguine server.
"""

import argparse
import os
import sys
from typing import Optional

import lynguine.util.talk as nt
import lynguine.util.yaml as ny

from lamd.config.interface import Interface

# Server mode support (optional dependency)
try:
    from lynguine.client import ServerClient
    SERVER_MODE_AVAILABLE = True
except ImportError:
    SERVER_MODE_AVAILABLE = False
    ServerClient = None


def extract_field_server_mode(field: str, filename: str, config_files: list) -> Optional[str]:
    """
    Extract field using lynguine server mode.

    NOTE: Full server mode integration for mdfield requires lynguine API enhancements
    to expose field extraction via server sessions. This is a placeholder implementation.

    Args:
        field: Field name to extract
        filename: Markdown filename
        config_files: List of config files to check

    Returns:
        Field value or None if not found (currently always returns None)
    """
    # TODO: Implement server mode field extraction
    # This requires:
    # 1. lynguine server to expose Interface field access via sessions
    # 2. API to extract fields from markdown frontmatter via server
    # 3. Session caching by config file path
    #
    # For now, return None to fall back to direct mode
    sys.stderr.write("Note: Server mode for mdfield not yet fully implemented. Using direct mode.\n")
    return None


def main() -> int:
    """
    Extract field values from markdown frontmatter.

    This function parses command line arguments, extracts the requested field
    from the specified markdown file's frontmatter, or falls back to configuration
    files if the field isn't found in the document. It first checks _lamd.yml for
    the field, and only if not found there, checks the markdown file itself.

    Supports server mode for fast repeated access when lynguine server is available.

    Returns:
        int: 0 for success, non-zero for failure
    """
    parser = argparse.ArgumentParser(
        description="Extract field values from markdown document headers.",
        epilog="Examples:\n"
        "  mdfield title document.md         # Extract the title\n"
        "  mdfield date document.md          # Extract the date\n"
        "  mdfield categories document.md    # Extract categories as a formatted list\n"
        "\n"
        "Server mode (faster for multiple calls):\n"
        "  mdfield --use-server title document.md  # Use lynguine server\n"
        "  LAMD_USE_SERVER=1 mdfield title doc.md  # Enable via environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("field", type=str, help="The field to extract from the markdown header")

    parser.add_argument("filename", type=str, help="The markdown file to extract the field from")

    # Server mode options
    parser.add_argument(
        "--use-server",
        action="store_true",
        help="Use lynguine server mode for faster repeated access (requires lynguine server mode)"
    )

    parser.add_argument(
        "--no-server",
        action="store_true",
        help="Force direct mode even if LAMD_USE_SERVER is set"
    )

    args = parser.parse_args()

    # Determine if we should use server mode
    use_server = args.use_server or (os.environ.get("LAMD_USE_SERVER", "0") == "1")
    if args.no_server:
        use_server = False

    # Check if server mode is available
    if use_server and not SERVER_MODE_AVAILABLE:
        sys.stderr.write("Warning: Server mode requested but lynguine.client not available. Falling back to direct mode.\n")
        use_server = False

    # Extract the field value
    config_files = ["_lamd.yml", "_config.yml"]

    if use_server:
        # Use server mode for faster access
        answer = extract_field_server_mode(args.field, args.filename, config_files)
        if answer is None:
            # Server mode failed, fall back to direct mode
            sys.stderr.write("Server mode failed, using direct mode\n")
            use_server = False

    if not use_server:
        # Direct mode (original implementation)
        try:
            answer = nt.talk_field(args.field, args.filename, user_file=config_files)
        except ny.FileFormatError:
            # If markdown file doesn't have the field, try _lamd.yml
            try:
                iface = Interface.from_file(user_file=config_files, directory=".")
                if args.field in iface:
                    answer = iface[args.field]
                else:
                    answer = ""
            except Exception as e:
                # If we can't access config files, return empty string
                sys.stderr.write(f"Error accessing configuration: {e}\n")
                answer = ""
        except Exception as e:
            # If we can't access config files, return empty string
            sys.stderr.write(f"Error accessing configuration: {e}\n")
            answer = ""

    # Handle different types of output
    if type(answer) is str:
        # Expand environment variables in paths
        answer = os.path.expandvars(answer)
        print(answer)
    elif args.field == "categories" and isinstance(answer, list):
        # Format categories as a string list
        print("['" + "', '".join(answer) + "']")
    else:
        # Print other types as-is
        print(answer)

    return 0


if __name__ == "__main__":
    sys.exit(main())
