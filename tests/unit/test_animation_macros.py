"""Tests for animation macro definitions across all output format files.

Phase 1 (CIP-0007): Guard against duplicate \\newframe in talk-macros-slides-html.gpp.
Phase 2 (CIP-0007): Verify fallback implementations exist in notes, ipynb, tex, pptx.
"""

import os
import re

import lamd


def _macro_file_path(filename: str = "talk-macros-slides-html.gpp") -> str:
    """Return the absolute path to a macro file in lamd/macros/."""
    return os.path.join(os.path.dirname(lamd.__file__), "macros", filename)


def _read_macro_file(filename: str = "talk-macros-slides-html.gpp") -> str:
    path = _macro_file_path(filename)
    assert os.path.exists(path), f"Macro file not found: {path}"
    with open(path) as f:
        return f.read()


def _has_animation_macros(content: str) -> tuple[bool, bool, bool]:
    """Return (has_startanimation, has_newframe, has_endanimation) for the given GPP content."""
    has_start = bool(re.search(r"\\define\s*\{\\startanimation\b", content))
    has_new = bool(re.search(r"\\define\s*\{\\newframe\b", content))
    has_end = bool(re.search(r"\\define\s*\{\\endanimation\b", content))
    return has_start, has_new, has_end


class TestAnimationMacros:
    """Tests for animation macros in the HTML slides macro file (Phase 1 regressions)."""

    def test_newframe_defined_exactly_once(self) -> None:
        """Regression: duplicate \\newframe definition must not exist (CIP-0007 Phase 1)."""
        content = _read_macro_file("talk-macros-slides-html.gpp")
        # Count occurrences of \define{\newframe (ignoring whitespace variants)
        matches = re.findall(r"\\define\s*\{\\newframe\b", content)
        assert len(matches) == 1, (
            f"Expected exactly one \\define{{\\newframe}} but found {len(matches)}. "
            "Duplicate definitions cause the second to silently override the first."
        )

    def test_newframe_does_not_create_new_slide(self) -> None:
        """The HTML \\newframe must NOT call \\newslide — frames live in one slide."""
        content = _read_macro_file("talk-macros-slides-html.gpp")
        lines = content.splitlines()
        newframe_line_indices = [i for i, line in enumerate(lines) if re.search(r"\\define\s*\{\\newframe", line)]
        assert len(newframe_line_indices) == 1, "Expected exactly one \\newframe definition line"
        idx = newframe_line_indices[0]
        definition_line = lines[idx]
        assert "\\newslide" not in definition_line, (
            "\\newframe must not call \\newslide in HTML output — animation frames "
            "are shown/hidden on a single slide via JavaScript."
        )

    def test_endanimation_is_defined(self) -> None:
        """\\endanimation must be defined and close the animation container div."""
        content = _read_macro_file("talk-macros-slides-html.gpp")
        match = re.search(r"\\define\s*\{\\endanimation\}\s*\{([^}]*)\}", content)
        assert match is not None, "\\endanimation is not defined in talk-macros-slides-html.gpp"
        body = match.group(1).strip()
        assert "</div>" in body, f"\\endanimation body '{body}' must close the animation container with </div>"

    def test_startanimation_is_defined(self) -> None:
        """\\startanimation must be defined and open a container div."""
        content = _read_macro_file("talk-macros-slides-html.gpp")
        assert r"\define{\startanimation{" in content, "\\startanimation is not defined in talk-macros-slides-html.gpp"
        idx = content.find(r"\define{\startanimation{")
        snippet = content[idx : idx + 400]
        assert "<div>" in snippet, "\\startanimation must open a <div> container for the animation group"

    def test_newframe_produces_centered_div(self) -> None:
        """\\newframe definition must use text-align:center styling."""
        content = _read_macro_file("talk-macros-slides-html.gpp")
        newframe_match = re.search(r"\\define\s*\{\\newframe[^}]*\}[^}]*\}\s*\{([^\n]*)\}", content)
        assert newframe_match is not None, "Could not locate \\newframe definition body"
        body = newframe_match.group(1)
        assert "text-align:center" in body, f"\\newframe body should include 'text-align:center', got: {body}"


class TestAnimationMacrosFallbacks:
    """Phase 2: Verify fallback implementations for non-HTML formats (CIP-0007)."""

    def _assert_all_three_macros_defined(self, filename: str) -> None:
        """Helper: all three animation macros must be explicitly defined."""
        content = _read_macro_file(filename)
        has_start, has_new, has_end = _has_animation_macros(content)
        assert has_start, f"\\startanimation not defined in {filename}"
        assert has_new, f"\\newframe not defined in {filename}"
        assert has_end, f"\\endanimation not defined in {filename}"

    def _newframe_body(self, filename: str) -> str:
        """Return the body of the \\newframe definition in the given file."""
        content = _read_macro_file(filename)
        # Match multi-line definition body: \define{\newframe{a}{b}{c}}{BODY}
        match = re.search(
            r"\\define\s*\{\\newframe\{[^}]*\}\{[^}]*\}\{[^}]*\}\}\s*\{(.*?)\}(?=\s*\\define|\s*\\endif|\s*$)",
            content,
            re.DOTALL,
        )
        assert match is not None, f"Cannot parse \\newframe body in {filename}"
        return match.group(1)

    # --- Notes format ---

    def test_notes_defines_startanimation(self) -> None:
        """Notes format must explicitly define \\startanimation."""
        content = _read_macro_file("talk-macros-notes.gpp")
        assert re.search(r"\\define\s*\{\\startanimation\b", content), "\\startanimation not defined in talk-macros-notes.gpp"

    def test_notes_startanimation_has_label(self) -> None:
        """Notes \\startanimation must produce a visible label so readers know an animation follows."""
        content = _read_macro_file("talk-macros-notes.gpp")
        idx = content.find(r"\define{\startanimation{")
        snippet = content[idx : idx + 200]
        assert (
            "Animation" in snippet or "animation" in snippet
        ), "Notes \\startanimation should include an 'Animation' label so readers know the context"

    def test_notes_newframe_preserves_content(self) -> None:
        """Notes \\newframe must include \\contents so frame content is not dropped."""
        content = _read_macro_file("talk-macros-notes.gpp")
        body = self._newframe_body("talk-macros-notes.gpp")
        assert r"\contents" in body, f"Notes \\newframe must pass through \\contents, got: {body!r}"

    def test_notes_newframe_has_paragraph_break(self) -> None:
        """Notes \\newframe must add spacing so consecutive frames don't run together."""
        body = self._newframe_body("talk-macros-notes.gpp")
        # Body should end with a blank line (two newlines) or start a new paragraph
        assert "\n" in body, f"Notes \\newframe body must include newlines for paragraph separation, got: {body!r}"

    # --- IPynb slides format ---

    def test_ipynb_defines_all_animation_macros(self) -> None:
        """IPynb slides must explicitly define all three animation macros."""
        self._assert_all_three_macros_defined("talk-macros-slides-ipynb.gpp")

    def test_ipynb_newframe_preserves_content(self) -> None:
        """IPynb \\newframe must pass through frame content."""
        body = self._newframe_body("talk-macros-slides-ipynb.gpp")
        assert r"\contents" in body, f"IPynb \\newframe must include \\contents, got: {body!r}"

    def test_ipynb_newframe_does_not_use_escape_newlines(self) -> None:
        """IPynb \\newframe must use real newlines, not GPP \\n escape sequences."""
        content = _read_macro_file("talk-macros-slides-ipynb.gpp")
        # Find the newframe definition and check for escaped \n
        match = re.search(r"\\define\s*\{\\newframe[^}]*\}[^}]*\}[^}]*\}\}\s*\{([^\n]*)", content)
        if match:
            first_line_body = match.group(1)
            assert (
                r"\n" not in first_line_body
            ), "IPynb \\newframe must not use GPP \\n escape; use real newlines in the definition body."

    # --- TEX slides format ---

    def test_tex_slides_defines_all_animation_macros(self) -> None:
        """TEX slides must explicitly define all three animation macros (no silent null fallback)."""
        self._assert_all_three_macros_defined("talk-macros-slides-tex.gpp")

    def test_tex_slides_newframe_preserves_content(self) -> None:
        """TEX \\newframe must pass through frame content so nothing is silently dropped."""
        body = self._newframe_body("talk-macros-slides-tex.gpp")
        assert r"\contents" in body, f"TEX \\newframe must include \\contents, got: {body!r}"

    # --- PPTX slides format ---

    def test_pptx_slides_defines_all_animation_macros(self) -> None:
        """PPTX slides must explicitly define all three animation macros."""
        self._assert_all_three_macros_defined("talk-macros-slides-pptx.gpp")

    def test_pptx_slides_newframe_preserves_content(self) -> None:
        """PPTX \\newframe must pass through frame content so nothing is silently dropped."""
        body = self._newframe_body("talk-macros-slides-pptx.gpp")
        assert r"\contents" in body, f"PPTX \\newframe must include \\contents, got: {body!r}"
