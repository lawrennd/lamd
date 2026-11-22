---
id: "2026-11-22_cip001B-overrun-warn"
title: "Advisory warning when blocktime sum exceeds sessionlength"
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
- validation
---

# Task: CIP-001B overrun advisory

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).

## Description

When `\sessionlength` (or YAML equivalent) is set and the sum of `\blocktime` minutes exceeds it, emit a non-fatal advisory warning during the build. Also warn if a collected block is missing a label.

## Acceptance Criteria

- [x] Sum > session length → warning on stderr (or build log); build still succeeds
- [x] Missing label → warning
- [x] No `\sessionlength` → no overrun check (or skip quietly)
- [x] Fixture covers the overrun case

## Implementation Notes

Strict/fail mode is out of scope for v1. Warnings live in `warn_timeplan` / `expand_timeplan` (`lamd/timeplan.py`).

## Related

- CIP: 001B

## Progress Updates

### 2026-11-22

Task created after CIP-001B was accepted.

Completed alongside collect/emit: advisory overrun and missing-label warnings with unit coverage.
