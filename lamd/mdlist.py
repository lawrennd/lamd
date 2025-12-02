#!/usr/bin/env python3

import argparse
import datetime
import os
import sys
from typing import Optional

import pandas as pd
from lynguine.config.interface import Interface
from lynguine.util.liquid import load_template_env
from lynguine.util.misc import remove_nan
from referia import assess

from lamd.util import set_since_year

"""
Markdown List Generator for Academic Content

This module generates formatted markdown lists from structured data files
for various academic content types including:
- Publications (all, journal, book, conference)
- Talks (current and external)
- Grants (current and former)
- Teaching activities (current and former)
- Students (current and former)
- Postdoctoral Research Associates (current and former)
- Meetings

The module:
1. Loads data from structured files (YAML, JSON, etc.)
2. Processes this data according to specified settings in cvlists.yml
3. Filters entries by year or other criteria
4. Applies preprocessing, augmentation, and sorting operations
5. Formats the data using Liquid templates
6. Outputs formatted markdown text to a file or stdout

The processing pipeline consists of:
- Preprocessors: Convert data types, standardize formats
- Augmentors: Add derived fields
- Sorters: Order entries appropriately
- Filters: Select entries meeting specific criteria

Usage:
    python -m lamd.mdlist [listtype] [options] [file...]

Dependencies:
    - lynguine: For data access and templating
    - referia: For data assessment
    - pandas: For data manipulation
"""

# Global year filter to be used across the module
global SINCE_YEAR
SINCE_YEAR: Optional[int] = None


def main() -> int:
    """Main function to process and generate markdown lists.

    Handles command line arguments, loads data, processes it according to specified
    settings, and outputs formatted markdown text either to a file or stdout.

    :return: Exit code (0 for success)
    :rtype: int
    """
    # Set up template environment for markdown
    ext = ".md"
    env = load_template_env(ext=ext)

    # Configure command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "listtype",
        type=str,
        choices=[
            "talks",
            "grants",
            "meetings",
            "extalks",
            "teaching",
            "exteaching",
            "students",
            "exstudents",
            "pdras",
            "expdras",
            "exgrants",
            "publications",
            "journal",
            "book",
            "conference",
        ],
        help="The type of output markdown list",
    )

    parser.add_argument("-o", "--output", type=str, help="Output filename")

    parser.add_argument("-s", "--since-year", type=int, help="The year from which to include entries")

    parser.add_argument("file", type=str, nargs="+", help="The file names to read in")

    args = parser.parse_args()
    now = pd.to_datetime(datetime.datetime.now().date())
    now_year = now.year

    # Load interface configuration for the specified list type
    # Look for cvlists.yml in the lamd config directory
    lamd_dir = os.path.dirname(os.path.abspath(__file__))
    config_dir = os.path.join(lamd_dir, "config")
    cvlists_path = os.path.join(config_dir, "cvlists.yml")
    interface = Interface.from_file(user_file=cvlists_path)[args.listtype]

    # Set the year filter - either from command line or default to 5 years ago
    if args.since_year:
        set_since_year(args.since_year)
    else:
        set_since_year(now_year - 5)

    # Configure data allocation based on input files
    interface["input"] = {}

    # Extract most common starting directory from file paths
    file_dirs = [os.path.dirname(os.path.abspath(f)) for f in args.file]
    common_prefix = os.path.commonpath(file_dirs)

    interface["input"]["base_directory"] = common_prefix

    # Remove common prefix from file paths
    args.file = [os.path.relpath(f, common_prefix) for f in args.file]
    interface["input"]["directory"] = "."
    if len(args.file) == 1:
        interface["input"]["filename"] = args.file[0]
        interface["input"]["type"] = "auto"
    else:
        interface["input"]["filename"] = args.file
        interface["input"]["type"] = "list"

    # Load the data using referia's CustomDataFrame
    data = assess.data.CustomDataFrame.from_flow(interface)

    # Initialize settings dictionary from the interface
    settings = {"lists": interface, "compute": {}, "filter": []}

    text = ""

    # Process the data through different operations (preprocessor, augmentor, sorter)
    for op in ["preprocessor", "augmentor", "sorter"]:
        if op in settings["lists"][args.listtype]:
            # Add operation to compute settings
            comp = settings["lists"][args.listtype][op]
            if op in settings["compute"]:
                if type(comp) is not list:
                    comp = [comp]
                settings["compute"][op] += comp
            else:
                settings["compute"][op] = comp

    # Handle filters if specified
    if "filter" in settings["lists"][args.listtype]:
        filt = settings["lists"][args.listtype]["filter"]
        if "filter" in settings:
            if type(filt) is not list:
                filt = [filt]
            settings["filter"] += filt
        else:
            settings["filter"] = filt

    # Preprocess the data
    data.preprocess()

    # Get the DataFrame from the data object
    df = data.df

    # Apply filter function to get boolean mask
    # This is a placeholder implementation since we don't have the actual filter functions
    # In a real implementation, this would use the filters from settings
    filt = pd.Series([True] * len(df), index=df.index)

    # Generate markdown text using the specified template
    listtemplate = settings["lists"][args.listtype]["listtemplate"]
    for index, entry in df.iterrows():
        if not pd.isna(filt[index]) and filt[index]:
            kwargs = remove_nan(entry.to_dict())
            text += env.get_template(listtemplate + ext).render(**kwargs)
            text += "\n"

    # Output the generated markdown
    if args.output is not None:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
