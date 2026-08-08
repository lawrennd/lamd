---
id: "2026-08-08_cip0007-format-support"
title: "CIP-0007 Phase 2: Improve Animation Format Support"
status: "Proposed"
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

- [ ] Notes format renders animation frames as static images or sequential content
- [ ] IPynb format renders animation frames as sequential cells
- [ ] No content is silently dropped in any format
- [ ] Consistent behaviour documented in format-specific notes

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
