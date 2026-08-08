---
id: "2026-08-08_cip0007-format-support"
title: "CIP-0007 Phase 2: Improve Animation Format Support"
status: "Completed"
priority: "Medium"
created: "2026-08-08"
last_updated: "2026-08-08"
category: "features"
related_cips: ["0007"]
owner: "Neil Lawrence"
dependencies: ["2026-08-08_cip0007-fix-animation-macros"]
tags:
- backlog
- animation
- macros
- notes
- ipynb
---

# Task: CIP-0007 Phase 2 — Improve Animation Format Support

## Description

Add fallback implementations for animation macros in non-HTML output formats (notes, ipynb), ensuring graceful degradation so that content is not lost when animations cannot be rendered interactively.

## Acceptance Criteria

- [x] Notes format renders animation frames as static images or sequential content
- [x] IPynb format renders animation frames as sequential cells
- [x] No content is silently dropped in any format (all `\newframe` bodies pass through `\contents`)
- [x] TEX and PPTX fallbacks added explicitly (previously inherited null definitions silently)
- [x] Tests added for all Phase 2 formats in `tests/unit/test_animation_macros.py`

## Implementation Notes

- Edit the notes and ipynb macro files (`talk-macros-notes.gpp`, `talk-macros-ipynb.gpp`)
- For notes: render each `\newframe` as a paragraph/figure without the slider JS
- For ipynb: render each frame as a markdown cell

## Related

- CIP: 0007
- Documentation: cip/cip0007.md

## Progress Updates

### 2026-08-08

Task created — tracking Phase 2 of CIP-0007.

Task completed. Changes:
- `talk-macros-notes.gpp`: improved `\startanimation` label and added blank-line separators between frames.
- `talk-macros-slides-ipynb.gpp`: simplified to pass content sequentially with blank-line separators (removed heading markers that created sub-slides).
- `talk-macros-slides-tex.gpp`: added explicit `\startanimation` / `\newframe` / `\endanimation` fallbacks.
- `talk-macros-slides-pptx.gpp`: added explicit fallbacks.
- `tests/unit/test_animation_macros.py`: extended with `TestAnimationMacrosFallbacks` covering all Phase 2 formats.
