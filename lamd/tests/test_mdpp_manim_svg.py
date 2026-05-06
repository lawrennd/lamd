"""Smoke tests for mdpp --to manim-svg.

Checks that:
  * the process exits with code 0
  * the output file is syntactically valid Python
  * the header sets config.renderer = RendererType.SVG
  * the header uses Scene (not Slide or manim_slides)
  * no next_slide() calls appear in the output

No Manim installation is required.
"""
import os
import py_compile
import subprocess
import sys
import tempfile
import unittest

_MDPP = [sys.executable, "-m", "lamd.mdpp"]
_MACROS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "macros")
_FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "minimal-manim-talk.md")


def _run_mdpp(output_path: str) -> subprocess.CompletedProcess:
    cmd = _MDPP + [
        _FIXTURE,
        "--to", "manim-svg",
        "--output", output_path,
        "--macros-path", _MACROS_DIR,
        "--format", "slides",
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def _read_output(path: str) -> str:
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()
    return ""


class TestMdppManim_SVG(unittest.TestCase):
    """Smoke-test mdpp --to manim-svg output."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.output = os.path.join(self.tmp.name, "talk.manim-svg.py")

    def tearDown(self):
        self.tmp.cleanup()

    def test_exit_code_zero(self):
        result = _run_mdpp(self.output)
        self.assertEqual(
            result.returncode, 0,
            msg=f"mdpp --to manim-svg exited {result.returncode}.\n"
                f"stdout: {result.stdout}\nstderr: {result.stderr}",
        )

    def test_output_file_created(self):
        _run_mdpp(self.output)
        self.assertTrue(os.path.isfile(self.output))

    def test_output_is_valid_python(self):
        result = _run_mdpp(self.output)
        if result.returncode != 0:
            self.skipTest("mdpp failed; skipping syntax check")
        try:
            py_compile.compile(self.output, doraise=True)
        except py_compile.PyCompileError as exc:
            self.fail(f"Output is not valid Python: {exc}")

    def test_uses_scene_not_slide(self):
        _run_mdpp(self.output)
        content = _read_output(self.output)
        self.assertIn("class Talk(Scene):", content)
        self.assertNotIn("manim_slides", content)
        self.assertNotIn("class Talk(Slide)", content)

    def test_sets_renderer_to_svg(self):
        _run_mdpp(self.output)
        content = _read_output(self.output)
        self.assertIn("RendererType.SVG", content)
        self.assertIn("config.renderer", content)

    def test_no_next_slide_calls(self):
        _run_mdpp(self.output)
        content = _read_output(self.output)
        self.assertNotIn("next_slide()", content)

    def test_has_construct_method(self):
        _run_mdpp(self.output)
        content = _read_output(self.output)
        self.assertIn("def construct(self):", content)
