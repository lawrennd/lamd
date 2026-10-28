---
id: "2026-10-28_cip0017-make-slides-pdf"
title: "Add Beamer slides PDF rules to make-tex.mk"
status: "Completed"
priority: "High"
created: "2026-10-28"
last_updated: "2026-10-28"
category: "features"
related_cips: ["0017"]
owner: "Neil D. Lawrence"
dependencies: ["2026-10-28_cip0017-slides-tex-macros"]
tags:
- backlog
- cip0017
- makefile
- pandoc
- beamer
---

# Task: Makefile rules for slides PDF

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).

## Description

Add `%.slides.tex.markdown`, `${BASE}.slides.tex`, and `${BASE}.slides.pdf` to `make-tex.mk`, mirroring notes PDF: mdpp slides/tex, percent-width sed, pandoc `-t beamer --slide-level 2`, pdflatex, copy to `${SLIDESDIR}/${OUT}.slides.pdf`.

## Acceptance Criteria

- [ ] `make ${BASE}.slides.pdf` is a defined rule
- [ ] Pandoc is invoked with `-t beamer --slide-level 2`
- [ ] Percent figure widths are rewritten for TeX
- [ ] Built PDF is copied to SLIDESDIR with the usual OUT prefix

## Implementation Notes

See CIP-0017 makefile sketch. Create SLIDESDIR if missing before copy.

## Related

- CIP: 0017

## Progress Updates

### 2026-10-28

Task created after CIP-0017 was accepted.
