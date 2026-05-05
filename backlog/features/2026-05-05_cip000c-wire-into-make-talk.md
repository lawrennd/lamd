---
id: "2026-05-05_cip000c-wire-into-make-talk"
title: "Wire make-manim.mk and make-video-manim.mk into make-talk.mk"
status: "Completed"
priority: "Medium"
created: "2026-05-05"
last_updated: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: ""
dependencies: ["2026-05-05_cip000c-make-manim-mk", "2026-05-05_cip000c-make-video-manim-mk"]
tags:
- backlog
- manim
- makefile
- cip-000c
---

# Task: Wire Manim makefiles into make-talk.mk

## Description

Add `include` directives to `lamd/makefiles/make-talk.mk` so that the `manim` and `manim-video` targets become available when building a talk. This is Phase 2 of CIP-000C.

## Acceptance Criteria

- [ ] `make-talk.mk` includes `$(MAKEFILESDIR)/make-manim.mk` (guarded so it only loads when the file exists, or unconditionally if consistent with project conventions)
- [ ] `make-talk.mk` includes `$(MAKEFILESDIR)/make-video-manim.mk`
- [ ] Running `make manim` in a talk directory produces `${BASE}.slides.html`
- [ ] Running `make manim-video` in a talk directory produces `${BASE}.video.mp4`
- [ ] Existing make targets (`make slides`, `make notes`, `make pptx`, etc.) are unaffected

## Implementation Notes

Follow the pattern of how other format-specific makefiles (e.g. `make-slides.mk`, `make-pptx.mk`) are included in `make-talk.mk`. A simple unconditional include is fine if the project convention is to always include all format makefiles.

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-make-manim-mk`, `2026-05-05_cip000c-make-video-manim-mk`

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 2.
