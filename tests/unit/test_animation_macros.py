"""Tests for animation macro definitions in talk-macros-slides-html.gpp.

These tests guard against regressions introduced by the Phase 1 fixes
described in CIP-0007: specifically the duplicate \newframe definition.
"""

import os
import re

import lamd


def _macro_file_path() -> str:
    """Return the absolute path to talk-macros-slides-html.gpp."""
    return os.path.join(os.path.dirname(lamd.__file__), "macros", "talk-macros-slides-html.gpp")


def _read_macro_file() -> str:
    path = _macro_file_path()
    assert os.path.exists(path), f"Macro file not found: {path}"
    with open(path) as f:
        return f.read()


class TestAnimationMacros:
    """Tests for animation macros in the HTML slides macro file."""

    def test_newframe_defined_exactly_once(self) -> None:
        """Regression: duplicate \\newframe definition must not exist (CIP-0007 Phase 1)."""
        content = _read_macro_file()
        # Count occurrences of \define{\newframe (ignoring whitespace variants)
        matches = re.findall(r"\\define\s*\{\\newframe\b", content)
        assert len(matches) == 1, (
            f"Expected exactly one \\define{{\\newframe}} but found {len(matches)}. "
            "Duplicate definitions cause the second to silently override the first."
        )

    def test_newframe_does_not_create_new_slide(self) -> None:
        """The HTML \\newframe must NOT call \\newslide — frames live in one slide."""
        content = _read_macro_file()
        # Isolate the newframe definition body
        match = re.search(
            r"\\define\s*\{\\newframe\{[^}]*\}\{[^}]*\}\{[^}]*\}\}\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}",
            content,
            re.DOTALL,
        )
        # Simpler check: the word \newslide must not appear adjacent to the newframe define block
        # Find the line(s) of the newframe definition and check nearby context
        lines = content.splitlines()
        newframe_line_indices = [i for i, line in enumerate(lines) if re.search(r"\\define\s*\{\\newframe", line)]
        assert len(newframe_line_indices) == 1, "Expected exactly one \\newframe definition line"
        idx = newframe_line_indices[0]
        # The definition body is on the same line (single-line form)
        definition_line = lines[idx]
        assert "\\newslide" not in definition_line, (
            "\\newframe must not call \\newslide in HTML output — animation frames "
            "are shown/hidden on a single slide via JavaScript."
        )

    def test_endanimation_is_defined(self) -> None:
        """\\endanimation must be defined and close the animation container div."""
        content = _read_macro_file()
        # Find the endanimation definition
        match = re.search(r"\\define\s*\{\\endanimation\}\s*\{([^}]*)\}", content)
        assert match is not None, "\\endanimation is not defined in talk-macros-slides-html.gpp"
        body = match.group(1).strip()
        assert "</div>" in body, f"\\endanimation body '{body}' must close the animation container with </div>"

    def test_startanimation_is_defined(self) -> None:
        """\\startanimation must be defined and open a container div."""
        content = _read_macro_file()
        assert r"\define{\startanimation{" in content, "\\startanimation is not defined in talk-macros-slides-html.gpp"
        # The definition must open a div
        idx = content.find(r"\define{\startanimation{")
        # Find the body: everything after the opening brace of the body
        snippet = content[idx : idx + 400]
        assert "<div>" in snippet, "\\startanimation must open a <div> container for the animation group"

    def test_newframe_produces_centered_div(self) -> None:
        """\\newframe definition must use text-align:center styling."""
        content = _read_macro_file()
        newframe_match = re.search(r"\\define\s*\{\\newframe[^}]*\}[^}]*\}\s*\{([^\n]*)\}", content)
        assert newframe_match is not None, "Could not locate \\newframe definition body"
        body = newframe_match.group(1)
        assert "text-align:center" in body, f"\\newframe body should include 'text-align:center', got: {body}"
