---
id: "2026-10-13_cip0014-fontsize-demo"
title: "CIP-0014: Font-size scale demo / fixture"
status: "Completed"
priority: "Medium"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "features"
related_cips: ["0014"]
owner: "Neil Lawrence"
dependencies:
- "2026-10-13_cip0014-talkfontsize-flags"
tags:
- backlog
- cip0014
- revealjs
- slides
- demo
- typography
---

# Task: CIP-0014 — font-size demo / fixture

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Add a small Reveal demo or build fixture that shows all five size steps at deck level and per-slide overrides (similar spirit to `demos/cip0012-ambient-background.html`). Optionally assert in tests that a fixture markdown with `.font-sm` yields the class on the reveal section.

## Acceptance Criteria

- [ ] Demo or fixture covers `xs`–`xl` (deck and/or per-slide)
- [ ] Shows coexistence with `.scrollable` on at least one slide
- [ ] Lightweight test or documented manual check for section class emission
- [ ] Linked from CIP-0014 References when landed

## Implementation Notes

Prefer a package-local demo under `demos/` or a unit fixture under `tests/fixtures/` that does not require a full talks repo checkout.

## Related

- CIP: 0014
- Depends on: `2026-10-13_cip0014-talkfontsize-flags`

## Progress Updates

### 2026-10-13

Task created (Ready) when CIP-0014 Accepted.

### 2026-10-13 (implementation)

Completed with CIP-0014 implementation.
