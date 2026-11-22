---
id: "2026-11-22_cip001B-overrun-warn"
title: "Advisory warning when blocktime sum exceeds sessionlength"
status: "Ready"
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

- [ ] Sum > session length → warning on stderr (or build log); build still succeeds
- [ ] Missing label → warning
- [ ] No `\sessionlength` → no overrun check (or skip quietly)
- [ ] Fixture covers the overrun case

## Implementation Notes

Strict/fail mode is out of scope for v1. Keep the warning message actionable (sum, limit, excess minutes).

## Related

- CIP: 001B

## Progress Updates

### 2026-11-22

Task created after CIP-001B was accepted.
