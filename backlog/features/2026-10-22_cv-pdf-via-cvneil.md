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

`corporate/` and `no10/` already produce PDF outside lamd:

```makefile
TEXINPUTS=../corporate/:$(TEXINPUTS) pandoc $< -o $@ \
  --pdf-engine=pdflatex \
  --template=$(HOME)/lawrennd/publications/papers/pandoc/_templates/pandoc-cv-tex-template.tex
```

That template uses `\documentclass{cvneil}`. The class currently lives beside the corporate variant, not in lamd.

CV CIP-0005 still has “Verify PDF generation pathway” unchecked.

## Acceptance Criteria

- [ ] When frontmatter has `pdf: true`, `makecv` / `make all` produces `${BASE}.pdf` as well as `.docx`
- [ ] PDF uses the cvneil pandoc template (or a lamd-shipped equivalent), not the notes-article template
- [ ] `cvneil.cls` is discoverable without copying it into every variant directory by hand
- [ ] CVs with `pdf: false` or omitted do not require LaTeX
- [ ] Existing `no10/` and `corporate/` pandoc makefiles are not overwritten by this work

## Implementation Notes

The template today lives in the publications repo. Either vendor a copy under `lamd/` (so CV builds do not depend on publications) or document a `_lamd.yml` / frontmatter key for the template path. `TEXINPUTS` must include the directory that holds `cvneil.cls`.

This is HOW for CIP-0005's remaining “verify PDF” item. It can stay a backlog feature until the `.docx` blockers are closed.

## Related

- CV CIP-0005 (PDF pathway still open)
- Template: `publications/papers/pandoc/_templates/pandoc-cv-tex-template.tex`
- Class: `cv/corporate/cvneil.cls` (and older `cv/tex/*/cvneil.cls`)

## Progress Updates

### 2026-10-22

Confirmed `make-cv.mk` never requests a CV PDF. Corporate/no10 PDFs are from their own makefiles.
