---
id: "2026-08-09_cip0010-paths-resolver-module"
title: "CIP-0010 Phase 1: Add lamd.paths resolver module"
status: "Completed"
priority: "High"
created: "2026-08-09"
last_updated: "2026-08-09"
category: "features"
related_cips: ["0010"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- paths
- diagrams
- mdpp
---

# Task: CIP-0010 Phase 1 — Add `lamd.paths` resolver module

## Description

Implement the unified path-resolution layer described in CIP-0010: separate
filesystem and web resolution for `\diagramsDir`, path normalisation, and a small
CLI for shell scripts. No consumer wiring in this task — only the module and tests.

## Acceptance Criteria

- [x] `lamd/paths.py` exposes `resolve_diagrams_filesystem()` and `resolve_diagrams_web()`
- [x] `normalise_path()` collapses duplicate slashes and resolves `.` / `..` relative to a base cwd
- [x] Optional `diagramswebpath` config key supported in web resolver fallback chain
- [x] CLI entry point prints filesystem path (for make / `copy_web_diagrams.sh`)
- [x] Unit tests in `tests/unit/test_paths.py` cover cwd, CLI overrides, `diagramsurl`, env expansion
- [x] Deprecation warning when `diagramsdir` looks like a URL

## Implementation Notes

See CIP-0010 “Unified resolver module” and “Resolution rules” sections.
Table-driven tests should include `_lamd/` cwd and Patterns B–D from the CIP audit.

## Related

- CIP: [CIP-0010](../../cip/cip0010.md)
- Parent tracking: [2025-05-22_path-handling-consistency](2025-05-22_path-handling-consistency.md)

## Progress Updates

### 2026-08-09

Task created from CIP-0010 implementation plan step 1.
