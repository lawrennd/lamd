---
id: "2026-09-15_cip0012-includescript-macro"
title: "CIP-0012 Track A: includescript macro for multi-format HTML"
status: "Completed"
priority: "High"
created: "2026-09-15"
last_updated: "2026-09-15"
category: "features"
related_cips: ["0012"]
owner: "Neil Lawrence"
dependencies:
- "2026-09-15_cip0012-inventory-test-suite"
tags:
- backlog
- cip0012
- javascript
- macros
- html
---

# Task: CIP-0012 Track A — `\includescript{relpath}`

## Description

Add `\includescript{relpath}` that emits a once-guarded `<script src="\scriptsDir/\relpath">` in **all HTML-emitting** macro sets that carry interactive content (slides-html, notes-html, ipynb HTML as applicable). No-op in TeX / PDF / PPTX / docx / Manim. Extend inventory-derived unit tests; add a migration golden (legacy include vs `\includescript` same `src` set).

## Acceptance Criteria

- [ ] Macro defined with path-safe once-guards
- [ ] Expands in slides-html and notes-html (and other agreed HTML formats)
- [ ] No script tags in tex/pptx/docx/manim macro expansions
- [ ] Inventory baselines still pass for unmigrated raw `<script>` snippets
- [ ] Twin fixture: legacy vs `\includescript` produce the same script `src` set
- [ ] Unit tests green

## Implementation Notes

Track A must not be slides-only — that was the original CIP mistake. Exact HTML macro file list fixed during implementation from Stage 0 format-reach notes.

## Related

- CIP: 0012
- Depends on: `2026-09-15_cip0012-inventory-test-suite`
- Parallel with: `2026-09-15_cip0012-slide-setup-include-after`

## Progress Updates

### 2026-09-15

Task created (Ready) when CIP-0012 Accepted.

### 2026-09-15 (implementation)

Completed as part of CIP-0012 implementation.
