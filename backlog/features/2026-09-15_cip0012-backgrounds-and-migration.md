---
id: "2026-09-15_cip0012-backgrounds-and-migration"
title: "CIP-0012: Background helpers and migration examples"
status: "Ready"
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

Document (and optionally implement) Track B background authoring helpers. Migrate or twin at least one inventoried content loader to `\includescript`. Provide a minimal `slide_setup` ambient example and one iframe-background slide example. Document the frontmatter `background:` pitfall (layout numbering ≠ slide background).

## Acceptance Criteria

- [ ] Raw `data-background` / `data-background-iframe` documented as primary Track B API
- [ ] `\slidebackground` / `\slidebackgroundiframe` added **or** explicitly deferred with rationale in CIP
- [ ] At least one inventoried Track A loader migrated or twin-documented with `\includescript`
- [ ] Example `slide_setup` fragment for ambient canvas (or equivalent) under includes / `_scripts`
- [ ] Example slide using iframe background pattern
- [ ] `background:` vs slide background pitfall written for later docs compression
- [ ] Manual spot-check notes for one live talk (e.g. Information Engines) if migration touches it

## Implementation Notes

Helpers only if they nest cleanly inside `\newslide`’s second argument; otherwise keep raw attributes.

## Related

- CIP: 0012
- Depends on: slide_setup + includescript tasks

## Progress Updates

### 2026-09-15

Task created (Ready) when CIP-0012 Accepted.
