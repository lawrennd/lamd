---
id: "2026-02-03_lamd-cv-subcommand"
title: "Phase 1: Implement `lamd cv` (generate + execute)"
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
- cv
- two-stage
---

# Task: Implement `lamd cv` (generate + execute)

## Description

Implement the `lamd cv` subcommand with the same two-stage workflow as `lamd talk`:

- `lamd cv --generate cv.md`
- `lamd cv --execute cv.interface.yml`
- `lamd cv cv.md` (default: generate then execute)

## Acceptance Criteria

- [ ] `lamd cv cv.md` produces the same outputs as `makecv cv.md` for common cases
- [ ] `--generate` creates an interface file without executing
- [ ] `--execute` consumes the interface file and executes successfully
- [ ] Existing `makecv` remains unchanged and fully supported
- [ ] Help text is clear and includes examples

## Related

- CIP: 0006
- Umbrella: `backlog/features/2026-01-04_two-stage-cli-phase1.md`

## Progress Updates

### 2026-02-03

Task created to decompose CIP-0006 Phase 1 into concrete DO-work.

