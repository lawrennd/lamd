---
id: "2026-05-05_cip000c-manim-gpp-skeleton"
title: "Create talk-macros-slides-manim.gpp skeleton"
status: "Completed"
priority: "High"
created: "2026-05-05"
last_updated: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: ""
dependencies: []
tags:
- backlog
- manim
- macros
- cip-000c
---

# Task: Create talk-macros-slides-manim.gpp skeleton

## Description

Create `lamd/macros/talk-macros-slides-manim.gpp` — the gpp macro file for the `--to manim` (manim-slides) output format. This is the first Phase 1 task for CIP-000C.

The file defines how LaMD macros are translated into `manim-slides` Python code. The whole talk becomes a single `Talk(Slide)` class; `self.next_slide()` marks slide boundaries.

## Acceptance Criteria

- [ ] `\newslide{title}` → `self.next_slide()` + wipe + title rendering via `lamd_text`
- [ ] `\slides{text}` → `self.play(FadeIn(lamd_text(r"text")))`
- [ ] `\notes{text}` → no-op (empty expansion)
- [ ] `\speakernotes{text}` → `notes=r"text"` argument on the preceding `self.next_slide(...)` call
- [ ] File generates a syntactically valid Python file (boilerplate header + class + `construct()`) when run through gpp on a minimal talk
- [ ] No-op macros added for `\slidesmanim{code}` (empty in this file; full definition added in Phase 2)

## Implementation Notes

Follow the pattern of `lamd/macros/talk-macros-slides-html.gpp` for the file structure. The generated Python header should be:

```python
from manim import *
from manim_slides import Slide
from _lamd_manim import lamd_text, lamd_display_math

class Talk(Slide):
    def construct(self):
```

The `\speakernotes` macro needs to emit `notes=r"..."` as an argument — this requires that `\newslide` defers its `self.next_slide()` call until after `\speakernotes` has been seen, or that `\speakernotes` is emitted inline in the `next_slide()` call immediately following the slide content. The simplest approach: `\speakernotes{text}` emits `        # speakernotes: text` as a comment in Phase 1; a proper `notes=` argument can be wired in Phase 3.

## Related

- CIP: 000C
- Depends on: none

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 1.

### 2026-05-05 (implementation)

Created `lamd/macros/talk-macros-slides-manim.gpp` with macro translations for `\slides`, `\notes`, `\speakernotes`, `\newslide`, `\slidesincremental`, `\slidesmanim`, and assorted no-op utility macros. Also created `lamd/macros/talk-macros-video-manim.gpp` for the `--to manim-video` pipeline (uses `self.wait()` instead of `self.next_slide()`). Updated `talk-macros.gpp` to include both files under `\ifdef{MANIM}` and `\ifdef{MANIM_VIDEO}` guards, following the same pattern as all other format-specific macro files.
