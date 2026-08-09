---
id: "2026-08-08_cip0005-dependency-management"
title: "CIP-0005 Phase 4: Dependency Management for mdpp"
status: "Proposed"
priority: "Medium"
created: "2026-08-08"
last_updated: "2026-08-09"
category: "features"
related_cips: ["0005"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- mdpp
- dependencies
- validation
---

# Task: CIP-0005 Phase 4 — Dependency Management for mdpp

## Description

Implement dependency checking and validation for mdpp as described in CIP-0005 Phase 4. This includes verifying that required external tools (gpp, pandoc, etc.) are installed and accessible, checking version compatibility, and providing clear error messages when dependencies are missing.

## Acceptance Criteria

- [ ] Required tools (gpp, pandoc) are checked for presence and version before processing
- [ ] Clear, actionable error messages emitted when dependencies are missing
- [ ] Version compatibility checked and warnings issued for known-incompatible versions
- [ ] Bibliography files existence verified when referenced in frontmatter
- [x] Template and include paths validated before processing begins (partial: potx/dotx via `check-reference-docs` and `resolve_reference_doc()` — see `2026-08-09_reference-doc-template-resolution.md`)

## Implementation Notes

- Add a `check_dependencies()` function in `lamd/validation.py`
- Integrate the check into `mdpp.py` pre-processing step
- Use `shutil.which()` for tool presence; `subprocess` for version queries
- Keep checks optional/skippable with a `--skip-dep-check` flag to avoid CI overhead

## Related

- CIP: 0005
- Documentation: cip/cip0005.md

## Progress Updates

### 2026-08-09

Partial completion: reference-doc template resolution and early makefile check
(`2026-08-09_reference-doc-template-resolution.md`). Remaining: gpp/pandoc version
checks, bibliography validation, mdpp integration.

### 2026-08-08

Task created — tracking Phase 4 of CIP-0005.
