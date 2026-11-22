---
id: "2026-11-22_cip001B-timer-bridge"
title: "Optional blocktime timer flag emits classtimertitled"
status: "Completed"
priority: "Medium"
created: "2026-11-22"
last_updated: "2026-11-22"
category: "features"
related_cips: ["001B"]
owner: "Neil D. Lawrence"
dependencies: ["2026-11-22_cip001B-collect-emit"]
tags:
- backlog
- cip001B
- classtimer
- timer
---

# Task: CIP-001B timer bridge

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).

## Description

When `\blocktime{minutes}{label}{timer}` is used, also emit the existing `\classtimertitled` live countdown at that point. Derive the wall-clock argument from `\sessionstart` plus cumulative prior minutes when possible; otherwise require an explicit clock.

## Acceptance Criteria

- [x] `timer` flag expands to `\classtimertitled{HH:MM}{label}` (or equivalent iframe) in slides HTML
- [x] Blocks without `timer` never produce timer iframes
- [x] With `\sessionstart`, derived clock matches the plan table start for that block
- [x] Without `\sessionstart`, behaviour is documented and fails clearly or requires an explicit clock
- [x] Existing CIP-0012 classtimer fixtures still pass

## Implementation Notes

Do not invent a second timer UI. Reuse CIP-0012 chrome only.

Post-gpp `expand_timeplan(..., timer_mode=…)` emits the same slides-html iframe / notes placeholder that `\classtimertitled` would have produced. Without `\sessionstart`, warns and skips the timer (no chrome).

## Related

- CIP: 001B
- CIP: 0012

## Progress Updates

### 2026-11-22

Task created after CIP-001B was accepted.

Completed: timer bridge in `lamd/timeplan.py`; mdpp selects `slides-html` / `notes` / `none` from format+to.
