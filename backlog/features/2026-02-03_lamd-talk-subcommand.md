---
id: "2026-02-03_lamd-talk-subcommand"
title: "Phase 1: Implement `lamd talk` (generate + execute)"
status: "Proposed"
priority: "High"
created: "2026-02-03"
last_updated: "2026-02-03"
category: "features"
related_cips: ["0006"]
owner: "Neil Lawrence"
dependencies:
- "2026-02-03_lamd-cli-entrypoint"
- "2026-02-03_interface-schema-compute-section"
tags:
- cli
- talk
- two-stage
---

# Task: Implement `lamd talk` (generate + execute)

## Description

Implement the `lamd talk` subcommand that provides the two-stage workflow:

- `lamd talk --generate talk.md` → writes `{basename}.interface.yml`
- `lamd talk --execute talk.interface.yml` → executes the workflow described
- `lamd talk talk.md` → default: generate then execute

## Acceptance Criteria

- [ ] `lamd talk talk.md` produces the same outputs as `maketalk talk.md` for common cases
- [ ] `--generate` creates an interface file without executing
- [ ] `--execute` consumes the interface file and executes successfully
- [ ] Existing `maketalk` remains unchanged and fully supported
- [ ] Help text is clear and includes examples

## Related

- CIP: 0006
- Umbrella: `backlog/features/2026-01-04_two-stage-cli-phase1.md`

## Progress Updates

### 2026-02-03

Task created to decompose CIP-0006 Phase 1 into concrete DO-work.

