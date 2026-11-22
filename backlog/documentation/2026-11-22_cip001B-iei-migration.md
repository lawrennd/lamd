---
id: "2026-11-22_cip001B-iei-migration"
title: "IEI migration example for blocktime/timeplan"
status: "Proposed"
priority: "Low"
created: "2026-11-22"
last_updated: "2026-11-22"
category: "documentation"
related_cips: ["001B"]
owner: "Neil D. Lawrence"
dependencies: ["2026-11-22_cip001B-docs-fixtures"]
tags:
- backlog
- cip001B
- iei
- migration
---

# Task: CIP-001B IEI migration example

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).  
> Optional follow-on in the IEI module repo once lamd macros ship.

## Description

Show how to replace IEI hand-written Clock|Block notes tables and quiz-only `\classtimertitled` with `\sessionstart` / `\sessionlength` / `\timeplan` / `\blocktime{…}{…}{timer}` for the quiz row and unmarked content blocks elsewhere.

## Acceptance Criteria

- [ ] One IEI lecture (or a short excerpt) migrated as a worked example
- [ ] Quiz keeps a live timer via `{timer}`; other blocks are plan-only
- [ ] Hand table removed in favour of compiled `\timeplan`
- [ ] Note linked from lamd docs or the CIP references section

## Implementation Notes

Work lands primarily in the IEI module (`_lamd/*.md`), not in the lamd package. Keep this task optional until the core macros are validated.

## Related

- CIP: 001B
- Module: IEI `_lamd/`

## Progress Updates

### 2026-11-22

Task created after CIP-001B was accepted (optional follow-on).
