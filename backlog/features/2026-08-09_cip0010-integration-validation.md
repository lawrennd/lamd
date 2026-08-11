---
id: "2026-08-09_cip0010-integration-validation"
title: "CIP-0010 Phase 5: Integration validation on mlfc builds"
status: "Completed"
priority: "High"
created: "2026-08-09"
last_updated: "2026-08-11"
category: "features"
related_cips: ["0010"]
owner: "Neil Lawrence"
dependencies:
- "2026-08-09_cip0010-wire-mdpp-dependencies"
- "2026-08-09_cip0010-makefiles-copy-web-scripts"
tags:
- backlog
- paths
- testing
- integration
---

# Task: CIP-0010 Phase 5 — Integration validation on mlfc builds

## Description

Validate the full resolver + consumer changes against real course builds. Confirm
pptx, html slides, TeX notes, and web diagram copy agree on filesystem paths without
`_lamd` directory-name hacks.

## Acceptance Criteria

- [x] `mlfc/_lamd/basis-functions-and-generalisation.pptx` builds cleanly
- [x] HTML slides target for the same talk builds; diagram URLs sane for publish (`https://mlatcl.github.io/mlfc/diagrams/...`)
- [x] At least one TeX notes target uses `$(DIAGRAMSDIR)` end-to-end (`notes.tex.markdown` → absolute paths under `mlfc/slides/diagrams/`)
- [x] `copy_web_diagrams.sh` run from `_lamd` succeeds without path adjustment hack
- [x] `dependencies batch` and markdown image paths match for the same source file (both under `mlfc/slides/diagrams/`)
- [x] Regression check: flat `./slides/diagrams/` Pattern A covered by `tests/unit/test_paths.py` (no dedicated integration fixture)

## Implementation Notes

Document manual checklist in CIP-0010 Implementation Status when complete. Consider
adding a minimal integration fixture under `tests/integration/` if repeatable in CI.

## Related

- CIP: [CIP-0010](../../cip/cip0010.md)
- Depends on Phases 2 and 3 backlog tasks

## Progress Updates

### 2026-08-09

Task created from CIP-0010 implementation plan step 5.

### 2026-08-11

Ran integration validation from `mlfc/_lamd` against `basis-functions-and-generalisation`:

- `lamd-resolve-diagrams-dir --cwd .` → `/Users/neil/mlatcl/mlfc/slides/diagrams`
- `make basis-functions-and-generalisation.pptx` — success (~6.6 MB)
- Forced rebuild of `basis-functions-and-generalisation.slides.html` — success; SVG `data=` URLs use publish base
- `make basis-functions-and-generalisation.notes.tex.markdown` — success; `\includegraphics` paths resolve under `slides/diagrams/`
- `copy_web_diagrams.sh … slidediagrams` — exit 0, no `_lamd` directory hack
- `dependencies batch` — diagram deps under `mlfc/slides/diagrams/`
- Unit tests: `tests/unit/test_paths.py` pass (41 related tests; one unrelated `test_mdpp` frontmatter failure pre-existing)

Note: `make basis-functions-and-generalisation.include.tex` failed on missing `../_includes/talk-notation.tex` (mlfc layout, not diagram resolution). Animation duplicate-id fix verified in rebuilt slides (`olympic_LM_polynomial_number` vs `_val`).
