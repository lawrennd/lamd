---
id: "2026-08-09_cip0010-wire-mdpp-dependencies"
title: "CIP-0010 Phase 2: Wire mdpp and dependencies to path resolver"
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
- mdpp
- dependencies
---

# Task: CIP-0010 Phase 2 — Wire mdpp and dependencies to path resolver

## Description

Replace ad hoc `\diagramsDir` logic in `mdpp.py` and `resolve_diagrams_dir()` in
`dependencies.py` with calls to `lamd.paths`. Add optional `--diagrams-web-dir` to
`mdpp` for html/ipynb-only web overrides.

## Acceptance Criteria

- [x] `mdpp.py` uses resolver for filesystem vs web `\diagramsDir` assignment
- [x] `dependencies.py` delegates filesystem resolution to `lamd.paths`
- [x] `--diagrams-dir` unchanged for make-driven builds (filesystem override)
- [x] `--diagrams-web-dir` added to mdpp argparse (html/ipynb only)
- [x] `test_mdpp.py` and `test_dependencies.py` updated for resolver integration
- [x] Inline url/baseurl concatenation removed from mdpp for local formats

## Implementation Notes

Keep backward-compatible fallback chain documented in CIP-0010. Tactical fixes
already in `dependencies.py` and `make-talk-flags.mk` should converge on the resolver
rather than duplicate logic.

## Related

- CIP: [CIP-0010](../../cip/cip0010.md)
- Depends on: [2026-08-09_cip0010-paths-resolver-module](2026-08-09_cip0010-paths-resolver-module.md)

## Progress Updates

### 2026-08-09

Task created from CIP-0010 implementation plan step 2.

### 2026-08-09 (implementation)

Wired `mdpp.py` and `dependencies.py` to `lamd.paths`; added `--diagrams-web-dir`.
