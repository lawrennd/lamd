---
category: features
created: "2026-10-22"
dependencies:
- 2026-10-22_cv-missing-check-reference-docs
github_issue: ""
id: 2026-10-22_cv-pdf-via-cvneil
last_updated: "2026-10-22"
owner: Neil Lawrence
priority: Medium
related_cips: []
status: Proposed
tags:
- backlog
- feature
- makecv
- pdf
- cvneil
title: Honour pdf true for CVs via cvneil template
---

# Task: Add a CV PDF path that matches recent pandoc + cvneil builds

## Description

Recent CVs set `pdf: true` in frontmatter. `make-cv.mk` only builds `${BASE}.docx`. The commented notes-PDF line is the talks notes template, not a CV class.

Some CVs already produce PDF outside lamd with a local pandoc makefile of the form:

```makefile
TEXINPUTS=.:$(TEXINPUTS) pandoc $< -o $@ \
  --pdf-engine=pdflatex \
  --template=/path/to/pandoc-cv-tex-template.tex
```

That template uses `\documentclass{cvneil}`. The class currently lives in the user’s CV tree, not in lamd.

## Acceptance Criteria

- [ ] When frontmatter has `pdf: true`, `makecv` / `make all` produces `${BASE}.pdf` as well as `.docx`
- [ ] PDF uses the cvneil pandoc template (or a lamd-shipped equivalent), not the notes-article template
- [ ] `cvneil.cls` is discoverable without copying it into every variant directory by hand
- [ ] CVs with `pdf: false` or omitted do not require LaTeX
- [ ] Existing user pandoc makefiles are not overwritten by this work

## Implementation Notes

The template today lives outside lamd. Either vendor a copy under `lamd/` or document a `_lamd.yml` / frontmatter key for the template path. `TEXINPUTS` must include the directory that holds `cvneil.cls`.

The `.docx` blockers are closed. `tests/unit/test_cv_makefiles.py::test_cv_compile_blockers_cleared_for_pdf_work` is the gate; `test_pdf_true_make_all_requests_cvneil_pdf` is a strict xfail for this task.

## Related

- User CV probe, 2026-10-22 (PDF pathway still open)
- Template: pandoc `cvneil` TeX template (outside this repo)
- Class: `cvneil.cls` (outside this repo)

## Progress Updates

### 2026-10-22

Confirmed `make-cv.mk` never requests a CV PDF. Existing user PDFs are from their own pandoc makefiles.

### 2026-10-22

Docx compile blockers landed. Next: satisfy `test_pdf_true_make_all_requests_cvneil_pdf`.
