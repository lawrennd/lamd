---
id: "2026-09-15_cip0012-inventory-test-suite"
title: "CIP-0012: Inventory-derived JS regression test suite"
status: "Completed"
priority: "High"
created: "2026-09-15"
last_updated: "2026-09-15"
category: "features"
related_cips: ["0012"]
owner: "Neil Lawrence"
dependencies:
- "2026-09-15_cip0012-stage0-js-inventory"
tags:
- backlog
- cip0012
- javascript
- testing
- slides
---

# Task: CIP-0012 — Inventory-derived test suite

## Description

Land checked-in fixtures and baseline/regression tests derived from the Stage 0 fixture list, under `tests/fixtures/cip0012/` (or equivalent) plus unit tests. Fixtures must map back to real snippet/talk paths in the inventory. Prefer slim copies over depending on live `talks/` / `snippets/` checkouts in CI.

Baseline tests should pass for **current** (legacy) behaviour before `\includescript` / `slide_setup` land, so later migrations are measurable.

## Acceptance Criteria

- [ ] Fixtures for each agreed inventory representative (content scripts, `data-background`, shared header JS)
- [ ] Track A: expansion tests — script tags present in slides-html and notes-html paths; absent in tex (as applicable to current macros)
- [ ] Track B: `data-background` (and iframe if inventoried) still emit on reveal sections after `\newslide`
- [ ] Header: default `slides-header.html` still references MathJax + `figure-animate.js`
- [ ] Inventory/fixture path mapping documented (in inventory or test module docstring)
- [ ] `pytest` suite green for these baselines

## Implementation Notes

Follow patterns in existing unit tests for GPP/macro expansion (`tests/unit/`). Do not require network access to `inverseprobability.com` for unit tests — assert on emitted markup / relative `scriptsDir` tokens.

## Related

- CIP: 0012
- Depends on: `2026-09-15_cip0012-stage0-js-inventory`

## Progress Updates

### 2026-09-15

Task created (Ready) when CIP-0012 Accepted.

### 2026-09-15 (implementation)

Completed as part of CIP-0012 implementation.
