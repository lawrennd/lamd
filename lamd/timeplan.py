"""Compile within-lecture time allocations (CIP-001B).

GPP macros emit HTML-comment markers; after includes expand through gpp,
``expand_timeplan`` collects them and replaces each ``<!--lamd-timeplan-->``
with a markdown table. Optional ``timer`` flags emit CIP-0012
``\\classtimertitled`` chrome (slides HTML iframe or notes placeholder).
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from typing import Literal, TextIO

# Capture groups must not cross HTML-comment terminators (avoid greedy [^|]*).
SESSIONSTART_RE = re.compile(r"<!--lamd-sessionstart\|([^|>]*)-->")
SESSIONLENGTH_RE = re.compile(r"<!--lamd-sessionlength\|([^|>]*)-->")
BLOCKTIME_RE = re.compile(r"<!--lamd-blocktime\|([^|>]*)\|([^|]*)\|([^|>]*)-->")
TIMEPLAN_RE = re.compile(r"<!--lamd-timeplan-->")
ANY_MARKER_RE = re.compile(r"<!--lamd-(?:sessionstart|sessionlength|blocktime|timeplan)(?:\|[^>]*)?-->")

TimerMode = Literal["none", "notes", "slides-html"]


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


def format_classtimertitled(
    clock: str,
    label: str,
    *,
    mode: TimerMode,
    scripts_dir: str = "scripts",
) -> str:
    """Emit CIP-0012 ``\\classtimertitled`` chrome for a derived wall clock."""
    if mode == "slides-html":
        return (
            f'<section data-background-iframe="{scripts_dir}/timer/index.html'
            f'?duration={clock}&title={label}" data-background-interactive></section>'
        )
    if mode == "notes":
        return f"*Class test timer ({label}): {clock}*"
    return ""


def is_timer_flag(flag: str) -> bool:
    """Return True when the optional third ``\\blocktime`` arg requests a live timer."""
    return flag.strip().lower() == "timer"


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
        if is_timer_flag(block.flag) and not plan.session_start:
            label = block.label or f"block {i}"
            print(
                f"lamd timeplan: {label!r} has timer flag but no \\sessionstart; "
                "cannot derive wall clock for \\classtimertitled — skipping timer",
                file=stream,
            )


def expand_timeplan(
    content: str,
    *,
    warn: bool = True,
    warn_stream: TextIO = sys.stderr,
    timer_mode: TimerMode = "none",
    scripts_dir: str = "scripts",
) -> str:
    """Replace timeplan markers with a compiled table; strip allocation markers.

    When ``timer_mode`` is ``notes`` or ``slides-html``, ``\\blocktime`` rows
    flagged ``timer`` expand to CIP-0012 classtimertitled chrome at the
    derived block start clock (requires ``\\sessionstart``).

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

    # Replace block markers in document order so timer chrome uses cumulative clocks.
    cursor = plan.session_start
    pieces: list[str] = []
    last = 0
    for match in BLOCKTIME_RE.finditer(content):
        pieces.append(content[last : match.start()])
        mins_raw, label_raw, flag_raw = match.groups()
        try:
            minutes = int(mins_raw.strip())
        except ValueError:
            pieces.append("")
            last = match.end()
            continue
        label = label_raw.strip()
        flag = flag_raw.strip()
        start_clock = cursor
        if cursor is not None:
            cursor = add_minutes(cursor, minutes)

        replacement = ""
        if is_timer_flag(flag) and timer_mode != "none":
            if start_clock is not None:
                replacement = format_classtimertitled(
                    start_clock,
                    label or "Timer",
                    mode=timer_mode,
                    scripts_dir=scripts_dir,
                )
            # else: warn_timeplan already advised; emit nothing
        pieces.append(replacement)
        last = match.end()
    pieces.append(content[last:])
    content = "".join(pieces)

    # Drop remaining allocation markers so they never leak into HTML/PDF.
    content = SESSIONSTART_RE.sub("", content)
    content = SESSIONLENGTH_RE.sub("", content)
    content = TIMEPLAN_RE.sub("", content)
    return content
