---
category: bugs
created: '2026-08-24'
dependencies: []
id: 2026-08-24_ipynb-references-cell-boundary
last_updated: '2026-08-24'
owner: Neil Lawrence
priority: High
related_cips: []
status: Completed
title: Ipynb References Cell Boundary Stray Marker
---

# Task: Fix stray cell marker before References in ipynb output

## Description

In the ipynb notes pipeline, `\references` expanded to `\subsection{References}`, which emits an opening `::: {.cell .markdown}` via `talk-macros-notes-ipynb.gpp` but no closing `:::` at document end. Pandoc then left the opener as literal content in the final notebook cell.

Observed in IEI notebooks (e.g. `iei/_notebooks/01-motivation-boltzmann.ipynb`): the References cell began with `::: {.cell .markdown}` instead of `## References`.

## Root cause

`\references` in `talk-macros-ipynb.gpp` inherited the generic `\subsection` expansion, which starts a new markdown cell without closing the document-level cell boundary.

## Fix applied

Changed `\references` in `lamd/macros/talk-macros-ipynb.gpp` to close the current cell and emit a plain `## References` heading (no `\subsection`):

```gpp
\define{\references}{\endCell

## References

}
```

## Acceptance Criteria

- [x] `\references` does not emit an unclosed `::: {.cell .markdown}` in ipynb intermediate markdown
- [x] Regression test `test_references_cell_boundary_no_stray_markers` passes
- [x] Rebuilt IEI notebook 01 shows References cell starting with `## References` only
- [ ] Rebuild remaining IEI lectures (02–08) to refresh notebooks after macro fix

## Related

- Test fixture: `tests/unit/test-references-cell-boundary.md`
- Test: `tests/unit/test_cell_boundaries.py::TestCellBoundaries::test_references_cell_boundary_no_stray_markers`
- Macro: `lamd/macros/talk-macros-ipynb.gpp`
- Prior related task: `backlog/bugs/2025-08-30_pandoc-cell-boundary-issue.md`

## Progress Updates

### 2026-08-24

Fix implemented and regression test added. Validated on `motivation-boltzmann` rebuild; other IEI notebooks still need rebuild.
