"""Machine-review pointer and heading macros (notes only)."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

import lamd

MACROS = Path(os.path.dirname(lamd.__file__)) / "macros"
_GPP = pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")


def _gpp(defines: list[str], body: str) -> str:
    gpp_input = "\\include{talk-macros.gpp}\n" + body
    cmd = ["gpp", "-T", f"-I{MACROS}", "-DscriptsDir=SCRIPTS", "-DwriteDiagramsDir=DIAGRAMS"]
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


def test_machine_review_macros_are_defined():
    notes = (MACROS / "talk-macros-notes.gpp").read_text()
    html = (MACROS / "talk-macros-notes-html.gpp").read_text()
    null = (MACROS / "talk-macros-null.gpp").read_text()
    assert r"\define{\machinereviewlink}" in notes
    assert r"\define{\machinereview}" in notes
    assert r"\define{\machinereviewlink}" in html
    assert r"\define{\machinereview}" in null


@_GPP
def test_machine_review_macros_notes_markdown():
    out = _gpp(
        ["-DNOTES=1"],
        "START\n\\machinereviewlink\nMID\n\\machinereview\nEND\n",
    )
    assert "START" in out and "MID" in out and "END" in out
    assert "#machine-review" in out
    assert "Machine Review" in out
    assert "<aside" not in out


@_GPP
def test_machine_review_macros_notes_html_aside():
    out = _gpp(
        ["-DNOTES=1", "-DHTML=1"],
        "\\machinereviewlink\n\\machinereview\n",
    )
    assert 'class="machine-review-link"' in out
    assert 'href="#machine-review"' in out
    assert "solid #ccc" in out
    assert "Machine Review" in out


@_GPP
def test_machine_review_macros_slides_empty():
    out = _gpp(
        ["-DSLIDES=1"],
        "A\\machinereviewlink{}B\\machinereview{}C",
    )
    assert "A" in out and "B" in out and "C" in out
    assert "Machine Review" not in out
    assert "machine-review" not in out
