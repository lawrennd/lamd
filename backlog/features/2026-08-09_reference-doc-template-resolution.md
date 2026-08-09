---
id: "2026-08-09_reference-doc-template-resolution"
title: "Resolve bundled potx/dotx reference templates for pandoc"
status: "Completed"
priority: "Medium"
created: "2026-08-09"
last_updated: "2026-08-09"
category: "features"
related_cips: ["0005"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- flags
- pptx
- docx
- validation
---

# Task: Resolve bundled potx/dotx reference templates for pandoc

## Description

PPTX and DOCX builds failed at the pandoc step when `_lamd.yml` configured bare
filenames such as `potx: custom-reference.potx`. Pandoc's `--reference-doc` does
not search `--resource-path`, so the template had to exist in the build directory
even though lamd ships copies under `lamd/includes/`. Because mdpp runs before
pandoc, the failure appeared only after a long preprocessing step.

## Acceptance Criteria

- [x] Bare `potx` / `dotx` filenames resolve to `lamd/includes/` when absent from cwd
- [x] Explicit paths and cwd-local templates are unchanged
- [x] Makefile fails fast with a clear message if the resolved template is missing
- [x] Template check runs before mdpp on pptx/docx builds
- [x] Unit tests cover reference-doc resolution

## Implementation Notes

- Added `resolve_reference_doc()` in `lamd/flags.py`; used by docx/pptx flag output
- Added `check-reference-docs` target in `make-talk-flags.mk`
- Wired check as a prerequisite of pptx/docx mdpp rules in `make-slides.mk` and `make-docx.mk`

## Related

- CIP: 0005 (Phase 4 — template path validation)
- Backlog: `2026-08-08_cip0005-dependency-management.md` (broader dependency work remains)

## Progress Updates

### 2026-08-09

Implemented and validated against `mlfc/_lamd` pptx build (template error resolved;
separate missing-diagram issue remains in content).
