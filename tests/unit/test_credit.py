"""Tests for CIP-0016 diagram credit resolver and formatters."""

from __future__ import annotations

import argparse
import os

from lamd.credit import (
    credit_output_context,
    expand_diagramcredit,
    format_credit,
    format_notes,
    format_slides,
    license_label,
    may_show_license,
    normalise_stem,
    resolve_credit,
)
from lamd.mdpp import apply_diagram_credits

FIXTURES = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fixtures", "cip0016"))


def test_normalise_stem_strips_diagramsdir_macro_and_extension() -> None:
    assert normalise_stem(r"\diagramsDir/physics/daniel-bernoulli.jpg") == "physics/daniel-bernoulli"
    assert normalise_stem(r"\diagramsDir/physics/daniel-bernoulli") == "physics/daniel-bernoulli"
    assert normalise_stem("physics/daniel-bernoulli.png") == "physics/daniel-bernoulli"


def test_yaml_wins_over_url() -> None:
    credit = resolve_credit(FIXTURES, "yaml-wins")
    assert credit is not None
    assert credit.origin == "yaml"
    assert credit.title == "YAML title"
    assert credit.source != "https://example.com/should-not-be-used"


def test_url_only_does_not_claim_license() -> None:
    credit = resolve_credit(FIXTURES, "url-only")
    assert credit is not None
    assert credit.origin == "url"
    assert credit.status == "unknown"
    assert credit.source.endswith("Example.jpg")
    assert credit.license is None
    assert may_show_license(credit) is False
    notes = format_notes(credit)
    assert "Source" in notes
    assert "CC" not in notes


def test_empty_url_and_missing_sidecar_are_empty() -> None:
    assert resolve_credit(FIXTURES, "empty") is None
    assert resolve_credit(FIXTURES, "does-not-exist") is None
    assert expand_diagramcredit(r"\diagramcredit{\diagramsDir/missing}", FIXTURES, "notes-html") == ""


def test_own_status_silent_unless_show_own() -> None:
    own = resolve_credit(FIXTURES, "own")
    shown = resolve_credit(FIXTURES, "own-shown")
    assert own is not None and shown is not None
    assert format_notes(own) == ""
    assert "Generated plot" in format_notes(shown)


def test_fair_use_has_no_cc_label_even_if_yaml_has_license() -> None:
    credit = resolve_credit(FIXTURES, "fair-use")
    assert credit is not None
    assert credit.license == "CC-BY-4.0"
    notes = format_notes(credit)
    assert "Source" in notes
    assert "CC BY" not in notes
    assert "creativecommons.org" not in notes


def test_trademark_emits_nothing() -> None:
    credit = resolve_credit(FIXTURES, "trademark")
    assert credit is not None
    assert format_notes(credit) == ""
    assert format_slides(credit) == ""


def test_notes_formatter_full_tasl() -> None:
    credit = resolve_credit(FIXTURES, "full")
    assert credit is not None
    notes = format_notes(credit)
    assert notes.startswith("*Credit:*")
    assert "Portrait of Daniel Bernoulli by Johann Rudolf Huber (attrib.)." in notes
    assert "[Source](https://commons.wikimedia.org/wiki/File:Daniel_Bernoulli.jpg)" in notes
    assert "[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)" in notes
    assert "Modified: cropped." in notes


def test_slides_formatter_compact_and_visible() -> None:
    credit = resolve_credit(FIXTURES, "full")
    slides = format_slides(credit)
    assert slides.startswith(r"\small{\alignright{")
    assert "Portrait of Daniel Bernoulli" in slides
    assert "Johann Rudolf Huber (attrib.)" in slides
    assert "CC BY-SA 4.0" in slides
    assert "aside" not in slides


def test_license_label_human_form() -> None:
    assert license_label("CC-BY-SA-4.0") == "CC BY-SA 4.0"
    assert license_label("FairUse") is None


def test_output_context_matrix() -> None:
    assert credit_output_context("html", "slides") == "slides-html"
    assert credit_output_context("html", "notes") == "notes-html"
    assert credit_output_context("ipynb", "notes") == "notes-html"
    assert credit_output_context("tex", "notes") == "tex"
    assert credit_output_context("pptx", "slides") == "empty"
    assert credit_output_context("manim", "slides") == "empty"
    assert credit_output_context("html", "code") == "empty"


def test_expand_diagramcredit_notes_and_slides() -> None:
    source = r"before \diagramcredit{\diagramsDir/full} after"
    notes = expand_diagramcredit(source, FIXTURES, "notes-html")
    slides = expand_diagramcredit(source, FIXTURES, "slides-html")
    empty = expand_diagramcredit(source, FIXTURES, "empty")
    assert "*Credit:*" in notes
    assert r"\small{\alignright{" in slides
    assert empty == "before  after"


def test_apply_diagram_credits_uses_filesystem_dir_not_web_url() -> None:
    args = argparse.Namespace(to="html", format="notes", diagrams_dir=FIXTURES)
    iface = {
        "diagramsdir": "/does/not/exist",
        "diagramsurl": "https://example.org/diagrams",
    }
    out = apply_diagram_credits(r"\diagramcredit{\diagramsDir/full}", args, iface)
    assert "*Credit:*" in out
    assert "CC BY-SA 4.0" in out


def test_apply_diagram_credits_slides_html() -> None:
    args = argparse.Namespace(to="html", format="slides", diagrams_dir=FIXTURES)
    iface = {"diagramsdir": FIXTURES}
    out = apply_diagram_credits(r"\diagramcredit{\diagramsDir/full}", args, iface)
    assert r"\small{\alignright{" in out


def test_tex_uses_markdown_notes_line() -> None:
    credit = resolve_credit(FIXTURES, "full")
    tex = format_credit(credit, "tex")
    assert "[Source](" in tex
    assert tex.startswith("*Credit:*")
