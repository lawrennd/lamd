---
id: "2026-05-06_cip000d-svg-manim-gpp"
title: "Create talk-macros-slides-svg-manim.gpp for SVG manim pipeline"
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
- macros
- cip-000d
---

# Task: Create talk-macros-slides-svg-manim.gpp

## Description

Create `lamd/macros/talk-macros-slides-svg-manim.gpp` — the GPP macro file for the `--to manim-svg` output format. This is Phase 1 of CIP-000D.

The file is intentionally thin. The shared `talk-macros-manim.gpp` already provides `\slides{}`, `\notes{}`, `\speakernotes{}`, `\slidesincremental{}`, `\fragment{}`, `\displaymath{}`, `\includediagram{}`, `\includeimg{}`, and `\slidesmanim{}`. This file only needs to define the slide-boundary macros that differ from CIP-000C's slides path.

The key difference from `talk-macros-slides-manim.gpp`: there is no `self.next_slide()` call, because the SVG pipeline uses a standard `Scene` (not a `manim-slides` `Slide`). Each `self.play()` call produces one `animation_N/` directory; the HTML generator creates one RevealJS slide per animation.

## Acceptance Criteria

- [ ] `\newslide{title}` → `self.play(FadeIn(lamd_text(r"""<title>""")))` with **no** `self.next_slide()` call
- [ ] `\section{title}`, `\subsection{title}`, `\subsubsection{title}` → same pattern as `\newslide`
- [ ] `\slidesincremental{items}` → `self.play(FadeIn(lamd_text(r"""<items>""")))` with no `self.next_slide()`
- [ ] File is guarded with `\ifndef{talkMacrosSlidessvgManim}` / `\define` / `\endif`
- [ ] Pattern matches `talk-macros-slides-manim.gpp` (same guard convention, same indentation style)
- [ ] `talk-macros-manim.gpp` is NOT duplicated — only overriding macros appear here

## Implementation Notes

Reference: [`lamd/macros/talk-macros-slides-manim.gpp`](../../lamd/macros/talk-macros-slides-manim.gpp) — copy and remove all `self.next_slide()` calls.

The macro file is loaded by `mdpp.py` when `--to manim-svg` is specified, after the shared `talk-macros-manim.gpp` is loaded. Macros defined here override those in the shared file.

## Related

- CIP: 000D
- Backlog: 2026-05-06_cip000d-mdpp-to-manim-svg (depends on this task)

## Progress Updates

### 2026-05-06
Task created with Proposed status.
