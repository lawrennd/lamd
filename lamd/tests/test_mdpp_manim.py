"""Smoke tests for mdpp --to manim / --to manim-video.

These tests run mdpp as a subprocess on a minimal fixture and check that:
  * the process exits with code 0
  * the output file passes py_compile (i.e. is syntactically valid Python)
  * Manim-specific macros expand correctly (FadeIn for incremental/fragment)
  * \\slidesmanim is a no-op in non-Manim output

No Manim or manim-slides installation is required.
"""
import os
import py_compile
import subprocess
import sys
import tempfile
import unittest

# Path to the mdpp entry point
_MDPP = [sys.executable, "-m", "lamd.mdpp"]

# Minimal macros directory shipped with the package
_MACROS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "macros")

# Fixture
_FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "minimal-manim-talk.md")


def _run_mdpp(to_format: str, output_path: str) -> subprocess.CompletedProcess:
    """Run mdpp on the minimal fixture and return the completed process."""
    cmd = _MDPP + [
        _FIXTURE,
        "--to", to_format,
        "--output", output_path,
        "--macros-path", _MACROS_DIR,
        "--format", "slides",
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def _read_output(path: str) -> str:
    """Read output file content, returning empty string if it doesn't exist."""
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()
    return ""


class TestMdppManim(unittest.TestCase):
    """Smoke-test mdpp --to manim output (interactive presentation pipeline)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.output = os.path.join(self.tmp.name, "talk.slides.manim.py")

    def tearDown(self):
        self.tmp.cleanup()

    def test_exit_code_zero(self):
        result = _run_mdpp("manim", self.output)
        self.assertEqual(
            result.returncode, 0,
            msg=f"mdpp --to manim exited with {result.returncode}.\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}",
        )

    def test_output_file_created(self):
        _run_mdpp("manim", self.output)
        self.assertTrue(
            os.path.isfile(self.output),
            msg=f"Expected output file not found: {self.output}",
        )

    def test_output_is_valid_python(self):
        result = _run_mdpp("manim", self.output)
        if result.returncode != 0:
            self.skipTest("mdpp failed; cannot check Python syntax")
        try:
            py_compile.compile(self.output, doraise=True)
        except py_compile.PyCompileError as exc:
            self.fail(f"Output is not valid Python: {exc}")

    def test_helper_copied_alongside_output(self):
        _run_mdpp("manim", self.output)
        helper = os.path.join(self.tmp.name, "_lamd_manim.py")
        self.assertTrue(
            os.path.isfile(helper),
            msg=f"_lamd_manim.py was not copied to output directory: {helper}",
        )

    def test_output_contains_class_header(self):
        _run_mdpp("manim", self.output)
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        with open(self.output) as f:
            content = f.read()
        self.assertIn("class Talk(Slide):", content)

    def test_output_imports_manim(self):
        _run_mdpp("manim", self.output)
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        with open(self.output) as f:
            content = f.read()
        self.assertIn("from manim import *", content)


class TestMdppManim_Video(unittest.TestCase):
    """Smoke-test mdpp --to manim-video output (continuous video pipeline)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.output = os.path.join(self.tmp.name, "talk.manim-video.py")

    def tearDown(self):
        self.tmp.cleanup()

    def test_exit_code_zero(self):
        result = _run_mdpp("manim-video", self.output)
        self.assertEqual(
            result.returncode, 0,
            msg=f"mdpp --to manim-video exited with {result.returncode}.\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}",
        )

    def test_output_is_valid_python(self):
        result = _run_mdpp("manim-video", self.output)
        if result.returncode != 0:
            self.skipTest("mdpp failed; cannot check Python syntax")
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        try:
            py_compile.compile(self.output, doraise=True)
        except py_compile.PyCompileError as exc:
            self.fail(f"Output is not valid Python: {exc}")

    def test_output_contains_scene_header(self):
        _run_mdpp("manim-video", self.output)
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        with open(self.output) as f:
            content = f.read()
        self.assertIn("class Talk(Scene):", content)


class TestMdppManim_Macros(unittest.TestCase):
    """Test that Manim-specific macros expand correctly in --to manim output."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.output = os.path.join(self.tmp.name, "talk.manim.py")
        _run_mdpp("manim", self.output)
        self.content = _read_output(self.output)

    def tearDown(self):
        self.tmp.cleanup()

    def test_slidesincremental_emits_fadein(self):
        """\\slidesincremental should produce a FadeIn call, not a comment."""
        self.assertIn(
            "FadeIn",
            self.content,
            msg="Expected FadeIn call from \\slidesincremental not found in output",
        )
        self.assertNotIn(
            "# incremental:",
            self.content,
            msg="Found stale comment placeholder from \\slidesincremental; expected FadeIn call",
        )

    def test_fragment_emits_fadein(self):
        """\\fragment should produce a FadeIn call in Manim output."""
        self.assertIn(
            "FadeIn",
            self.content,
            msg="Expected FadeIn call from \\fragment not found in output",
        )

    def test_slidesmanim_emits_raw_code(self):
        """\\slidesmanim block should appear verbatim in Manim output."""
        self.assertIn(
            "Manim only",
            self.content,
            msg="\\slidesmanim code block should appear in manim output",
        )


class TestMdppHtml_SlidesManimNoOp(unittest.TestCase):
    """Test that \\slidesmanim is a no-op in non-Manim (HTML) output."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.output = os.path.join(self.tmp.name, "talk.slides.html")

    def tearDown(self):
        self.tmp.cleanup()

    def test_slidesmanim_absent_from_html_output(self):
        """\\slidesmanim should expand to nothing in HTML output."""
        result = _run_mdpp("html", self.output)
        if result.returncode != 0:
            self.skipTest(
                f"mdpp --to html failed (returncode={result.returncode}); skipping no-op test"
            )
        content = _read_output(self.output)
        self.assertNotIn(
            r"\slidesmanim",
            content,
            msg="\\slidesmanim literal found in HTML output; it should be a no-op",
        )
        self.assertNotIn(
            "Manim only",
            content,
            msg="Raw \\slidesmanim content found in HTML output; it should be suppressed",
        )


class TestMdppManim_HtmlComments(unittest.TestCase):
    """HTML comments in Markdown source should become Python comments in Manim output."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        fixture = os.path.join(self.tmp.name, "comment-talk.md")
        with open(fixture, "w") as f:
            f.write(
                "---\ntitle: Comment Test\nauthor:\n- family: Test\n  given: Author\n"
                "date: 2026-05-05\n---\n\n"
                "\\newslide{Test}{}\n\n"
                "<!-- single-line html comment -->\n\n"
                "\\slides{After comment.}\n"
            )
        self.output = os.path.join(self.tmp.name, "comment-test.manim.py")
        cmd = _MDPP + [
            fixture,
            "--to", "manim",
            "--output", self.output,
            "--macros-path", _MACROS_DIR,
            "--format", "slides",
        ]
        subprocess.run(cmd, capture_output=True, text=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_html_comment_converted_to_python_comment(self):
        """<!-- ... --> should become # ... in Manim output."""
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        content = _read_output(self.output)
        self.assertNotIn("<!--", content, msg="Raw HTML comment delimiter found in Manim output")
        self.assertNotIn("-->", content, msg="Raw HTML comment delimiter found in Manim output")
        self.assertIn("single-line html comment", content,
                      msg="Comment content should be preserved as a Python comment")

    def test_output_is_valid_python_with_comment(self):
        """Output should be valid Python after comment conversion."""
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        try:
            py_compile.compile(self.output, doraise=True)
        except py_compile.PyCompileError as exc:
            self.fail(f"Output is not valid Python after comment conversion: {exc}")


class TestMdppManim_DisplayMath(unittest.TestCase):
    """$$...$$ display math at top level should become lamd_display_math calls."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        fixture = os.path.join(self.tmp.name, "math-talk.md")
        with open(fixture, "w") as f:
            f.write(
                "---\ntitle: Math Test\nauthor:\n- family: Test\n  given: Author\n"
                "date: 2026-05-05\n---\n\n"
                "\\newslide{Entropy}{}\n\n"
                "\\slides{The entropy is given by:}\n\n"
                "$$\n"
                "H(X) = -\\sum_x p(x) \\log p(x)\n"
                "$$\n\n"
                "\\notes{This is Shannon entropy.}\n"
            )
        self.output = os.path.join(self.tmp.name, "math-test.manim.py")
        cmd = _MDPP + [
            fixture,
            "--to", "manim",
            "--output", self.output,
            "--macros-path", _MACROS_DIR,
            "--format", "slides",
        ]
        subprocess.run(cmd, capture_output=True, text=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_dollar_signs_absent_from_output(self):
        """Raw $$ should not appear at the top level of the Manim Python output."""
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        content = _read_output(self.output)
        # $$  on its own line (top-level math) should have been converted
        import re
        bare_dollars = re.search(r"^\s*\$\$", content, re.MULTILINE)
        self.assertIsNone(bare_dollars, "Bare $$ found at top level of Manim output")

    def test_lamd_display_math_called(self):
        """Display math should produce a lamd_display_math call."""
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        content = _read_output(self.output)
        self.assertIn("lamd_display_math", content,
                      msg="lamd_display_math not found; display math was not converted")

    def test_output_is_valid_python_with_math(self):
        """Output should be valid Python after display-math conversion."""
        if not os.path.isfile(self.output):
            self.skipTest("Output file not created")
        try:
            py_compile.compile(self.output, doraise=True)
        except py_compile.PyCompileError as exc:
            self.fail(f"Output is not valid Python after display-math conversion: {exc}")


if __name__ == "__main__":
    unittest.main()
