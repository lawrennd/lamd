---
id: "2026-05-06_cip000d-svg-to-html"
title: "Write lamd/util/svg_to_html.py HTML generator"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
category: "features"
related_cips: ["000D"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- manim
- svg
- html
- revealjs
- cip-000d
---

# Task: Write lamd/util/svg_to_html.py

## Description

Write `lamd/util/svg_to_html.py` — the HTML generator that converts a directory of SVG animation frames (produced by `manim --renderer svg`) into a self-contained RevealJS presentation using the `js/manim-svg.js` plugin from the `lawrennd/manim` fork. This is Phase 3 of CIP-000D.

The script is invoked via `python -m lamd.util.svg_to_html` from the makefile.

## Acceptance Criteria

- [ ] Callable as `python -m lamd.util.svg_to_html <animation_root_dir> <output.html>` with optional `--title`, `--js-src`, `--theme` flags
- [ ] Scans `<animation_root_dir>/animation_*/animation.json` (sorted by animation index N)
- [ ] Produces one `<section data-manim-svg="<relative_path_to_animation_N>" data-manim-loop="false">` per animation directory
- [ ] Wraps sections in valid RevealJS 5 boilerplate (CDN links or local vendor, configurable)
- [ ] Inlines or links `js/manim-svg.js`; `--js-src` flag specifies the path to the plugin file
- [ ] Title slide (plain `<section>`) with `--title` text is prepended if `--title` is given
- [ ] Output HTML passes basic validation (well-formed, opens in browser without console errors)
- [ ] `--js-src` defaults to a sensible search path: first checks `$MANIMSVGJS` env var, then the installed `lawrennd/manim` package data, then the current directory

## Implementation Notes

Suggested structure:

```python
#!/usr/bin/env python3
"""Generate a RevealJS HTML presentation from manim SVG animation directories."""
import argparse, json, os, pathlib, shutil

REVEAL_CDN = "https://cdn.jsdelivr.net/npm/reveal.js@5"

def find_animations(root: pathlib.Path) -> list[pathlib.Path]:
    """Return animation_N dirs sorted by index N."""
    dirs = sorted(root.glob("animation_*/"), key=lambda p: int(p.name.split("_")[1]))
    return [d for d in dirs if (d / "animation.json").exists()]

def make_section(anim_dir: pathlib.Path, root: pathlib.Path) -> str:
    rel = anim_dir.relative_to(root.parent)
    return f'    <section data-manim-svg="{rel}" data-manim-loop="false"></section>'

def generate_html(root, output, title, js_src, theme="black") -> None:
    ...
```

The path passed to `data-manim-svg` must be relative to the output HTML file location so the browser can resolve it.

## Related

- CIP: 000D
- Backlog: 2026-05-06_cip000d-makefile (depends on this task)
- Backlog: 2026-05-06_cip000d-tests (tests this module)

## Progress Updates

### 2026-05-06
Task created with Proposed status.
