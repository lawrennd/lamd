---
id: "2026-05-06_cip000d-mdpp-to-manim-svg"
title: "Add --to manim-svg to mdpp.py"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
category: "features"
related_cips: ["000D"]
owner: "Neil Lawrence"
dependencies: ["2026-05-06_cip000d-svg-manim-gpp"]
tags:
- backlog
- manim
- svg
- mdpp
- cip-000d
---

# Task: Add --to manim-svg to mdpp.py

## Description

Add `manim-svg` as a valid `--to` choice in `mdpp.py` and implement the corresponding header injection and GPP flag setup. This is Phase 2 of CIP-000D.

The pattern mirrors the existing `--to manim` implementation (CIP-000C). The differences are:

1. The Python header uses `Scene` (not `Slide`) and sets `config.renderer = RendererType.SVG`
2. The GPP flags load `talk-macros-slides-svg-manim.gpp` instead of `talk-macros-slides-manim.gpp`
3. The output file extension is `.manim-svg.py`

## Acceptance Criteria

- [ ] `mdpp.py --to manim-svg` is a valid invocation (no `argparse` error)
- [ ] Output file header contains `from manim import *`, `from manim.constants import RendererType`, `config.renderer = RendererType.SVG`, `class Talk(Scene):`, `    def construct(self):`
- [ ] GPP is invoked with `-DMANIM=1 -DSLIDES=1` (reusing existing guards) and loads `talk-macros-slides-svg-manim.gpp`
- [ ] `_lamd_manim.py` helper is copied to the output directory (same as `--to manim`)
- [ ] `mdpp.py --to manim-svg` on a minimal fixture talk produces a `.py` file that passes `python -m py_compile`
- [ ] Existing `--to manim` and `--to manim-video` behaviour is unchanged

## Implementation Notes

Find the section in `mdpp.py` where `_MANIM_SLIDES_HEADER` is defined and used. Add a parallel constant `_MANIM_SVG_HEADER`:

```python
_MANIM_SVG_HEADER = """\
from manim import *
from manim.constants import RendererType

config.renderer = RendererType.SVG

class Talk(Scene):
    def construct(self):
"""
```

In the `--to` dispatch block, handle `"manim-svg"` similarly to `"manim"` but use `_MANIM_SVG_HEADER` and the new GPP macro file.

## Related

- CIP: 000D
- Backlog: 2026-05-06_cip000d-svg-manim-gpp (dependency)
- Backlog: 2026-05-06_cip000d-makefile (depends on this task)

## Progress Updates

### 2026-05-06
Task created with Proposed status.
