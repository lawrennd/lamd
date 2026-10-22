---
id: "2026-10-11_hardcoded-includes-path-notes-tex"
title: "Notes/paper TeX rules hardcode ../_includes instead of INCLUDESDIR"
status: "Completed"
priority: "High"
created: "2026-10-11"
last_updated: "2026-10-11"
category: "bugs"
related_cips: ["0010"]
owner: "Neil D. Lawrence"
dependencies: []
tags:
- backlog
- bug
- makefile
- includes
- notespdf
- cip0010
---

# Bug: Hardcoded `../_includes` in notes/paper TeX pandoc rules

## Description

`make-tex.mk` and `make-paper.mk` pass pandoc before-body includes as:

```makefile
-B ../_includes/${NOTATION}
```

`maketalk` / `makecv` already set `INCLUDESDIR` to the package includes tree
(`lamd/includes/`, which ships `talk-notation.tex`). Modules that do not keep a
local `../_includes/` directory (e.g. IEI `_lamd/` under VibeCourse) fail when
building notes PDF:

```
pandoc: ../_includes/talk-notation.tex: openBinaryFile: does not exist
```

The same failure was noted during CIP-0010 integration validation for
`*.include.tex` under mlfc layout.

`make-cv-flags.mk` already defaults `NOTATION=talk-notation.tex`; talk flags
leave `NOTATION` empty when frontmatter / `_lamd.yml` omit it, which compounds
the broken path.

## Acceptance Criteria

- [x] `make-tex.mk` notes and include TeX rules use `-B ${INCLUDESDIR}/${NOTATION}`
- [x] `make-paper.mk` paper TeX rule uses `-B ${INCLUDESDIR}/${NOTATION}`
- [x] Empty `NOTATION` in `make-talk-flags.mk` defaults to `talk-notation.tex`
- [x] No remaining `../_includes/${NOTATION}` in `lamd/makefiles/`
- [x] Notes TeX recipe resolves `-B` to package `includes/talk-notation.tex`
      without a local `_includes/` (confirmed via `make -n` in IEI `_lamd/`)

## Implementation Notes

- Prefer `${INCLUDESDIR}` (set in generated makefile by `maketalk` / `makecv`)
  over any relative project path.
- Mirror the CV flags default for `NOTATION` so `-B` always names a real file
  under package includes unless the author overrides `notation:`.

## Related

- CIP: 0010 (directory-path consistency; residual hardcoded include root)
- Discovered via: IEI worksheet notes PDF
  (`intro-history-entropy-shannon-practical.md`, 2026-10-11)
- Earlier note: `backlog/features/2026-08-09_cip0010-integration-validation.md`

## Progress Updates

### 2026-10-11

Bug filed from IEI practical notes-PDF failure.

Fixed: `make-tex.mk` and `make-paper.mk` use `${INCLUDESDIR}/${NOTATION}`;
`make-talk-flags.mk` defaults empty `NOTATION` to `talk-notation.tex`.
`make -n …notes.pdf` in IEI `_lamd/` shows
`-B …/lamd/includes/talk-notation.tex` (no `../_includes`). Full PDF may
still hit unrelated bib/`mdfield` issues in that environment.
