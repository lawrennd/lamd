---
id: "2026-09-15_cip0012-compress-slides-docs"
title: "CIP-0012: Compress JS tracks into slides.md docs"
status: "Proposed"
priority: "Low"
created: "2026-09-15"
last_updated: "2026-09-15"
category: "documentation"
related_cips: ["0012"]
owner: "Neil Lawrence"
dependencies:
- "2026-09-15_cip0012-backgrounds-and-migration"
tags:
- backlog
- cip0012
- documentation
- compression
---

# Task: CIP-0012 — Compress into `docs/contexts/slides.md`

## Description

After CIP-0012 is Closed (implementation validated), compress durable guidance into `docs/contexts/slides.md`: Track A vs B, `\includescript`, `slide_setup` lifecycle, background attributes, `background:` pitfall, inventory examples. Set `compressed: true` on the CIP.

## Acceptance Criteria

- [ ] CIP-0012 status Closed and validated
- [ ] `docs/contexts/slides.md` updated with Track A/B and authoring tables
- [ ] Links to example setup / includescript usage
- [ ] CIP frontmatter `compressed: true`

## Implementation Notes

Do not duplicate the full CIP; distill current behaviour only (documentation lifecycle tenet).

## Related

- CIP: 0012
- Docs: `docs/contexts/slides.md`

## Progress Updates

### 2026-09-15

Task created (Proposed) for post-close compression when CIP-0012 Accepted.
