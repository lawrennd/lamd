---
id: "2026-02-03_lamd-cli-entrypoint"
title: "Phase 1: Add `lamd` CLI entrypoint with talk/cv subcommands"
status: "Proposed"
priority: "High"
created: "2026-02-03"
last_updated: "2026-02-03"
category: "features"
related_cips: ["0006"]
owner: "Neil Lawrence"
dependencies: []
tags:
- cli
- interface
- two-stage
- workflow
---

# Task: Add `lamd` CLI entrypoint with talk/cv subcommands

## Description

Create a new top-level `lamd` command (subcommand-style) without changing existing commands (`maketalk`, `makecv`). This provides the migration path for the two-stage interface workflow while preserving backward compatibility.

## Acceptance Criteria

- [ ] `lamd` CLI entrypoint exists (e.g. `lamd/cli.py` with `main()`)
- [ ] `pyproject.toml` exposes `lamd = "lamd.cli:main"` (or equivalent)
- [ ] `lamd --help` shows at least `talk` and `cv` subcommands
- [ ] Running `lamd` with no args returns help and non-zero exit
- [ ] No behavior change to existing `maketalk` / `makecv`

## Related

- CIP: 0006
- Umbrella: `backlog/features/2026-01-04_two-stage-cli-phase1.md`

## Progress Updates

### 2026-02-03

Task created to decompose CIP-0006 Phase 1 into concrete DO-work.

