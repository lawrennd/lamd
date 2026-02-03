---
id: "2026-02-03_lamd-cli-docs-and-migration"
title: "Phase 1: Document `lamd` CLI two-stage workflow and migration path"
status: "Proposed"
priority: "Medium"
created: "2026-02-03"
last_updated: "2026-02-03"
category: "documentation"
related_cips: ["0006"]
owner: "Neil Lawrence"
dependencies:
- "2026-02-03_lamd-talk-subcommand"
- "2026-02-03_lamd-cv-subcommand"
tags:
- documentation
- cli
- migration
- workflow
---

# Task: Document `lamd` CLI two-stage workflow and migration path

## Description

Create user-facing documentation for the new `lamd` CLI, focusing on:

- `lamd talk` and `lamd cv`
- the interface file format and what it enables (auditability, reproducibility)
- migration guidance from `maketalk`/`makecv` to the new `lamd` CLI

## Acceptance Criteria

- [ ] Docs cover `lamd talk` and `lamd cv` with examples
- [ ] Docs explain `--generate` and `--execute` and when to use them
- [ ] Docs clarify that `maketalk`/`makecv` remain supported (no breaking change)
- [ ] Docs link to interface schema reference

## Related

- CIP: 0006
- Requirement: `requirements/req0001_cli-discoverability.md`
- Requirement: `requirements/req0003_workflow-transparency.md`
- Cross-reference: ExecEd “material review” work that motivates future `lamd` analysis subcommands:
  - `~/mlatcl/execed/cip/cip0002.md`
  - `~/mlatcl/execed/backlog/features/2026-01-28_execed-material-review-tooling.md`

## Progress Updates

### 2026-02-03

Task created to decompose CIP-0006 Phase 1 into concrete DO-work.

