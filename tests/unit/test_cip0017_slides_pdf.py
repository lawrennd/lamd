"""CIP-0017: Beamer slides PDF macros, flags, and maketalk targets."""

import os
import subprocess
from unittest.mock import mock_open, patch

import lamd
from lamd.maketalk import main


def _slides_tex_macros() -> str:
    path = os.path.join(os.path.dirname(lamd.__file__), "macros", "talk-macros-slides-tex.gpp")
    with open(path, encoding="utf-8") as f:
        return f.read()


def _make_tex() -> str:
    path = os.path.join(os.path.dirname(lamd.__file__), "makefiles", "make-tex.mk")
    with open(path, encoding="utf-8") as f:
        return f.read()


def test_newslide_tex_drops_reveal_attrs():
    content = _slides_tex_macros()
    assert r"\define{\newslide{text}{commands}}" in content
    # Attrs argument is accepted but not interpolated into the heading.
    assert r"## \text" in content
    assert ".scrollable" not in content
    assert "data-background" not in content


def test_figure_tex_is_not_a_float():
    content = _slides_tex_macros()
    assert r"\begin{figure}" not in content
    assert r"\begin{center}" in content


def test_makefile_has_beamer_slides_pdf_rule():
    content = _make_tex()
    assert "${BASE}.slides.pdf:" in content
    assert "-t beamer" in content
    assert "--slide-level 2" in content
    assert "%.slides.tex.markdown:" in content


@patch("sys.argv", ["maketalk", "test.md", "--format", "slides", "--to", "pdf"])
@patch("lamd.maketalk.open", new_callable=mock_open)
@patch("os.system")
@patch("lamd.maketalk.subprocess.run")
@patch("os.path.exists")
def test_maketalk_slides_pdf_target(mock_exists, mock_run, mock_system, mock_file):
    mock_exists.return_value = True
    mock_run.return_value = subprocess.CompletedProcess(["make", "test.slides.pdf"], 0)
    with patch("lamd.__file__", "/path/to/lamd/__init__.py"):
        with patch("lamd.config.interface.Interface.from_file") as mock_interface:
            mock_interface.return_value = {"snippetsdir": "test-snippets", "bibdir": "test-bib"}
            main()
    assert mock_run.call_args_list[-1][0][0] == "make test.slides.pdf"


@patch("sys.argv", ["maketalk", "test.md", "--to", "pdf"])
@patch("lamd.maketalk.open", new_callable=mock_open)
@patch("os.system")
@patch("lamd.maketalk.subprocess.run")
@patch("os.path.exists")
def test_maketalk_to_pdf_builds_notes_and_slides(mock_exists, mock_run, mock_system, mock_file):
    mock_exists.return_value = True
    mock_run.return_value = subprocess.CompletedProcess(["make", "test.notes.pdf", "test.slides.pdf"], 0)
    with patch("lamd.__file__", "/path/to/lamd/__init__.py"):
        with patch("lamd.config.interface.Interface.from_file") as mock_interface:
            mock_interface.return_value = {"snippetsdir": "test-snippets", "bibdir": "test-bib"}
            main()
    assert mock_run.call_args_list[-1][0][0] == "make test.notes.pdf test.slides.pdf"


def test_fixture_contains_newslide_and_notes_split():
    fixture = os.path.join(os.path.dirname(__file__), "../fixtures/cip0017/slides-pdf.md")
    text = open(fixture, encoding="utf-8").read()
    assert r"\newslide{Little's formula}{.scrollable}" in text
    assert r"\notes{" in text
    assert r"\slides{" in text
    assert r"\figure{" in text
