"""CIP-001B gpp macros for lecture time allocation markers.

Markers alone must not emit classtimer Reveal chrome; the post-gpp
expand pass emits CIP-0012 chrome only for ``timer``-flagged blocks.
"""

from __future__ import annotations

import io
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
        out = expand_timeplan(marked, warn=False, timer_mode="none")
        assert "<!--lamd-" not in out
        assert "| 10:05–10:15 | 10 | Quiz 3 |" in out
        assert "| 10:15–10:35 | 20 | Exponential family |" in out
        assert "| 10:35–10:45 | 10 | Break |" in out
        assert "data-background-iframe" not in out
        assert "timer/index.html" not in out

    def test_gpp_then_expand_timer_bridge_slides_html(self) -> None:
        body = _read(FIXTURES / "timeplan-macros.md")
        marked = _gpp(
            ["-DSLIDES=1", "-DHTML=1"],
            "talk-macros-null.gpp",
            "talk-macros-html.gpp",
            "talk-macros-slides.gpp",
            "talk-macros-slides-html.gpp",
            body=body,
        )
        assert "data-background-iframe" not in marked
        out = expand_timeplan(marked, warn=False, timer_mode="slides-html", scripts_dir="SCRIPTS")
        assert "| 10:05–10:15 | 10 | Quiz 3 |" in out
        # Only Break is flagged timer → start clock 10:35.
        assert "duration=10:35&title=Break" in out
        assert out.count("data-background-iframe") == 1
        assert "duration=10:05&title=Quiz 3" not in out

    def test_gpp_then_expand_timer_bridge_notes(self) -> None:
        body = _read(FIXTURES / "timeplan-macros.md")
        marked = _gpp(
            ["-DNOTES=1"],
            "talk-macros-null.gpp",
            "talk-macros-notes.gpp",
            body=body,
        )
        out = expand_timeplan(marked, warn=False, timer_mode="notes")
        assert "*Class test timer (Break): 10:35*" in out
        assert "data-background-iframe" not in out

    def test_include_order_in_compiled_plan(self) -> None:
        body = _read(FIXTURES / "timeplan-with-include.md")
        # Resolve fixture-relative includes via -I on the fixtures dir.
        chunks = [
            "\\include{talk-macros-null.gpp}",
            "\\include{talk-macros-notes.gpp}",
            body,
        ]
        gpp_input = "\n".join(chunks)
        result = subprocess.run(
            [
                "gpp",
                "-T",
                f"-I{MACROS}",
                f"-I{FIXTURES}",
                "-DNOTES=1",
                "-DscriptsDir=SCRIPTS",
            ],
            input=gpp_input,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        out = expand_timeplan(result.stdout, warn=False, timer_mode="slides-html", scripts_dir="SCRIPTS")
        assert "| 09:00–09:10 | 10 | Opening |" in out
        assert "| 09:10–09:25 | 15 | From include |" in out
        assert "| 09:25–09:45 | 20 | Closing |" in out
        assert "duration=09:25&title=Closing" in out
        assert out.count("data-background-iframe") == 1

    def test_overrun_fixture_warns(self) -> None:
        body = _read(FIXTURES / "timeplan-overrun.md")
        marked = _gpp(
            ["-DNOTES=1"],
            "talk-macros-null.gpp",
            "talk-macros-notes.gpp",
            body=body,
        )
        buf = io.StringIO()
        out = expand_timeplan(marked, warn=True, warn_stream=buf, timer_mode="none")
        assert "exceeding session length 25" in buf.getvalue()
        assert "| 10:00–10:20 | 20 | A |" in out
        assert "| 10:20–10:40 | 20 | B |" in out
