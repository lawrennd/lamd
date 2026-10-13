---
id: "2026-10-13_cip0014-compress-slides-docs"
title: "CIP-0014: Compress font-size guidance into slides.md"
status: "Proposed"
priority: "Medium"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "documentation"
related_cips: ["0014"]
owner: "Neil Lawrence"
dependencies:
- "2026-10-13_cip0014-talkfontsize-flags"
- "2026-10-13_cip0014-slidefont-macros"
tags:
- backlog
- cip0014
- documentation
- slides
- typography
---

# Task: CIP-0014 — compress typography docs into `slides.md`

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

After CIP-0014 implementation is validated and the CIP is Closed, compress durable guidance into `docs/contexts/slides.md`: `talkfontsize`, class table, precedence vs deck default, HTML-only note, and optional `\slidefont`. Set `compressed: true` on the CIP.

## Acceptance Criteria

- [ ] `docs/contexts/slides.md` has a Typography subsection covering deck + per-slide API
- [ ] Documents five tokens, aliases, and precedence (per-slide > deck > default)
- [ ] Notes Reveal-HTML-only (notes / PPTX no-op for v1)
- [ ] CIP-0014 `compressed: true` after docs land

## Implementation Notes

Land on Close (documentation lifecycle Phase 4), not during initial implementation. Mirror the CIP-0012 Track B documentation style.

## Related

- CIP: 0014
- Documentation: `docs/contexts/slides.md`

## Progress Updates

### 2026-10-13

Task created (Proposed) when CIP-0014 Accepted; execute after Close / validation.
