#!/usr/bin/env python3

import argparse
import datetime
import os
import sys
from typing import Any, Optional

import pandas as pd
from lynguine.config.interface import Interface
from lynguine.util.liquid import load_template_env
from lynguine.util.misc import remove_nan
from referia import assess

from lamd.util import get_since_year, set_since_year

# Server mode support (optional dependency)
try:
    from lynguine.client import ServerClient

    SERVER_MODE_AVAILABLE = True
except ImportError:
    SERVER_MODE_AVAILABLE = False
    ServerClient = None

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


def cvlists_config_dir() -> str:
    """Directory that contains the packaged ``cvlists.yml``."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")


def load_cvlists_interface() -> Interface:
    """Load packaged list settings even when cwd is a CV directory.

    lynguine confines ``Interface.from_file`` to ``allowed_roots`` (cwd by
    default). An absolute ``user_file`` under the lamd package is therefore
    rejected unless that package config directory is an allowed root.
    """
    config_dir = cvlists_config_dir()
    return Interface.from_file(
        user_file="cvlists.yml",
        directory=config_dir,
        allowed_roots=[config_dir],
    )


def _year_int(value: object) -> Optional[int]:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if pd.isna(value):
        return None
    year = int(value)
    if 1900 <= year <= 2100:
        return year
    return None


def _is_year_number(value: object) -> bool:
    return _year_int(value) is not None


def value_year(value: object) -> Optional[int]:
    """Calendar year from an int year, datetime, or parseable date string."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    year = _year_int(value)
    if year is not None:
        return year
    ts = pd.to_datetime(value, errors="coerce")
    if pd.isna(ts):
        return None
    return int(ts.year)


def value_date(value: object, *, end: bool = False) -> pd.Timestamp:
    """Timestamp for current/former comparisons. Bare years become Jan 1 or Dec 31."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return pd.NaT
    year = _year_int(value)
    if year is not None:
        if end:
            return pd.Timestamp(year=year, month=12, day=31)
        return pd.Timestamp(year=year, month=1, day=1)
    ts = pd.to_datetime(value, errors="coerce")
    return ts if not pd.isna(ts) else pd.NaT


def row_year(row: pd.Series) -> Optional[int]:
    for column in ("year", "published", "date", "start"):
        if column in row.index:
            year = value_year(row[column])
            if year is not None:
                return year
    return None


def compute_section(config: object) -> dict[str, Any]:
    """Return the compute mapping from a list config.

    ``CustomDataFrame.from_flow`` rewrites ``compute`` from a dict into a
    one-element list. Unwrap that so filters and sorters remain reachable.
    """
    compute = config.get("compute") if isinstance(config, dict) else None
    if isinstance(compute, dict):
        return compute
    if isinstance(compute, list):
        merged: dict[str, Any] = {}
        for item in compute:
            if isinstance(item, dict):
                merged.update(item)
        return merged
    return {}


def _truthy_flag(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if pd.isna(value):
            return False
        return bool(value)
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _as_filter_list(filt: object) -> list[dict[str, Any]]:
    if filt is None:
        return []
    if isinstance(filt, dict):
        return [filt]
    if isinstance(filt, list):
        return [item for item in filt if isinstance(item, dict)]
    return []


def apply_named_filter(df: pd.DataFrame, spec: dict[str, Any], since_year: Optional[int], today: pd.Timestamp) -> pd.Series:
    """Boolean mask for one cvlists.yml filter spec."""
    function = spec.get("function")
    args = spec.get("args") or {}
    true = pd.Series(True, index=df.index)
    if df.empty:
        return true
    if function == "recent":
        column = args.get("column", "year")
        years = df.apply(lambda row: value_year(row[column]) if column in row.index else row_year(row), axis=1)
        if since_year is None:
            return true
        known = years.notna()
        return ~known | (years >= since_year)
    if function == "current":
        current_col = args.get("current")
        if current_col and current_col in df.columns:
            return df[current_col].map(_truthy_flag)
        end_col = args.get("end", "end")
        if end_col not in df.columns:
            return true
        ends = df[end_col].map(lambda value: value_date(value, end=True))
        return ends.isna() | (ends >= today)
    if function == "former":
        current_col = args.get("current")
        if current_col and current_col in df.columns:
            return ~df[current_col].map(_truthy_flag)
        end_col = args.get("end", "end")
        if end_col not in df.columns:
            return pd.Series(False, index=df.index)
        ends = df[end_col].map(lambda value: value_date(value, end=True))
        return ends.notna() & (ends < today)
    if function == "columnis":
        column, expected = args.get("column"), args.get("value")
        if column not in df.columns:
            return pd.Series(False, index=df.index)
        return df[column] == expected
    if function == "columncontains":
        column, expected = args.get("column"), args.get("value")
        if column not in df.columns:
            return pd.Series(False, index=df.index)

        def contains(cell: object) -> bool:
            if expected is None:
                return False
            if isinstance(cell, (list, tuple)):
                return expected in cell
            if cell is None or (isinstance(cell, float) and pd.isna(cell)):
                return False
            return str(expected) in str(cell)

        return df[column].map(contains)
    if function == "onbool":
        column = args.get("column")
        invert = bool(args.get("invert", False))
        if column not in df.columns:
            return pd.Series(False, index=df.index)
        mask = df[column].fillna(False).astype(bool)
        return ~mask if invert else mask
    return true


def apply_list_filters(
    df: pd.DataFrame,
    filters: object,
    since_year: Optional[int],
    today: Optional[pd.Timestamp] = None,
    *,
    apply_since: bool = False,
) -> pd.Series:
    """AND together cvlists filters. Optionally also apply a since-year cut."""
    if today is None:
        today = pd.Timestamp(datetime.datetime.now().date())
    mask = pd.Series(True, index=df.index)
    specs = _as_filter_list(filters)
    for spec in specs:
        mask = mask & apply_named_filter(df, spec, since_year, today)
    if apply_since or any(spec.get("function") == "recent" for spec in specs):
        if since_year is not None:
            years = df.apply(row_year, axis=1)
            known = years.notna()
            mask = mask & (~known | (years >= since_year))
    return mask


def coerce_yearish_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Turn bare integer years on date columns into timestamps for Liquid date filters."""
    if df.empty:
        return df
    out = df.copy()
    for column, end in (("start", False), ("end", True), ("date", False), ("published", False)):
        if column not in out.columns:
            continue
        out[column] = out[column].map(lambda value, is_end=end: value_date(value, end=is_end))
    return out


def sort_list_frame(df: pd.DataFrame, sorter: object) -> pd.DataFrame:
    if not isinstance(sorter, dict):
        return df
    args = sorter.get("args") or {}
    by = args.get("by", sorter.get("by"))
    if not by:
        return df
    if not isinstance(by, list):
        by = [by]
    columns = [column for column in by if column in df.columns]
    if not columns:
        return df
    descending = sorter.get("function") == "descending"
    return df.sort_values(by=columns, ascending=not descending, na_position="last")


def main() -> int:
    """Main function to process and generate markdown lists.

    Handles command line arguments, loads data, processes it according to specified
    settings, and outputs formatted markdown text either to a file or stdout.

    :return: Exit code (0 for success)
    :rtype: int
    """
    # Set up template environment for markdown
    # Use lamd's templates directory, not lynguine's default
    ext = ".md"
    lamd_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(lamd_dir, "templates")
    env = load_template_env(ext=ext, template_dir=template_dir)

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

    # Server mode options
    parser.add_argument(
        "--use-server",
        action="store_true",
        help="Use lynguine server mode for faster repeated access (requires lynguine server mode)",
    )

    parser.add_argument("--no-server", action="store_true", help="Force direct mode even if LAMD_USE_SERVER is set")

    parser.add_argument("file", type=str, nargs="+", help="The file names to read in")

    args = parser.parse_args()

    # Determine if we should use server mode
    use_server = args.use_server or (os.environ.get("LAMD_USE_SERVER", "0") == "1")
    if args.no_server:
        use_server = False

    # Check if server mode is available
    if use_server and not SERVER_MODE_AVAILABLE:
        sys.stderr.write("Warning: Server mode requested but lynguine.client not available. Falling back to direct mode.\n")
        use_server = False
    now = pd.to_datetime(datetime.datetime.now().date())
    now_year = now.year

    interface = load_cvlists_interface()[args.listtype]

    # Set the year filter - either from command line or default to 5 years ago.
    # The default only applies when a cvlists filter is `recent`; current/former
    # lists must not be year-cut just because we stored a default.
    explicit_since = args.since_year is not None
    if explicit_since:
        set_since_year(args.since_year)
    else:
        set_since_year(now_year - 5)

    # Configure data allocation based on input files
    interface["input"] = {}

    # Extract most common starting directory from file paths
    file_dirs = [os.path.dirname(os.path.abspath(f)) for f in args.file]
    common_prefix = os.path.commonpath(file_dirs)

    interface["input"]["base_directory"] = common_prefix
    interface["input"]["index"] = "filename"  # Use filename as unique identifier

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
    if use_server:
        # Server mode integration for mdlist is deferred to Phase 3
        # Complexity: CustomDataFrame.from_flow() integrates tightly with compute operations
        # (preprocessors, augmentors, sorters) and mdlist's current architecture expects
        # local DataFrame processing for template rendering.
        #
        # For Phase 2 MVP, focus is on mdfield (38 calls in CV builds).
        # mdlist server integration will be addressed in Phase 3 with proper architecture.
        sys.stderr.write("Note: Server mode for mdlist deferred to Phase 3. Using direct mode.\n")
        use_server = False

    # Snapshot compute before from_flow, which may wrap the mapping in a list.
    compute = compute_section(interface)
    listtemplate = interface["listtemplate"]

    # Load data (direct mode for now)
    data = assess.data.CustomDataFrame.from_flow(interface)
    compute = compute_section(interface) or compute

    settings = {
        "lists": interface,
        "compute": compute,
        "filter": _as_filter_list(compute.get("filter")),
    }

    text = ""

    try:
        data.preprocess()
    except TypeError as err:
        sys.stderr.write(f"Warning: skipping lynguine preprocess ({err}). Applying pandas list filters instead.\n")

    df = data.to_pandas()
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame()

    df = coerce_yearish_dates(df)
    df = sort_list_frame(df, settings["compute"].get("sorter"))
    filt = apply_list_filters(
        df,
        settings.get("filter"),
        get_since_year(),
        now,
        apply_since=explicit_since,
    )

    skip_empty_title = listtemplate == "listtalk"
    keep = filt.reindex(df.index).fillna(False).astype(bool)
    for _, entry in df.loc[keep].iterrows():
        kwargs = remove_nan(entry.to_dict())
        if skip_empty_title and not kwargs.get("title"):
            continue
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
