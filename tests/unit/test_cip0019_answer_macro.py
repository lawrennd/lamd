"""CIP-0019: in-place ``\\answer{text}{blankheight}`` slot."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

import lamd

MACROS = Path(os.path.dirname(lamd.__file__)) / "macros"
_GPP = pytest.mark.skipif(shutil.which("gpp") is None, reason="gpp not available")

ANSWER = r"\answer{Little's law follows from the arrival rate.}{6}"
BODY = "Little's law follows from the arrival rate."


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


def test_answer_macro_defined():
    notes = (MACROS / "talk-macros-notes.gpp").read_text()
    html = (MACROS / "talk-macros-notes-html.gpp").read_text()
    slides = (MACROS / "talk-macros-slides.gpp").read_text()
    null = (MACROS / "talk-macros-null.gpp").read_text()
    assert r"\define{\answer{text}{blankheight}}" in notes
    assert r"\define{\answer{text}{blankheight}}" in html
    assert r"\define{\answer{text}{blankheight}}" in slides
    assert r"\define{\answer{text}{blankheight}}" in null


@_GPP
def test_answer_notes_lecturer_prints_body():
    out = _gpp(["-DNOTES=1"], f"START{ANSWER}END")
    assert BODY in out
    assert r"\vspace*" not in out
    assert "answer-blank" not in out


@_GPP
def test_answer_notes_student_tex_vspace():
    out = _gpp(["-DNOTES=1", "-DSTUDENT=1"], f"START{ANSWER}END")
    assert BODY not in out
    assert r"\vspace*{6 cm}" in out or r"\vspace*{6cm}" in out


@_GPP
def test_answer_notes_student_html_div():
    out = _gpp(["-DNOTES=1", "-DHTML=1", "-DSTUDENT=1"], f"START{ANSWER}END")
    assert BODY not in out
    assert 'class="answer-blank"' in out
    assert "min-height:6 cm" in out or "min-height:6cm" in out
    assert r"\vspace*" not in out


@_GPP
def test_answer_slides_always_print_body():
    lecturer = _gpp(["-DSLIDES=1"], f"START{ANSWER}END")
    student = _gpp(["-DSLIDES=1", "-DSTUDENT=1"], f"START{ANSWER}END")
    assert BODY in lecturer
    assert BODY in student
    assert r"\vspace*" not in lecturer
    assert r"\vspace*" not in student


@_GPP
def test_answer_null_context_is_empty():
    out = _gpp([], f"START{ANSWER}END")
    assert "STARTEND" in out.replace("\n", "")
    assert BODY not in out


@_GPP
def test_writeassignment_model_answer_still_expands():
    body = r"\writeassignment{Question text}{5}{MODEL-ANSWER}"
    with_key = _gpp(
        ["-DNOTES=1", "-DIPYNB=1", "-DEXERCISES=1", "-DASSIGNMENTANSWERS=1"],
        body,
    )
    without_key = _gpp(
        ["-DNOTES=1", "-DIPYNB=1", "-DEXERCISES=1"],
        body,
    )
    assert "MODEL-ANSWER" in with_key
    assert "Question text" in with_key
    assert "MODEL-ANSWER" not in without_key
    assert "Question text" in without_key
