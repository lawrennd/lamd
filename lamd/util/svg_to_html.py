"""Generate a RevealJS HTML presentation from manim SVG animation directories.

Each ``animation_N/`` subdirectory produced by ``manim --renderer svg``
becomes one RevealJS ``<section data-manim-svg="...">`` slide.  The
``js/manim-svg.js`` plugin from the lawrennd/manim fork is included as a
``<script>`` tag and plays back the per-frame SVGs by cycling them on the
RevealJS slide-background layer.

Usage (CLI)::

    python -m lamd.util.svg_to_html media/svg/Talk mytalk.manim-svg.html \\
        --title "My Talk" --js-src /path/to/js/manim-svg.js

Usage (API)::

    from lamd.util.svg_to_html import generate_html
    generate_html(
        animation_root=pathlib.Path("media/svg/Talk"),
        output_path=pathlib.Path("mytalk.manim-svg.html"),
        title="My Talk",
        js_src=pathlib.Path("js/manim-svg.js"),
    )
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import sys
from typing import Optional

REVEAL_CDN = "https://cdn.jsdelivr.net/npm/reveal.js@5"

_HTML_TEMPLATE = """\
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="{reveal_cdn}/dist/reveal.css" />
  <link rel="stylesheet" href="{reveal_cdn}/dist/theme/black.css" />
</head>
<body>
<div class="reveal">
  <div class="slides">
{title_slide}{sections}
  </div>
</div>
<script src="{reveal_cdn}/dist/reveal.js"></script>
<script src="{js_src_ref}"></script>
<script>
  Reveal.initialize({{
    hash: true,
    plugins: [ManimSVG],
  }});
</script>
</body>
</html>
"""

_TITLE_SECTION = """\
    <section>
      <h2>{title}</h2>
    </section>
"""

_ANIM_SECTION = """\
    <section data-manim-svg="{rel_path}" data-manim-loop="false"></section>"""


def find_animations(root: pathlib.Path) -> list[pathlib.Path]:
    """Return animation_N directories sorted by animation index N."""
    dirs = sorted(
        root.glob("animation_*/"),
        key=lambda p: int(p.name.split("_")[1]),
    )
    return [d for d in dirs if (d / "animation.json").exists()]


def _relative_path(anim_dir: pathlib.Path, output_path: pathlib.Path) -> str:
    """Return a path to *anim_dir* relative to *output_path*'s parent directory."""
    try:
        return str(anim_dir.resolve().relative_to(output_path.resolve().parent))
    except ValueError:
        return str(anim_dir.resolve())


def _locate_js_plugin(js_src: Optional[pathlib.Path]) -> Optional[pathlib.Path]:
    """Resolve the path to manim-svg.js, trying several fallback locations."""
    if js_src is not None and js_src.is_file():
        return js_src

    # Environment variable override.
    env_path = os.environ.get("MANIMSVGJS")
    if env_path and pathlib.Path(env_path).is_file():
        return pathlib.Path(env_path)

    # Installed lawrennd/manim package: look for js/manim-svg.js alongside it.
    try:
        import manim as _manim  # type: ignore[import]

        candidate = pathlib.Path(_manim.__file__).parent.parent / "js" / "manim-svg.js"
        if candidate.is_file():
            return candidate
    except ImportError:
        pass

    # Current working directory.
    cwd_candidate = pathlib.Path("js") / "manim-svg.js"
    if cwd_candidate.is_file():
        return cwd_candidate

    return None


def generate_html(
    animation_root: pathlib.Path,
    output_path: pathlib.Path,
    title: str = "",
    js_src: Optional[pathlib.Path] = None,
    theme: str = "black",
    reveal_cdn: str = REVEAL_CDN,
) -> None:
    """Generate a RevealJS HTML file from an animation root directory.

    Args:
        animation_root: Directory containing ``animation_N/`` subdirectories.
        output_path: Destination ``.html`` file.
        title: Presentation title (shown as a leading title slide if non-empty).
        js_src: Path to ``manim-svg.js``; auto-detected if *None*.
        theme: RevealJS theme name (default: ``"black"``).
        reveal_cdn: Base URL for RevealJS CDN assets.
    """
    anims = find_animations(animation_root)
    if not anims:
        raise FileNotFoundError(
            f"No animation directories found under {animation_root!r}. " "Run 'manim --renderer svg' first."
        )

    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Resolve JS plugin.
    resolved_js = _locate_js_plugin(js_src)
    if resolved_js is None:
        raise FileNotFoundError("Cannot find manim-svg.js. Install lawrennd/manim or set --js-src.")

    # Copy the plugin alongside the output HTML so it can be served locally.
    js_dest = output_path.parent / "manim-svg.js"
    if resolved_js.resolve() != js_dest.resolve():
        shutil.copy2(resolved_js, js_dest)
    js_src_ref = "manim-svg.js"

    # Build section list.
    sections = "\n".join(_ANIM_SECTION.format(rel_path=_relative_path(d, output_path)) for d in anims)

    title_slide = _TITLE_SECTION.format(title=title) if title else ""

    html = _HTML_TEMPLATE.format(
        title=title or "Manim SVG Presentation",
        reveal_cdn=reveal_cdn.rstrip("/").replace("/dist/theme/black.css", "").rstrip("/"),
        title_slide=title_slide,
        sections=sections,
        js_src_ref=js_src_ref,
    )

    # Fix the CDN paths — the template uses a single base variable.
    cdn_base = reveal_cdn.rstrip("/")
    html = html.replace(f"{cdn_base}/dist/reveal.css", f"{cdn_base}/dist/reveal.css")

    output_path.write_text(html, encoding="utf-8")
    print(f"Written: {output_path}  ({len(anims)} animation(s))")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a RevealJS HTML presentation from manim SVG animation directories.",
    )
    parser.add_argument(
        "animation_root",
        type=pathlib.Path,
        help="Root directory containing animation_N/ subdirectories (e.g. media/svg/Talk).",
    )
    parser.add_argument(
        "output",
        type=pathlib.Path,
        help="Output HTML file path.",
    )
    parser.add_argument(
        "--title",
        default="",
        help="Presentation title (added as a leading title slide).",
    )
    parser.add_argument(
        "--js-src",
        type=pathlib.Path,
        default=None,
        dest="js_src",
        help="Path to manim-svg.js (auto-detected if omitted).",
    )
    parser.add_argument(
        "--theme",
        default="black",
        help="RevealJS theme name (default: black).",
    )
    parser.add_argument(
        "--reveal-cdn",
        default=REVEAL_CDN,
        dest="reveal_cdn",
        help=f"RevealJS CDN base URL (default: {REVEAL_CDN}).",
    )

    args = parser.parse_args(argv)

    try:
        generate_html(
            animation_root=args.animation_root,
            output_path=args.output,
            title=args.title,
            js_src=args.js_src,
            theme=args.theme,
            reveal_cdn=args.reveal_cdn,
        )
        return 0
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
