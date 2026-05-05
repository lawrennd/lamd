"""Smoke tests for mdpp --to manim / --to manim-video.

These tests run mdpp as a subprocess on a minimal fixture and check that:
  * the process exits with code 0
  * the output file passes py_compile (i.e. is syntactically valid Python)

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


if __name__ == "__main__":
    unittest.main()
