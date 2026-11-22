"""Unit tests for CIP-001B time-plan collection and table emission."""

from __future__ import annotations

import io

from lamd.timeplan import (
    add_minutes,
    expand_timeplan,
    format_timeplan_table,
    parse_timeplan_markers,
    warn_timeplan,
)


def test_add_minutes() -> None:
    assert add_minutes("10:05", 10) == "10:15"
    assert add_minutes("10:50", 20) == "11:10"


def test_parse_markers_in_order() -> None:
    content = "\n".join(
        [
            "<!--lamd-sessionstart|10:05-->",
            "<!--lamd-sessionlength|110-->",
            "<!--lamd-timeplan-->",
            "<!--lamd-blocktime|10|Quiz 3|-->",
            "from include:",
            "<!--lamd-blocktime|20|Exponential family|-->",
            "<!--lamd-blocktime|10|Break|timer-->",
        ]
    )
    plan = parse_timeplan_markers(content)
    assert plan.session_start == "10:05"
    assert plan.session_length == 110
    assert [b.minutes for b in plan.blocks] == [10, 20, 10]
    assert [b.label for b in plan.blocks] == ["Quiz 3", "Exponential family", "Break"]
    assert plan.blocks[2].flag == "timer"


def test_format_table_with_clocks() -> None:
    plan = parse_timeplan_markers(
        "<!--lamd-sessionstart|10:05-->" "<!--lamd-blocktime|10|Quiz 3|-->" "<!--lamd-blocktime|20|Talk|-->"
    )
    table = format_timeplan_table(plan)
    assert "| Clock | Mins | Block |" in table
    assert "| 10:05–10:15 | 10 | Quiz 3 |" in table
    assert "| 10:15–10:35 | 20 | Talk |" in table


def test_format_table_without_clocks() -> None:
    plan = parse_timeplan_markers("<!--lamd-blocktime|15|Shannon|-->")
    table = format_timeplan_table(plan)
    assert "| Mins | Block |" in table
    assert "Clock" not in table
    assert "| 15 | Shannon |" in table


def test_expand_replaces_timeplan_and_strips_markers() -> None:
    content = "\n".join(
        [
            "Intro",
            "<!--lamd-sessionstart|10:05-->",
            "<!--lamd-sessionlength|110-->",
            "<!--lamd-timeplan-->",
            "Body",
            "<!--lamd-blocktime|10|Quiz 3|-->",
            "<!--lamd-blocktime|20|Talk|-->",
            "End",
        ]
    )
    out = expand_timeplan(content, warn=False)
    assert "<!--lamd-" not in out
    assert "| 10:05–10:15 | 10 | Quiz 3 |" in out
    assert "| 10:15–10:35 | 20 | Talk |" in out
    assert "Intro" in out and "Body" in out and "End" in out
    assert "data-background-iframe" not in out


def test_expand_unchanged_without_markers() -> None:
    src = "# Hello\n\nNo plan here.\n"
    assert expand_timeplan(src) is src or expand_timeplan(src) == src


def test_overrun_and_missing_label_warnings() -> None:
    plan = parse_timeplan_markers("<!--lamd-sessionlength|30-->" "<!--lamd-blocktime|20|A|-->" "<!--lamd-blocktime|20||-->")
    buf = io.StringIO()
    warn_timeplan(plan, buf)
    text = buf.getvalue()
    assert "exceeding session length 30" in text
    assert "missing a label" in text


def test_expand_emits_overrun_warning() -> None:
    content = "<!--lamd-sessionlength|15-->" "<!--lamd-timeplan-->" "<!--lamd-blocktime|10|A|-->" "<!--lamd-blocktime|10|B|-->"
    buf = io.StringIO()
    expand_timeplan(content, warn=True, warn_stream=buf)
    assert "exceeding session length 15" in buf.getvalue()
