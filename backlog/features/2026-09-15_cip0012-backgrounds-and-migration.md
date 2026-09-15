---
id: "2026-09-15_cip0012-backgrounds-and-migration"
title: "CIP-0012: Background helpers and migration examples"
status: "Completed"
priority: "Medium"
created: "2026-09-15"
last_updated: "2026-09-15"
category: "features"
related_cips: ["0012"]
owner: "Neil Lawrence"
dependencies:
- "2026-09-15_cip0012-slide-setup-include-after"
- "2026-09-15_cip0012-includescript-macro"
tags:
- backlog
- cip0012
- revealjs
- javascript
- migration
---

# Task: CIP-0012 — Backgrounds, helpers, and migration examples

## Description

Document (and optionally implement) Track B background authoring helpers. Migrate or twin at least one inventoried content loader to `\includescript`. Provide a minimal `slide_setup` ambient example and one iframe-background slide example. Document the frontmatter `background:` pitfall and **§B3 clash policy** (deck ambient vs per-slide, including shared snippet slides).

## Acceptance Criteria

- [x] Raw `data-background` / `data-background-iframe` documented as primary Track B API
- [x] `\slidebackground` / `\slidebackgroundiframe` deferred — raw `data-background*` is primary (CIP progress)
- [x] At least one inventoried Track A loader migrated or twin-documented with `\includescript`
- [x] Example `slide_setup` fragment for ambient canvas implements §B3 yield/resume on `slidechanged`
- [x] Example slide using iframe background pattern (demonstrates ambient yielding while that slide is current)
- [x] Docs notes: `background:` pitfall + deck vs per-slide clash policy (for later compression)
- [ ] Manual spot-check notes for one live talk (e.g. Information Engines) if migration touches it

## Implementation Notes

Helpers only if they nest cleanly inside `\newslide`’s second argument; otherwise keep raw attributes. Shared snippet `\newslide{…}{data-background=…}` is per-slide precedence, not a third tier.

## Related

- CIP: 0012 §B3
- Depends on: slide_setup + includescript tasks

## Progress Updates

### 2026-09-15

Task created (Ready) when CIP-0012 Accepted.

### 2026-09-15 (later)

Extended for §B3 deck ambient vs per-slide clash documentation and example behaviour.

### 2026-09-15 (implementation)

Completed as part of CIP-0012 implementation.
