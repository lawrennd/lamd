#!/usr/bin/env python3
"""
Flags Module - Extracts flags and options for pandoc from YAML frontmatter.

This module generates command-line flags for Pandoc based on the YAML frontmatter
in markdown files and configuration files. It supports multiple output formats and
produces the appropriate flags for each.

The flags module is used by other tools in the lamd package to generate
consistent command-line options when converting markdown files to various formats.

Usage:
    flags OUTPUT BASE

Where:
    OUTPUT: The type of output (pp, post, docx, pptx, prefix, reveal, cv)
    BASE: The base part of the filename (without extension)

Example:
    flags reveal myfile
    flags post lecture-notes
    flags docx syllabus
"""

import argparse
import os
import sys
import lynguine.util.talk as nt
import lynguine.util.yaml as ny


def main() -> int:
    """
    Process markdown files and extract appropriate pandoc flags based on YAML frontmatter.

    This function:
    1. Parses command-line arguments for output type and base filename
    2. Reads YAML frontmatter from the specified markdown file
    3. Extracts relevant fields from the frontmatter or config files
    4. Generates a prefix for output filenames based on layout and metadata
    5. Outputs appropriate pandoc flags based on the requested output format

    Output formats:
        prefix: Returns the file prefix only, based on date and layout
        post: Generates metadata flags for Jekyll post conversion
        docx: Generates flags for Word document conversion
        pptx: Generates flags for PowerPoint presentation conversion
        reveal: Generates flags for reveal.js presentation
        pp: Generates flags for the preprocessor
        cv: Placeholder for CV-specific flags (not fully implemented)

    Returns:
        int: Exit code (0 for success)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output",
        type=str,
        choices=["pp", "post", "docx", "pptx", "prefix", "reveal", "cv"],
        help="The type of output file (post is for a jekyll post, docx for word, pptx for powerpoint)",
    )
    parser.add_argument("base", type=str, help="The base part of the filename")

    user_file = ["_lamd.yml", "_config.yml"]

    args = parser.parse_args()

    filename = args.base + ".md"

    fields = ny.header_fields(filename)

    try:
        date = ny.header_field("date", fields, user_file).strftime("%Y-%m-%d")
    except ny.FileFormatError:
        date = None

    try:
        week = int(ny.header_field("week", fields, user_file))
        weekarg = f" --metadata week={week}"
    except ny.FileFormatError:
        week = None
        weekarg = ""

    try:
        topic = int(ny.header_field("topic", fields, user_file))
        topicarg = f" --metadata topic={topic}"
    except ny.FileFormatError:
        topic = None
        topicarg = ""

    try:
        session = int(ny.header_field("session", fields, user_file))
        sessionarg = f" --metadata session={session}"
    except ny.FileFormatError:
        session = None
        sessionarg = ""

    try:
        practical = int(ny.header_field("practical", fields, user_file))
        practicalarg = f" --metadata practical={practical}"
    except ny.FileFormatError:
        practical = None
        practicalarg = ""

    try:
        background = int(ny.header_field("background", fields, user_file))
        backgroundarg = f" --metadata background={background}"
    except ny.FileFormatError:
        background = None
        backgroundarg = ""

    try:
        revealjs_url = ny.header_field("revealjs_url", fields, user_file)
    except ny.FileFormatError:
        revealjs_url = "https://unpkg.com/reveal.js@3.9.2"
    revealjs_urlarg = f" --variable revealjs-url={revealjs_url}"

    try:
        talktheme = ny.header_field("talktheme", fields, user_file)
    except ny.FileFormatError:
        talktheme = "black"
    talkthemearg = f" --variable theme={talktheme}"

    try:
        talkcss = ny.header_field("talkcss", fields, user_file)
    except ny.FileFormatError:
        talkcss = "https://inverseprobability.com/assets/css/talks.css"
    talkcssarg = f" --css {talkcss}"

    try:
        layout = ny.header_field("layout", fields, user_file)
    except ny.FileFormatError:
        layout = "talk"

    prefix = ""
    if layout == "lecture":
        prefix = ""
        if week is not None and isinstance(week, int) and week > 0:
            prefix += "{0:02}".format(week)
        if session is not None and isinstance(session, int) and session > 0:
            if week is not None and isinstance(week, int) and week > 0:
                prefix += "-"
            prefix += "{0:02}".format(session)
        if len(prefix) > 0:
            prefix += "-"
    elif layout == "topic":
        prefix = ""
        if topic is not None and isinstance(topic, int) and topic > 0:
            prefix += "{0:02}".format(topic)
        if len(prefix) > 0:
            prefix += "-"
    elif layout == "background":
        prefix = ""
        if week is not None and week > 0:
            prefix += "{0:02}".format(week)
            prefix += "-"
        if session is not None and session > 0:
            prefix += "{0:02}".format(session)
            prefix += "-"
        if background is not None and background > 0:
            prefix += "{0:02}".format(background)
            prefix += "-"
    elif layout == "test":
        prefix = "XXXX-XX-XX"
        prefix += "-"
    elif layout == "talk":
        if date is not None:
            prefix = date
            prefix += "-"
        else:
            prefix = ""
    elif layout == "casestudy":
        if date is not None:
            prefix = date
            prefix += "-"
        else:
            prefix = ""
    elif layout == "notebook":
        prefix = ""
    elif layout == "practical":
        prefix = ""
        if week is not None and week > 0:
            prefix += "{0:02}".format(week)
            prefix += "-"
        if session is not None and session > 0:
            prefix += "{0:02}".format(session)
            prefix += "-"
        if practical is not None and practical > 0:
            prefix += "{0:02}".format(practical)
            prefix += "-"
    elif layout == "example":
        prefix = ""
    elif layout == "software":
        prefix = ""
    elif layout == "dataset":
        prefix = ""
    elif layout == "cv":
        if date is not None:
            prefix = date
            prefix += "-"
        else:
            prefix = ""

    out = prefix + args.base

    lines = ""
    if args.output == "prefix":
        print(prefix)

    elif args.output == "post":
        if date is not None:
            lines += """--metadata date={date} """
        for ext in ["docx", "pptx"]:
            if ny.header_field(ext, fields, user_file):
                lines += """ --metadata {ext}={{out}}.{ext}""".format(ext=ext)
        if ny.header_field("reveal", fields, user_file):
            lines += """ --metadata reveal={out}.slides.html"""
        if ny.header_field("ipynb", fields, user_file):
            lines += """ --metadata ipynb={out}.ipynb"""
        if ny.header_field("slidesipynb", fields, user_file):
            lines += """ --metadata slidesipynb={out}.slides.ipynb"""
        if ny.header_field("notespdf", fields, user_file):
            lines += """ --metadata notespdf={out}.notes.pdf"""
        if ny.header_field("pdf", fields, user_file):
            lines += """ --metadata pdf={out}.pdf"""

        lines += weekarg + topicarg + sessionarg + practicalarg + f" --metadata layout={layout}"
        if ny.header_field("ghub", fields, user_file=["_lamd.yml", "_config.yml"]):
            ghub = ny.header_field("ghub", fields, user_file)[0]
            lines += """ --metadata edit_url={local_edit}""".format(
                local_edit="https://github.com/{ghub_organization}/{ghub_repository}/edit/{ghub_branch}/{ghub_dir}/{base}.md".format(
                    base=args.base,
                    ghub_organization=ghub["organization"],
                    ghub_repository=ghub["repository"],
                    ghub_branch=ghub["branch"],
                    ghub_dir=ghub["directory"],
                )
            )
        print(lines.format(out=out, date=date))

    elif args.output == "docx":
        lines += "--reference-doc " + ny.header_field("dotx", fields, user_file)
        print(lines)

    elif args.output == "pptx":
        lines += "--reference-doc " + ny.header_field("potx", fields, user_file)
        print(lines)

    elif args.output == "reveal":
        lines += "--slide-level 2 " + revealjs_urlarg + talkthemearg + talkcssarg
        print(lines)

    elif args.output == "pp":
        lines = "--include-path ./.."
        # Flags for the preprocessor.
        try:
            if ny.header_field("assignment", fields, user_file):
                lines += """ --assignment"""
        except ny.FileFormatError:
            pass

        print(lines)

    elif args.output == "cv":
        # For CV output, we don't need to print any specific flags
        # This is a placeholder for future implementation
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
