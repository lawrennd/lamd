---
id: "2026-05-05_cip000c-video-manim-gpp"
title: "Create talk-macros-video-manim.gpp for linear MP4 pipeline"
status: "Completed"
priority: "High"
created: "2026-05-05"
last_updated: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: "Neil Lawrence"
dependencies: ["2026-05-05_cip000c-manim-gpp-skeleton"]
tags:
- backlog
- manim
- macros
- cip-000c
---

# Task: Create talk-macros-video-manim.gpp

## Description

Create `lamd/macros/talk-macros-video-manim.gpp` — the gpp macro file for the `--to manim-video` output format. This produces a single linear Manim `Scene` with no slide breaks, suitable for raw `manim` rendering to a continuous MP4 file. This is Phase 2 of CIP-000C.

## Acceptance Criteria

- [ ] `\newslide{title}` → title rendering via `lamd_text` but **no** `self.next_slide()` call (slides run continuously)
- [ ] `\slides{text}` → `self.play(FadeIn(lamd_text(r"text")))` (same as slides-manim)
- [ ] `\notes{text}` → no-op
- [ ] `\speakernotes{text}` → no-op
- [ ] `\slidesmanim{code}` → verbatim passthrough (same as slides-manim)
- [ ] `\slidesincremental{items}` → each bullet rendered sequentially with `self.play(FadeIn(...))`, all bullets remain visible (no wipe between bullets)
- [ ] Generated class is `class Talk(Scene):` (not `Slide`) so that raw `manim` command is used
- [ ] Boilerplate header uses `from manim import *` only (no `from manim_slides import Slide`)

## Implementation Notes

The key difference from `talk-macros-slides-manim.gpp` is:
1. Class inherits from `Scene` not `Slide`
2. No `self.next_slide()` calls anywhere — everything plays sequentially
3. `\speakernotes` is a no-op (presenter notes are not meaningful in a video)

This allows the generated file to be rendered with:
```bash
manim talk.video.manim.py Talk -o talk.video.mp4
```

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-manim-gpp-skeleton` (for structural reference)

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 2.
