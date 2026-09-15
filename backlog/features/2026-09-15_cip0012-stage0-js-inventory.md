---
id: "2026-09-15_cip0012-stage0-js-inventory"
title: "CIP-0012 Stage 0: Inventory JS use in snippets and talks"
status: "Ready"
priority: "High"
created: "2026-09-15"
last_updated: "2026-09-15"
category: "features"
related_cips: ["0012"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- cip0012
- javascript
- inventory
- slides
---

# Task: CIP-0012 Stage 0 — JS inventory + fixture list

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Before any API or makefile changes, inventory existing JavaScript authoring in snippets, talks, and lamd includes. Classify each hit as Track A (content / multi-format), Track B (Reveal setup / background), or other. Produce `cip/cip0012/inventory.md` and an agreed fixture list for the regression suite.

No macro or makefile changes land until this inventory and fixture list are reviewed.

## Acceptance Criteria

- [ ] Search `snippets/**/*.md` for `<script`, `scriptsDir`, `_scripts/includes`, canvas widgets
- [ ] Search `talks/**/*.md` for the same plus `data-background`, `data-background-iframe`, `slidesheader`
- [ ] Search `lamd/includes/` and `lamd/macros/` for shared header JS, `\includeplotly`, animation init
- [ ] Each hit classified Track A / Track B / other, with format reach noted
- [ ] `cip/cip0012/inventory.md` written with findings and a concrete fixture list (ballworld/maxwell, dasher or dieroll, privacy `data-background`, `figure-animate` header, iframe if any)
- [ ] Fixture list reviewed/agreed before Stage 1 tasks start

## Implementation Notes

Keep the CIP as the decision document; put research detail in `cip/cip0012/`. Prefer listing real paths that map 1:1 to slim copies under `tests/fixtures/cip0012/` in the next task.

## Related

- CIP: 0012
- Next: `2026-09-15_cip0012-inventory-test-suite`

## Progress Updates

### 2026-09-15

Task created (Ready) when CIP-0012 Accepted.
