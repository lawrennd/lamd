---
id: "2026-08-08_cip0007-accessibility"
title: "CIP-0007 Phase 3: Improve Animation Accessibility"
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
- accessibility
- aria
---

# Task: CIP-0007 Phase 3 — Improve Animation Accessibility

## Description

Enhance the HTML animation controls with proper ARIA labels, roles, and keyboard navigation support to meet accessibility requirements (REQ-0004).

## Acceptance Criteria

- [ ] Range slider has `aria-label` and `aria-valuetext` attributes
- [ ] Navigation buttons have descriptive `aria-label` values
- [ ] Keyboard navigation works for all animation controls (Tab, Arrow keys)
- [ ] Animation container has appropriate `role` attribute
- [ ] Screen-reader-only text provided where controls are icon-only

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
