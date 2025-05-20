#!/usr/bin/env python
"""
Script to generate people macros for LAMD system.

This script creates macros for displaying people's images and information in a consistent format
across different documents. It takes a YAML file that defines people's information and generates
LaTeX/GPP macros that can be included in documents.

Each person's macro allows displaying their image in a circular format with optional URL links,
titles, and custom image cropping. The script automatically generates appropriate macro names
based on the person's name.

Usage:
    python -m lamd.mdpeople --input people.yaml [--output talk-people.gpp]

Where:
    people.yaml: A YAML file containing people information
    talk-people.gpp: Output file for the generated macros (default: talk-people.gpp)

Example YAML format:
    - given: Jane
      family: Doe
      image: people/jane-doe.jpg
      url: https://example.com/jane
      title: Professor

    - given: John
      family: Smith
      image: people/john-smith.jpg
      crop:
        llx: 0
        lly: 0
        urx: 100
        ury: 100
"""

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def create_circle_head_macro() -> str:
    """Creates the base circleHead macro that other macros will use.

    Returns:
        str: The macro definition for circleHead
    """
    return r"""
\define{\circleHead{filename}{alttext}{width}{circleurl}}{
\ifndef{urlCount}\define{urlCount}{0}\else\defeval{urlCount}{\eval{\urlCount+1}}\endif
<svg viewBox="0 0 200 200" style="width:\width">
<defs>
<clipPath id="clip\urlCount">
<style>
circle {
  fill: black;
}
</style>
<circle cx="100" cy="100" r="100"/>
</clipPath>
</defs><title>\alttext</title><image preserveAspectRatio="xMinYMin slice" width="100%" xlink:href="\filename" clip-path="url(#clip\urlCount)"/></svg>}
"""


def create_person_macro(
    given: str,
    family: str,
    image_path: str,
    url: Optional[str] = None,
    title: Optional[str] = None,
    crop: Optional[Dict[str, int]] = None,
) -> str:
    """Creates a macro for a specific person.

    Args:
        given: Person's given name
        family: Person's family name
        image_path: Path to their image
        url: Optional URL for their webpage
        title: Optional title/position
        crop: Optional crop coordinates {llx, lly, urx, ury}

    Returns:
        str: The macro definition for this person
    """
    # Create macro name from person's name
    given_lowered = given[0].lower() + given[1:]
    macro_name = given_lowered + family
    macro_name = macro_name.replace(" ", "").replace("-", "").replace(".", "")
    macro_name = "".join(c for c in macro_name if c.isalnum())

    diagrams_dir = "\\diagramsDir" + "/" + image_path

    # Create display name - use title if available, otherwise combine given and family names
    display_name = title if title else f"{given} {family}"

    if crop:
        # Handle cropped images
        macro = rf"""\\defeval{{\\{macro_name}Picture{{width}}}}{{\\circleHead{{\includeimgclip{{{diagrams_dir}}}{{{crop['llx']}}}{{{crop['lly']}}}{{{crop['urx']}}}{{{crop['ury']}}}}}{{{display_name}}}{{\width}}"""
    else:
        # Standard image handling
        macro = rf"""\\defeval{{\\{macro_name}Picture{{width}}}}{{\\circleHead{{{diagrams_dir}}}{{{display_name}}}{{\width}}"""

    if url:
        macro += rf"{{{url}}}"

    macro += "}"
    return macro


def generate_macros_file(people: List[Dict[str, Any]], output_file: str = "talk-people.gpp") -> None:
    """Generates a complete macro file for all people.

    Args:
        people: List of dictionaries with people information
        output_file: File to write macros to
    """
    with open(output_file, "w") as f:
        # Write header
        f.write(
            r"""\ifndef{talkPeople}
\define{talkPeople}
"""
        )

        # Write base circle head macro
        f.write(create_circle_head_macro())

        # Write each person's macro
        for person_info in people:
            macro = create_person_macro(
                person_info["given"],
                person_info["family"],
                person_info["image"],
                person_info.get("url"),
                person_info.get("title"),
                person_info.get("crop"),
            )
            f.write(f"\n{macro}\n")

        # Write footer
        f.write(
            r"""
\endif
"""
        )


def main() -> int:
    """Main function to parse arguments and generate macros.

    Returns:
        int: Exit code (0 for success)
    """
    parser = argparse.ArgumentParser(description="Generate people macros for LAMD")
    parser.add_argument("--input", "-i", type=str, required=True, help="Input YAML file with people information")
    parser.add_argument("--output", "-o", type=str, default="talk-people.gpp", help="Output file for macros")

    args = parser.parse_args()

    try:
        with open(args.input) as f:
            people = yaml.safe_load(f)

        generate_macros_file(people, args.output)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
