---
id: "2026-08-09_cip0010-makefiles-copy-web-scripts"
title: "CIP-0010 Phase 3: Align makefiles and copy_web_diagrams with resolver"
status: "Completed"
priority: "High"
created: "2026-08-09"
last_updated: "2026-08-09"
category: "features"
related_cips: ["0010"]
owner: "Neil Lawrence"
dependencies: ["2026-08-09_cip0010-paths-resolver-module"]
tags:
- backlog
- paths
- makefiles
- scripts
---

# Task: CIP-0010 Phase 3 — Align makefiles and copy_web_diagrams with resolver

## Description

Remove special-case path logic from shell and make layers; use `$(DIAGRAMSDIR)` and
the paths resolver CLI consistently across TeX preprocess, web diagram copy, and any
remaining hardcoded `diagrams` paths.

## Acceptance Criteria

- [x] `make-tex.mk` passes `--diagrams-dir $(DIAGRAMSDIR)` instead of hardcoded `diagrams`
- [x] `copy_web_diagrams.sh` removes `_lamd` basename hack; uses resolver CLI or pre-resolved path from make
- [x] Audit of `lamd/makefiles/` finds no other hardcoded diagram roots inconsistent with `DIAGRAMSDIR`
- [x] `make-ipynb.mk` reviewed; web vs filesystem flags passed explicitly if needed
- [x] Clear error when resolved diagrams root does not exist (message cites config key and cwd)

## Implementation Notes

Prefer thin bash calling `python -m lamd.paths` (or documented CLI name) over
duplicating resolution in shell. Coordinate with Phase 2 so make targets pass the
same paths mdpp and dependencies use.

## Related

- CIP: [CIP-0010](../../cip/cip0010.md)
- Depends on: [2026-08-09_cip0010-paths-resolver-module](2026-08-09_cip0010-paths-resolver-module.md)

## Progress Updates

### 2026-08-09

Task created from CIP-0010 implementation plan step 3.

### 2026-08-09 (implementation)

- `make-tex.mk`: `--diagrams-dir ${DIAGRAMSDIR}`
- `copy_web_diagrams.sh`: resolver CLI + `--diagrams-dir` on dependencies; removed `_lamd` hack
- `make-ipynb.mk`: documented web URL resolution (no `--diagrams-dir` on ipynb targets)
