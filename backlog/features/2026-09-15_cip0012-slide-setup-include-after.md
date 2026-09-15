---
id: "2026-09-15_cip0012-slide-setup-include-after"
title: "CIP-0012 Track B: slide_setup and include-after-body"
status: "Ready"
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
- revealjs
- slides
- javascript
---

# Task: CIP-0012 Track B — `slide_setup` + include-after / Mermaid hygiene

## Description

Wire frontmatter/topic `slide_setup` through field extraction and `make-slides.mk` to pandoc `--include-after-body` (only when set). Confirm template `$include-after$` runs after `Reveal.initialize`. Fix Mermaid’s Reveal `ready` listener so it does not run before Reveal is loaded.

Reference ambient setup must implement CIP-0012 §B3 clash policy: on `ready` / `slidechanged`, if the current slide has per-slide `data-background*`, hide and pause ambient; otherwise show and run it.

## Acceptance Criteria

- [ ] `slide_setup` extracted alongside `slidesheader` in make/mdfield batch
- [ ] `make-slides.mk` passes `--include-after-body` only when `slide_setup` is set (no empty file)
- [ ] Path resolution consistent with `slidesheader` / `INCLUDESDIR`
- [ ] Build fixture: setup fragment appears after `Reveal.initialize` in `.slides.html`
- [ ] Build negative: no `slide_setup` → no broken include-after flag
- [ ] Mermaid init moved or guarded to share post-Reveal lifecycle
- [ ] Reference ambient example (or documented contract) yields/pauses when current slide has `data-background*`
- [ ] Existing inventory header/background baselines still pass

## Implementation Notes

See CIP-0012 Track B §B1–B3. Do not put talk-specific ambient JS into the shared default `slides-header.html`. Default is exclusive yield, not layered stacking.

## Related

- CIP: 0012
- Depends on: `2026-09-15_cip0012-inventory-test-suite`

## Progress Updates

### 2026-09-15

Task created (Ready) when CIP-0012 Accepted.

### 2026-09-15 (later)

Acceptance criteria extended for §B3 per-slide vs deck ambient clash policy.
