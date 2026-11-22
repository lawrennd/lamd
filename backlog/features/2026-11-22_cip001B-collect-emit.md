---
id: "2026-11-22_cip001B-collect-emit"
title: "Collect blocktime entries and emit timeplan table"
status: "Ready"
priority: "High"
created: "2026-11-22"
last_updated: "2026-11-22"
category: "features"
related_cips: ["001B"]
owner: "Neil D. Lawrence"
dependencies: ["2026-11-22_cip001B-macros"]
tags:
- backlog
- cip001B
- mdpp
- timeplan
---

# Task: CIP-001B collect and emit time plan

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).

## Description

In `mdpp` (or a small post-pass), collect `\blocktime` entries in document order after includes expand, and replace `\timeplan` with a compiled **Clock | Mins | Block** table (clock column when `\sessionstart` is set).

## Acceptance Criteria

- [ ] Blocks from the main file and from `\include`s appear in plan order
- [ ] `\timeplan` expands to one markdown/HTML table with minutes and labels
- [ ] When `\sessionstart` is set, clock ranges are derived from cumulative durations
- [ ] Lectures without `\blocktime` / `\timeplan` are unchanged
- [ ] Unflagged blocks do not create classtimer iframes

## Implementation Notes

Emission is **only** at `\timeplan` (no auto-insert). Notes are the primary surface; slides may emit a short summary or leave `\timeplan` inert — document the choice in the docs task.

## Related

- CIP: 001B

## Progress Updates

### 2026-11-22

Task created after CIP-001B was accepted.
