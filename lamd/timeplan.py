"""Compile within-lecture time allocations (CIP-001B).

GPP macros emit HTML-comment markers; after includes expand through gpp,
``expand_timeplan`` collects them and replaces each ``<!--lamd-timeplan-->``
with a markdown table. Live ``\\classtimer`` chrome is unchanged.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import TextIO

# Capture groups must not cross HTML-comment terminators (avoid greedy [^|]*).
SESSIONSTART_RE = re.compile(r"<!--lamd-sessionstart\|([^|>]*)-->")
SESSIONLENGTH_RE = re.compile(r"<!--lamd-sessionlength\|([^|>]*)-->")
BLOCKTIME_RE = re.compile(r"<!--lamd-blocktime\|([^|>]*)\|([^|]*)\|([^|>]*)-->")
TIMEPLAN_RE = re.compile(r"<!--lamd-timeplan-->")
ANY_MARKER_RE = re.compile(r"<!--lamd-(?:sessionstart|sessionlength|blocktime|timeplan)(?:\|[^>]*)?-->")


@dataclass(frozen=True)
class BlockAllocation:
    """One ``\\blocktime`` row after marker expansion."""

    minutes: int
    label: str
    flag: str = ""


@dataclass(frozen=True)
class TimePlan:
    """Parsed session metadata and ordered block allocations."""

    session_start: str | None
    session_length: int | None
    blocks: tuple[BlockAllocation, ...]


def add_minutes(clock: str, minutes: int) -> str:
    """Return ``HH:MM`` after adding ``minutes`` to ``clock``."""
    parts = clock.strip().split(":")
    if len(parts) != 2:
        raise ValueError(f"invalid clock: {clock!r}")
    hours, mins = int(parts[0]), int(parts[1])
    total = hours * 60 + mins + minutes
    # Allow past midnight without wrapping for long evening sessions.
    return f"{total // 60:02d}:{total % 60:02d}"


def parse_timeplan_markers(content: str) -> TimePlan:
    """Collect session and block markers in document order."""
    starts = SESSIONSTART_RE.findall(content)
    lengths = SESSIONLENGTH_RE.findall(content)
    session_start = starts[0].strip() if starts else None
    session_length: int | None = None
    if lengths:
        try:
            session_length = int(lengths[0].strip())
        except ValueError:
            session_length = None

    blocks: list[BlockAllocation] = []
    for mins_raw, label, flag in BLOCKTIME_RE.findall(content):
        try:
            minutes = int(mins_raw.strip())
        except ValueError:
            continue
        blocks.append(
            BlockAllocation(
                minutes=minutes,
                label=label.strip(),
                flag=flag.strip(),
            )
        )
    return TimePlan(
        session_start=session_start or None,
        session_length=session_length,
        blocks=tuple(blocks),
    )


def format_timeplan_table(plan: TimePlan) -> str:
    """Render a markdown Clock|Mins|Block (or Mins|Block) table."""
    if not plan.blocks:
        return "_No time allocations declared._"

    use_clock = bool(plan.session_start)
    lines: list[str] = []
    if use_clock:
        lines.append("| Clock | Mins | Block |")
        lines.append("|------:|-----:|-------|")
    else:
        lines.append("| Mins | Block |")
        lines.append("|-----:|-------|")

    cursor = plan.session_start
    for block in plan.blocks:
        label = block.label or "_(untitled)_"
        if use_clock and cursor is not None:
            end = add_minutes(cursor, block.minutes)
            lines.append(f"| {cursor}–{end} | {block.minutes} | {label} |")
            cursor = end
        else:
            lines.append(f"| {block.minutes} | {label} |")
    return "\n".join(lines)


def warn_timeplan(plan: TimePlan, stream: TextIO = sys.stderr) -> None:
    """Emit advisory messages for overrun and missing labels."""
    total = sum(b.minutes for b in plan.blocks)
    if plan.session_length is not None and total > plan.session_length:
        excess = total - plan.session_length
        print(
            f"lamd timeplan: allocations sum to {total} min, "
            f"exceeding session length {plan.session_length} by {excess} min",
            file=stream,
        )
    for i, block in enumerate(plan.blocks, start=1):
        if not block.label:
            print(
                f"lamd timeplan: block {i} ({block.minutes} min) is missing a label",
                file=stream,
            )


def expand_timeplan(
    content: str,
    *,
    warn: bool = True,
    warn_stream: TextIO = sys.stderr,
) -> str:
    """Replace timeplan markers with a compiled table; strip allocation markers.

    If the content has no CIP-001B markers, return it unchanged.
    """
    if "<!--lamd-" not in content:
        return content
    if not ANY_MARKER_RE.search(content):
        return content

    plan = parse_timeplan_markers(content)
    if warn and plan.blocks:
        warn_timeplan(plan, warn_stream)

    table = format_timeplan_table(plan) if plan.blocks else ""

    def _replace_timeplan(_match: re.Match[str]) -> str:
        return table

    if TIMEPLAN_RE.search(content):
        content = TIMEPLAN_RE.sub(_replace_timeplan, content)

    # Drop remaining allocation markers so they never leak into HTML/PDF.
    content = SESSIONSTART_RE.sub("", content)
    content = SESSIONLENGTH_RE.sub("", content)
    content = BLOCKTIME_RE.sub("", content)
    content = TIMEPLAN_RE.sub("", content)
    return content
