---
id: "2026-08-08_cip0007-fix-animation-macros"
title: "CIP-0007 Phase 1: Fix Critical Animation Macro Bugs"
status: "Completed"
priority: "High"
created: "2026-08-08"
last_updated: "2026-08-08"
completed: "2026-08-08"
category: "bugs"
related_cips: ["0007"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- animation
- macros
- html
---

# Task: CIP-0007 Phase 1 — Fix Critical Animation Macro Bugs

## Description

Fix the two critical bugs in the animation macro system identified in CIP-0007:
1. Duplicate `\newframe` definition in `talk-macros-slides-html.gpp` (second overrides first, breaking slide creation)
2. Missing `\endanimation` implementation for HTML slides

## Acceptance Criteria

- [x] Duplicate `\newframe` definition removed from `talk-macros-slides-html.gpp`
- [x] `\endanimation` macro implemented for HTML slides (closes animation container)
- [x] Existing animation sequences render correctly in HTML output
- [x] Tests confirm both fixes and prevent regression

## Implementation Notes

- File to edit: `lamd/macros/talk-macros-slides-html.gpp`
- Keep the second (non-`\newslide`) `\newframe` definition; remove the first
- `\endanimation` for HTML can simply close the wrapping `<div>` container

## Related

- CIP: 0007
- Documentation: cip/cip0007.md

## Progress Updates

### 2026-08-08

Task created — tracking Phase 1 of CIP-0007.

Task completed:
- Removed duplicate `\newframe` definition from `talk-macros-slides-html.gpp` (first definition with `\newslide{}` was overridden by the second and never used — removing it makes the intent clear)
- `\endanimation` was already correctly implemented (`</div>`)
- Added 5 regression tests in `tests/unit/test_animation_macros.py`
