---
id: "2026-08-08_cip0007-error-handling"
title: "CIP-0007 Phase 4: Animation Error Handling and JS Fallback"
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
- javascript
- error-handling
---

# Task: CIP-0007 Phase 4 — Animation Error Handling and JS Fallback

## Description

Add JavaScript error detection and a graceful fallback when `figure-animate.js` is missing or fails to load, and improve the HTML container structure for better programmatic control.

## Acceptance Criteria

- [ ] Animation controls degrade gracefully when JS is unavailable (shows first frame, hides controls)
- [ ] Console warning emitted when `figure-animate.js` fails to load
- [ ] Animation container `<div>` has a stable CSS class/id for external styling and testing
- [ ] No JS errors thrown in console during normal operation

## Implementation Notes

- Add an inline `<noscript>` fallback inside `\startanimation` HTML output
- Wrap JS initialisation in a `try/catch` block
- Use `data-animation-group` attribute on the container for stable targeting

## Related

- CIP: 0007
- Documentation: cip/cip0007.md

## Progress Updates

### 2026-08-08

Task created — tracking Phase 4 of CIP-0007.
