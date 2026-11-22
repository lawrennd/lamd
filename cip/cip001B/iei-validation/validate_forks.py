#!/usr/bin/env python3
"""Validate CIP-001B IEI forks: compiled tables match original clocks."""

from __future__ import annotations

import io
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MACROS = ROOT / "lamd" / "macros"
HERE = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT))
from lamd.timeplan import expand_timeplan  # noqa: E402

CASES = [
    {
        "file": "limits-on-intelligence.fork.md",
        "rows": [
            "| 10:05–10:15 | 10 | Quiz 4 (paper); collect Worksheet 4 |",
            "| 10:15–10:40 | 25 | Short limits synthesis / W4 themes |",
            "| 10:40–10:50 | 10 | Break |",
            "| 10:50–11:35 | 45 | Protected: no-barber",
            "| 11:35–11:55 | 20 | Course close; Week 1 answer |",
        ],
        "timer_title": "Quiz 4 (paper); collect Worksheet 4",
        "timer_clock": "10:05",
        "iframe_count": 1,
    },
    {
        "file": "good-regulator-goals-channels.fork.md",
        "rows": [
            "| 10:05–10:25 | 20 | Unmarked Worksheet 3 review; flag W4 due Week 8 start |",
            "| 10:25–10:50 | 25 | Good Regulator overview:",
            "| 10:50–11:00 | 10 | Break |",
            "| 11:00–11:35 | 35 | Goal measure / Radon--Nikodym;",
            "| 11:35–11:50 | 15 | Shannon $R\\le C$; DPI statement and moral |",
            "| 11:50–11:55 | 5 | Define-this-week; W4 reminder; Week 8 preview |",
        ],
        "timer_title": None,
        "iframe_count": 0,
    },
    {
        "file": "exponential-family-fisher-overviews.fork.md",
        "rows": [
            "| 10:05–10:32 | 27 | Quiz 3 (paper); collect Worksheet 3; release Worksheet 4 |",
            "| 10:32–10:34 | 2 | Maxwell-speed / high-d ring aside |",
            "| 10:34–11:00 | 26 | Exp family:",
            "| 11:00–11:05 | 5 | MaxEnt property Q\\&A; break called |",
            "| 11:05–11:15 | 10 | Break |",
            "| 11:15–11:42 | 27 | Base measure",
            "| 11:42–11:56 | 14 | $H=\\psi-\\theta\\cdot\\eta$;",
            "| 11:56–11:58 | 2 | GRT pointer for Worksheet 4 only |",
        ],
        "timer_title": "Quiz 3 (paper); collect Worksheet 3; release Worksheet 4",
        "timer_clock": "10:05",
        "iframe_count": 1,
        # as-delivered sum is 113 (>110): expect advisory
        "expect_overrun": True,
    },
]


def gpp_notes(body: str) -> str:
    chunks = [
        "\\include{talk-macros-null.gpp}",
        "\\include{talk-macros-notes.gpp}",
        body,
    ]
    result = subprocess.run(
        ["gpp", "-T", f"-I{MACROS}", "-DNOTES=1", "-DscriptsDir=SCRIPTS"],
        input="\n".join(chunks),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gpp failed: {result.stderr}")
    return result.stdout


def gpp_slides(body: str) -> str:
    chunks = [
        "\\include{talk-macros-null.gpp}",
        "\\include{talk-macros-html.gpp}",
        "\\include{talk-macros-slides.gpp}",
        "\\include{talk-macros-slides-html.gpp}",
        body,
    ]
    result = subprocess.run(
        [
            "gpp",
            "-T",
            f"-I{MACROS}",
            "-DSLIDES=1",
            "-DHTML=1",
            "-DscriptsDir=SCRIPTS",
        ],
        input="\n".join(chunks),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"gpp failed: {result.stderr}")
    return result.stdout


def main() -> int:
    os.chdir(ROOT)
    failures = 0
    for case in CASES:
        path = HERE / case["file"]
        body = path.read_text(encoding="utf-8")
        # Drop YAML frontmatter for gpp (mdpp would handle it).
        if body.startswith("---"):
            end = body.find("\n---", 3)
            body = body[end + 4 :] if end != -1 else body

        print(f"== {case['file']} ==")
        marked = gpp_notes(body)
        warn_buf = io.StringIO()
        notes_out = expand_timeplan(marked, warn=True, warn_stream=warn_buf, timer_mode="notes")
        warn_text = warn_buf.getvalue()

        for row in case["rows"]:
            if row not in notes_out:
                print(f"  FAIL missing row: {row}")
                failures += 1
            else:
                print(f"  ok row: {row[:60]}…")

        if case.get("expect_overrun"):
            if "exceeding session length" not in warn_text:
                print("  FAIL expected overrun warning")
                failures += 1
            else:
                print(f"  ok overrun warning: {warn_text.strip().splitlines()[0]}")
        elif "exceeding session length" in warn_text:
            print(f"  FAIL unexpected overrun: {warn_text.strip()}")
            failures += 1
        else:
            print("  ok no overrun")

        slides_marked = gpp_slides(body)
        slides_out = expand_timeplan(
            slides_marked,
            warn=False,
            timer_mode="slides-html",
            scripts_dir="SCRIPTS",
        )
        iframe_n = slides_out.count("data-background-iframe")
        if iframe_n != case["iframe_count"]:
            print(f"  FAIL iframe count {iframe_n} != {case['iframe_count']}")
            failures += 1
        else:
            print(f"  ok iframe count={iframe_n}")

        if case.get("timer_title"):
            needle = f"duration={case['timer_clock']}&title={case['timer_title']}"
            if needle not in slides_out:
                print(f"  FAIL missing timer chrome: {needle}")
                failures += 1
            else:
                print(f"  ok timer at {case['timer_clock']}")
            if "*Class test timer" not in notes_out:
                print("  FAIL missing notes timer placeholder")
                failures += 1
            else:
                print("  ok notes timer placeholder")

        if "<!--lamd-" in notes_out or "<!--lamd-" in slides_out:
            print("  FAIL markers leaked")
            failures += 1

    if failures:
        print(f"\n{failures} failure(s)")
        return 1
    print("\nAll IEI fork validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
