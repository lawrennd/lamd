"""Unit tests for lamd.util.svg_to_html.

Tests exercise the public API (generate_html) with synthetic animation
directories, checking that the output HTML has the correct structure without
requiring a real manim installation or a live manim-svg.js file.
"""

import json
import pathlib
import shutil
import tempfile
import unittest


def _make_fake_anim_dir(root: pathlib.Path, index: int, frame_count: int = 3) -> pathlib.Path:
    """Create a fake animation_N/ directory with an animation.json and stub SVG files."""
    anim = root / f"animation_{index}"
    anim.mkdir(parents=True, exist_ok=True)
    manifest = {
        "fps": 15,
        "frame_count": frame_count,
        "width": 1920,
        "height": 1080,
    }
    (anim / "animation.json").write_text(json.dumps(manifest))
    for i in range(frame_count):
        (anim / f"frame_{i:04d}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg"><text>frame {i}</text></svg>')
    return anim


def _make_fake_js(path: pathlib.Path) -> pathlib.Path:
    """Write a minimal stub for manim-svg.js."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("/* stub manim-svg.js */\nvar ManimSVG = {};")
    return path


class TestFindAnimations(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_finds_animation_dirs_in_order(self):
        from lamd.util.svg_to_html import find_animations

        _make_fake_anim_dir(self.tmp, 2)
        _make_fake_anim_dir(self.tmp, 0)
        _make_fake_anim_dir(self.tmp, 1)
        dirs = find_animations(self.tmp)
        self.assertEqual([d.name for d in dirs], ["animation_0", "animation_1", "animation_2"])

    def test_ignores_dirs_without_manifest(self):
        from lamd.util.svg_to_html import find_animations

        _make_fake_anim_dir(self.tmp, 0)
        (self.tmp / "animation_1").mkdir()  # no animation.json
        dirs = find_animations(self.tmp)
        self.assertEqual(len(dirs), 1)

    def test_returns_empty_for_empty_root(self):
        from lamd.util.svg_to_html import find_animations

        dirs = find_animations(self.tmp)
        self.assertEqual(dirs, [])


class TestGenerateHtml(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.anim_root = self.tmp / "media" / "svg" / "Talk"
        self.js_src = self.tmp / "js" / "manim-svg.js"
        _make_fake_anim_dir(self.anim_root, 0, frame_count=4)
        _make_fake_anim_dir(self.anim_root, 1, frame_count=2)
        _make_fake_js(self.js_src)
        self.output = self.tmp / "out" / "talk.html"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _run(self, **kwargs):
        from lamd.util.svg_to_html import generate_html

        generate_html(
            animation_root=self.anim_root,
            output_path=self.output,
            js_src=self.js_src,
            **kwargs,
        )
        return self.output.read_text()

    def test_output_file_created(self):
        self._run()
        self.assertTrue(self.output.exists())

    def test_html_has_reveal_structure(self):
        html = self._run()
        self.assertIn('<div class="reveal">', html)
        self.assertIn('<div class="slides">', html)

    def test_data_manim_svg_attributes_present(self):
        html = self._run()
        self.assertIn("data-manim-svg=", html)
        # One section per animation directory.
        self.assertEqual(html.count("data-manim-svg="), 2)

    def test_title_slide_included_when_title_given(self):
        html = self._run(title="Test Talk")
        self.assertIn("Test Talk", html)

    def test_no_title_slide_when_empty(self):
        html = self._run(title="")
        self.assertNotIn("<h2></h2>", html)

    def test_js_plugin_copied_alongside_output(self):
        self._run()
        self.assertTrue((self.output.parent / "manim-svg.js").exists())

    def test_raises_if_no_animation_dirs(self):
        from lamd.util.svg_to_html import generate_html

        empty_root = self.tmp / "empty"
        empty_root.mkdir()
        with self.assertRaises(FileNotFoundError):
            generate_html(
                animation_root=empty_root,
                output_path=self.output,
                js_src=self.js_src,
            )


class TestMainCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.anim_root = self.tmp / "anims"
        self.js_src = self.tmp / "manim-svg.js"
        _make_fake_anim_dir(self.anim_root, 0)
        _make_fake_js(self.js_src)
        self.output = self.tmp / "talk.html"

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_cli_exit_code_zero(self):
        from lamd.util.svg_to_html import main

        rc = main([str(self.anim_root), str(self.output), "--js-src", str(self.js_src), "--title", "CLI Test"])
        self.assertEqual(rc, 0)
        self.assertTrue(self.output.exists())

    def test_cli_exit_code_one_on_missing_root(self):
        from lamd.util.svg_to_html import main

        rc = main([str(self.tmp / "nonexistent"), str(self.output), "--js-src", str(self.js_src)])
        self.assertEqual(rc, 1)
