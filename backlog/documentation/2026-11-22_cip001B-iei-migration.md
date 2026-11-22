---
id: "2026-11-22_cip001B-iei-migration"
title: "IEI migration example for blocktime/timeplan"
status: "Completed"
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

- [x] One IEI lecture (or a short excerpt) migrated as a worked example
- [x] Quiz keeps a live timer via `{timer}`; other blocks are plan-only
- [x] Hand table removed in favour of compiled `\timeplan`
- [x] Note linked from lamd docs or the CIP references section

## Implementation Notes

Worked examples live under `cip/cip001B/iei-validation/` (forks of Weeks 6–8 time plans). Live IEI `_lamd/*.md` curriculum is unchanged until a teaching pass applies the same pattern.

Validate with:

```bash
PYTHONPATH=. python3 cip/cip001B/iei-validation/validate_forks.py
```

Finding: Week 6 as-delivered SRT clocks sum to 113 minutes against a 110-minute slot — overrun advisory fires correctly.

## Related

- CIP: 001B
- Module: IEI `_lamd/`
- Forks: `cip/cip001B/iei-validation/`

## Progress Updates

### 2026-11-22

Task created after CIP-001B was accepted (optional follow-on).

Completed as validation forks + script (limits / good-regulator / exponential-family). Live IEI apply deferred to a separate teaching edit.
