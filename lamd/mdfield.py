#!/usr/bin/env python3
"""
Utility to extract fields from markdown document headers.

This script extracts metadata fields from markdown document frontmatter (YAML headers)
or falls back to configuration files if the field isn't found in the document.

Supports server mode for fast repeated access via lynguine server.

Commands:
  mdfield <field> <file>           Extract a single field
  mdfield batch <file> --fields <f1> <f2> ...   Extract multiple fields in one call
"""

import argparse
import os
import sys
from typing import Optional, Dict, List

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

    Uses lynguine server's talk_field endpoint for fast field extraction
    from markdown frontmatter with config file fallback.

    Args:
        field: Field name to extract
        filename: Markdown filename
        config_files: List of config files to check

    Returns:
        Field value or None if server mode fails
    """
    try:
        # Create client with auto-start and reasonable timeout
        client = ServerClient(auto_start=True, idle_timeout=300)

        # Extract field using server's talk_field endpoint
        # This wraps lynguine.util.talk.talk_field() with config fallback
        answer = client.extract_talk_field(
            field=field,
            markdown_file=filename,
            config_files=config_files
        )

        # Server returns empty string for missing fields (matching direct mode)
        return answer

    except Exception as e:
        # Server mode failed, return None to trigger fallback
        sys.stderr.write(f"Server mode error: {e}. Falling back to direct mode.\n")
        return None


def extract_field_direct(field: str, filename: str, config_files: list) -> str:
    """
    Extract field in direct mode (no server).

    Args:
        field: Field name to extract
        filename: Markdown filename
        config_files: List of config files to check

    Returns:
        Field value (empty string if not found)
    """
    try:
        answer = nt.talk_field(field, filename, user_file=config_files)
    except ny.FileFormatError:
        # If markdown file doesn't have the field, try _lamd.yml
        try:
            iface = Interface.from_file(user_file=config_files, directory=".")
            if field in iface:
                answer = iface[field]
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
    return answer


def extract_fields_batch(fields: List[str], filename: str, config_files: list, use_server: bool = False) -> Dict[str, str]:
    """
    Extract multiple fields in one call.

    This is much faster than calling mdfield multiple times because:
    - Reads the markdown file once instead of N times
    - Uses single server call instead of N calls
    - Reduces file I/O and startup overhead

    Args:
        fields: List of field names to extract
        filename: Markdown filename
        config_files: List of config files to check
        use_server: Whether to use server mode

    Returns:
        Dictionary mapping field names to their values
    """
    result = {}

    if use_server and SERVER_MODE_AVAILABLE:
        # Try server mode - extract all fields in one call
        try:
            client = ServerClient(auto_start=True, idle_timeout=300)
            for field in fields:
                answer = client.extract_talk_field(
                    field=field,
                    markdown_file=filename,
                    config_files=config_files
                )
                result[field] = answer if answer is not None else ""
            return result
        except Exception as e:
            sys.stderr.write(f"Server mode error: {e}. Falling back to direct mode.\n")
            # Fall through to direct mode

    # Direct mode - still more efficient than multiple calls
    # because we read the file once and extract all fields
    for field in fields:
        result[field] = extract_field_direct(field, filename, config_files)

    return result


def format_field_value(field: str, value) -> str:
    """
    Format a field value for output.

    Args:
        field: Field name
        value: Field value

    Returns:
        Formatted string value
    """
    if isinstance(value, str):
        # Expand environment variables in paths
        return os.path.expandvars(value)
    elif field == "categories" and isinstance(value, list):
        # Format categories as a string list
        return "['" + "', '".join(value) + "']"
    else:
        # Print other types as-is
        return str(value)


def main() -> int:
    """
    Extract field values from markdown frontmatter.

    This function parses command line arguments, extracts the requested field(s)
    from the specified markdown file's frontmatter, or falls back to configuration
    files if the field isn't found in the document.

    Supports server mode for fast repeated access when lynguine server is available.

    Returns:
        int: 0 for success, non-zero for failure
    """
    parser = argparse.ArgumentParser(
        description="Extract field values from markdown document headers.",
        epilog="Examples:\n"
        "  mdfield title document.md                  # Extract single field\n"
        "  mdfield batch document.md --fields date title categories  # Extract multiple fields\n"
        "\n"
        "Server mode (faster for multiple calls):\n"
        "  mdfield --use-server title document.md     # Use lynguine server\n"
        "  LAMD_USE_SERVER=1 mdfield title doc.md     # Enable via environment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Check if first arg is 'batch' to determine mode
    # (Simple approach: if sys.argv contains 'batch', use batch mode)
    is_batch_mode = len(sys.argv) > 1 and sys.argv[1] == "batch"

    if is_batch_mode:
        # Batch mode: extract multiple fields in one call
        parser.add_argument("mode", choices=["batch"], help="Batch extraction mode")
        parser.add_argument("filename", type=str, help="The markdown file to extract fields from")
        parser.add_argument(
            "--fields",
            nargs="+",
            required=True,
            help="Fields to extract (space-separated)"
        )
    else:
        # Single field mode (original behavior)
        parser.add_argument("field", type=str, help="The field to extract from the markdown header")
        parser.add_argument("filename", type=str, help="The markdown file to extract the field from")

    # Server mode options (common to both modes)
    parser.add_argument(
        "--use-server",
        action="store_true",
        help="Use lynguine server mode for faster repeated access"
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

    config_files = ["_lamd.yml", "_config.yml"]

    if is_batch_mode:
        # Batch mode: extract all fields in one call
        results = extract_fields_batch(args.fields, args.filename, config_files, use_server)

        # Output in format: fieldname:value
        for field in args.fields:
            value = results.get(field, "")
            formatted_value = format_field_value(field, value)
            print(f"{field}:{formatted_value}")

    else:
        # Single field mode (original behavior)
        if use_server:
            # Use server mode for faster access
            answer = extract_field_server_mode(args.field, args.filename, config_files)
            if answer is None:
                # Server mode failed, fall back to direct mode
                answer = extract_field_direct(args.field, args.filename, config_files)
        else:
            # Direct mode
            answer = extract_field_direct(args.field, args.filename, config_files)

        # Format and print the result
        formatted = format_field_value(args.field, answer)
        print(formatted)

    return 0


if __name__ == "__main__":
    sys.exit(main())
