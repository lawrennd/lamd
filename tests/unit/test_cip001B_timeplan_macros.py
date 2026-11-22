"""CIP-001B gpp macros for lecture time allocation markers.

Markers must be collectable and must not emit classtimer Reveal chrome
until the optional timer-bridge task lands.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

import lamd
from lamd.timeplan import expand_timeplan

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "cip001B"
MACROS = Path(os.path.dirname(lamd.__file__)) / "macros"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _gpp(defines: list[str], *macro_files: str, body: str) -> str:
    chunks: list[str] = []
    for name in macro_files:
        chunks.append(f"\\include{{{name}}}")
    chunks.append(body)
    gpp_input = "\n".join(chunks)
    cmd = ["gpp", "-T", f"-I{MACROS}", "-DscriptsDir=SCRIPTS"]
    cmd.extend(defines)
    result = subprocess.run(
        cmd,
        input=gpp_input,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, f"gpp failed: {result.stderr}\ninput:\n{gpp_input}"
    return result.stdout


@pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")
class TestTimeplanMacros:
    def test_null_emits_markers_without_timer_chrome(self) -> None:
        body = _read(FIXTURES / "timeplan-macros.md")
        out = _gpp([], "talk-macros-null.gpp", body=body)
        assert "<!--lamd-sessionstart|10:05-->" in out
        assert "<!--lamd-sessionlength|110-->" in out
        assert "<!--lamd-timeplan-->" in out
        assert "<!--lamd-blocktime|10|Quiz 3|-->" in out
        assert "<!--lamd-blocktime|20|Exponential family|-->" in out
        assert "<!--lamd-blocktime|10|Break|timer-->" in out
        assert "data-background-iframe" not in out
        assert "timer/index.html" not in out

    def test_notes_emits_markers_without_timer_chrome(self) -> None:
        body = _read(FIXTURES / "timeplan-macros.md")
        out = _gpp(
            ["-DNOTES=1"],
            "talk-macros-null.gpp",
            "talk-macros-notes.gpp",
            body=body,
        )
        assert "<!--lamd-timeplan-->" in out
        assert "<!--lamd-blocktime|10|Break|timer-->" in out
        assert "data-background-iframe" not in out

    def test_slides_html_markers_do_not_create_timer_iframes(self) -> None:
        body = _read(FIXTURES / "timeplan-macros.md")
        out = _gpp(
            ["-DSLIDES=1", "-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            "talk-macros-slides.gpp",
            "talk-macros-slides-html.gpp",
            body=body,
        )
        assert "<!--lamd-blocktime|10|Break|timer-->" in out
        assert "data-background-iframe" not in out
        assert "timer/index.html" not in out

    def test_gpp_then_expand_emits_clock_table(self) -> None:
        body = _read(FIXTURES / "timeplan-macros.md")
        marked = _gpp(
            ["-DNOTES=1"],
            "talk-macros-null.gpp",
            "talk-macros-notes.gpp",
            body=body,
        )
        out = expand_timeplan(marked, warn=False)
        assert "<!--lamd-" not in out
        assert "| 10:05–10:15 | 10 | Quiz 3 |" in out
        assert "| 10:15–10:35 | 20 | Exponential family |" in out
        assert "| 10:35–10:45 | 10 | Break |" in out
        assert "data-background-iframe" not in out
        assert "timer/index.html" not in out
