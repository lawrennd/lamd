"""Unit tests for lamd.util.lamd_manim_helper.

Manim is NOT required.  All Manim classes are replaced with lightweight
fakes via ``unittest.mock.patch`` so that the tests can run in a plain CI
environment without a Manim installation.
"""

import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# ---------------------------------------------------------------------------
# Build a minimal fake Manim module so that the helper's TYPE_CHECKING block
# and local imports inside the functions can succeed without a real install.
# ---------------------------------------------------------------------------


def _make_fake_manim():
    """Return a fake ``manim`` module with stub classes."""

    class FakeMarkupText:
        def __init__(self, text, font_size=36, **kwargs):
            self.text = text
            self.font_size = font_size

        def __repr__(self):
            return f"MarkupText({self.text!r})"

    class FakeMathTex:
        def __init__(self, latex, font_size=36, **kwargs):
            self.latex = latex
            self.font_size = font_size

        def __repr__(self):
            return f"MathTex({self.latex!r})"

    class FakeVGroup:
        def __init__(self, *mobjects):
            self.mobjects = list(mobjects)

        def arrange(self, *args, **kwargs):
            return self

        def __repr__(self):
            return f"VGroup({self.mobjects!r})"

    fake = types.ModuleType("manim")
    fake.MarkupText = FakeMarkupText
    fake.MathTex = FakeMathTex
    fake.VGroup = FakeVGroup
    return fake


_FAKE_MANIM = _make_fake_manim()


# ---------------------------------------------------------------------------
# Helpers to invoke helper functions with the fake Manim module injected.
# ---------------------------------------------------------------------------


def _import_helper():
    """Import the helper module, injecting the fake Manim module."""
    # Ensure the fake module is present before import
    sys.modules.setdefault("manim", _FAKE_MANIM)
    # Import fresh each time (in case of re-import)
    import importlib

    import lamd.util.lamd_manim_helper as mod

    importlib.reload(mod)
    return mod


class TestMdToPango(unittest.TestCase):
    """Tests for the internal _md_to_pango helper."""

    def setUp(self):
        self.mod = _import_helper()

    def test_plain_text_unchanged(self):
        self.assertEqual(self.mod._md_to_pango("hello world"), "hello world")

    def test_bold(self):
        self.assertEqual(self.mod._md_to_pango("**bold**"), "<b>bold</b>")

    def test_italic(self):
        self.assertEqual(self.mod._md_to_pango("*italic*"), "<i>italic</i>")

    def test_bold_and_italic(self):
        result = self.mod._md_to_pango("**bold** and *italic*")
        self.assertEqual(result, "<b>bold</b> and <i>italic</i>")

    def test_no_partial_bold(self):
        # Single asterisk should not trigger bold
        self.assertEqual(self.mod._md_to_pango("a * b"), "a * b")


class TestLamdText(unittest.TestCase):
    """Tests for lamd_text."""

    def setUp(self):
        self.mod = _import_helper()
        self.MarkupText = _FAKE_MANIM.MarkupText
        self.MathTex = _FAKE_MANIM.MathTex
        self.VGroup = _FAKE_MANIM.VGroup

    def test_empty_string(self):
        result = self.mod.lamd_text("")
        self.assertIsInstance(result, self.MarkupText)
        self.assertEqual(result.text, "")

    def test_plain_text_returns_markup_text(self):
        result = self.mod.lamd_text("Hello world")
        self.assertIsInstance(result, self.MarkupText)
        self.assertEqual(result.text, "Hello world")

    def test_bold_plain_text(self):
        result = self.mod.lamd_text("**bold** word")
        self.assertIsInstance(result, self.MarkupText)
        self.assertEqual(result.text, "<b>bold</b> word")

    def test_italic_plain_text(self):
        result = self.mod.lamd_text("*italic* word")
        self.assertIsInstance(result, self.MarkupText)
        self.assertEqual(result.text, "<i>italic</i> word")

    def test_inline_math_only_returns_mathtex(self):
        result = self.mod.lamd_text("$x^2$")
        self.assertIsInstance(result, self.MathTex)
        self.assertEqual(result.latex, "x^2")

    def test_mixed_text_and_math_returns_vgroup(self):
        result = self.mod.lamd_text("Area is $A = \\pi r^2$")
        self.assertIsInstance(result, self.VGroup)
        self.assertEqual(len(result.mobjects), 2)
        self.assertIsInstance(result.mobjects[0], self.MarkupText)
        self.assertIsInstance(result.mobjects[1], self.MathTex)

    def test_font_size_passed_through(self):
        result = self.mod.lamd_text("Hello", font_size=48)
        self.assertEqual(result.font_size, 48)

    def test_math_font_size_passed_through(self):
        result = self.mod.lamd_text("$E=mc^2$", font_size=24)
        self.assertEqual(result.font_size, 24)


class TestLamdDisplayMath(unittest.TestCase):
    """Tests for lamd_display_math."""

    def setUp(self):
        self.mod = _import_helper()
        self.MathTex = _FAKE_MANIM.MathTex

    def test_returns_mathtex(self):
        result = self.mod.lamd_display_math("\\frac{1}{2}")
        self.assertIsInstance(result, self.MathTex)

    def test_latex_content(self):
        result = self.mod.lamd_display_math("\\sum_{i=0}^n x_i")
        self.assertEqual(result.latex, "\\sum_{i=0}^n x_i")

    def test_default_font_size(self):
        result = self.mod.lamd_display_math("x")
        self.assertEqual(result.font_size, 48)

    def test_custom_font_size(self):
        result = self.mod.lamd_display_math("x", font_size=60)
        self.assertEqual(result.font_size, 60)


if __name__ == "__main__":
    unittest.main()
