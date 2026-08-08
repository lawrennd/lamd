---
id: "2026-08-08_cip0007-accessibility"
title: "CIP-0007 Phase 3: Improve Animation Accessibility"
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
- accessibility
- aria
---

# Task: CIP-0007 Phase 3 — Improve Animation Accessibility

## Description

Enhance the HTML animation controls with proper ARIA labels, roles, and keyboard navigation support to meet accessibility requirements (REQ-0004).

## Acceptance Criteria

- [x] Range slider has `aria-label` and `aria-valuemin`/`aria-valuemax`/`aria-valuenow` attributes
- [x] Navigation buttons have descriptive `aria-label` values ("Previous frame" / "Next frame")
- [x] Keyboard navigation works for all animation controls (Tab, Arrow keys — native for `<input type="range">` and `<button>`)
- [x] Animation container has `role="region"` and `aria-label` attributes
- [x] Each frame div has `role="img"` and `aria-label` for screen readers

## Implementation Notes

- Edit `\startanimation` macro in `talk-macros-slides-html.gpp`
- Test with VoiceOver (macOS) and axe browser extension
- Follow WCAG 2.1 AA as the baseline

## Related

- CIP: 0007
- Documentation: cip/cip0007.md

## Progress Updates

### 2026-08-08

Task created — tracking Phase 3 of CIP-0007.

Task completed. Changes:
- `talk-macros-slides-html.gpp`: `\startanimation` container now has `role="region"` and `aria-label="\name"`.
- `talk-macros-slides-html.gpp`: range slider now has `aria-label`, `aria-valuemin`, `aria-valuemax`, `aria-valuenow`.
- `talk-macros-slides-html.gpp`: navigation buttons now have `aria-label="Previous frame"` / `aria-label="Next frame"`.
- `talk-macros-slides-html.gpp`: `\newframe` divs now have `role="img"` and `aria-label="\name"`.
- `tests/unit/test_animation_macros.py`: added `TestAnimationAccessibility` with 8 new tests covering all ARIA changes.
