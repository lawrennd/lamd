---
id: "2026-08-08_cip0007-documentation"
title: "CIP-0007 Phase 5: Animation System Documentation"
status: "Proposed"
priority: "Low"
created: "2026-08-08"
last_updated: "2026-08-08"
category: "documentation"
related_cips: ["0007"]
owner: "Neil Lawrence"
dependencies: ["2026-08-08_cip0007-accessibility", "2026-08-08_cip0007-error-handling", "2026-08-08_cip0007-format-support"]
tags:
- backlog
- animation
- documentation
---

# Task: CIP-0007 Phase 5 — Animation System Documentation

## Description

Update `slides.md` and related documentation to cover the animation macro system in full: JavaScript dependencies, accessibility guidelines, format-specific behaviour, and troubleshooting.

## Acceptance Criteria

- [ ] `slides.md` documents `\startanimation`, `\newframe`, `\endanimation` with parameters and examples
- [ ] JavaScript dependency (`figure-animate.js`) and its required functions documented
- [ ] Accessibility guidelines (ARIA, keyboard nav) described for content authors
- [ ] Format-specific behaviour (HTML vs notes vs ipynb) explained
- [ ] Troubleshooting section covers common failure modes (missing JS, empty frames, etc.)
- [ ] At least one worked example of a complete animation sequence

## Implementation Notes

- Primary doc file: `docs/source/slides.md` (or equivalent Sphinx source)
- Reference the `figure-animate.js` source location
- Link to WCAG 2.1 for accessibility context

## Related

- CIP: 0007
- Documentation: cip/cip0007.md

## Progress Updates

### 2026-08-08

Task created — tracking Phase 5 of CIP-0007.
