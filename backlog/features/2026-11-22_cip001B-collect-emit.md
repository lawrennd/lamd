---
id: "2026-11-22_cip001B-collect-emit"
title: "Collect blocktime entries and emit timeplan table"
status: "Completed"
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

- [x] Blocks from the main file and from `\include`s appear in plan order
- [x] `\timeplan` expands to one markdown/HTML table with minutes and labels
- [x] When `\sessionstart` is set, clock ranges are derived from cumulative durations
- [x] Lectures without `\blocktime` / `\timeplan` are unchanged
- [x] Unflagged blocks do not create classtimer iframes

## Implementation Notes

Emission is **only** at `\timeplan` (no auto-insert). Implemented as `lamd/timeplan.py` plus a post-gpp pass in `mdpp` so include-expanded markers are collected in order. Same markdown table for notes and slides for v1.

## Related

- CIP: 001B

## Progress Updates

### 2026-11-22

Task created after CIP-001B was accepted.

Implemented `expand_timeplan` and wired it after gpp in `mdpp`. Unit + gpp integration tests pass.
