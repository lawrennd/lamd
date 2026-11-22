---
id: "2026-11-22_cip001B-docs-fixtures"
title: "Document timeplan macros and add fixtures"
status: "Ready"
priority: "Medium"
created: "2026-11-22"
last_updated: "2026-11-22"
category: "documentation"
related_cips: ["001B"]
owner: "Neil D. Lawrence"
dependencies:
- "2026-11-22_cip001B-collect-emit"
- "2026-11-22_cip001B-overrun-warn"
tags:
- backlog
- cip001B
- docs
- fixtures
---

# Task: CIP-001B docs and fixtures

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).

## Description

Document `\sessionstart`, `\sessionlength`, `\blocktime`, and `\timeplan` in slides/notes context docs, clearly distinguishing them from `\classtimer` / `\classtimertitled`. Add fixtures that assert compiled table content, include order, overrun warning, and no stray timer slides unless flagged.

## Acceptance Criteria

- [ ] Docs distinguish allocation/plan macros from live countdown timers
- [ ] `\timeplan` emission rule (explicit only) is documented
- [ ] Fixture: compiled table matches block order and minutes
- [ ] Fixture: include-borne `\blocktime` appears in plan order
- [ ] Fixture: unflagged blocks create no timer iframes; `timer` flag does (if bridge landed)
- [ ] Fixture: overrun warning when sum > session length

## Implementation Notes

Update `docs/contexts/slides.md` and/or a short lectures/planning note. Mirror CIP-0012 fixture layout under `tests/fixtures/` if that pattern still fits.

## Related

- CIP: 001B
- Documentation: docs/contexts/slides.md

## Progress Updates

### 2026-11-22

Task created after CIP-001B was accepted.
