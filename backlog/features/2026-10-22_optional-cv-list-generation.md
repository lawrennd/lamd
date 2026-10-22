---
category: features
created: "2026-10-22"
dependencies:
- 2026-10-22_make-lists-colon-filenames
github_issue: ""
id: 2026-10-22_optional-cv-list-generation
last_updated: "2026-10-22"
owner: Neil Lawrence
priority: Medium
related_cips: []
status: Completed
tags:
- backlog
- feature
- makecv
- make-lists
title: Do not require list generation for plain CVs
---

# Task: Make CV list generation opt-in

## Description

Some CVs are self-contained markdown: no `\include{publication-list.md}`, no generated lists. `makecv` still includes `make-lists.mk` and scans `talksdir` / `publicationsdir` / `groupdir` at makefile parse time.

That coupling is why a junk file in the talks tree blocks a short CV that never mentions talks.

After the colon-filename crash is fixed, list scanning should still be skipped unless the CV actually depends on a generated `.markdown` list.

## Acceptance Criteria

- [x] A CV with no list includes builds `.docx` without `gfind` over `talksdir` / `publicationsdir` / `groupdir`
- [x] A CV that `\include`s `publication-list.md` (or equivalent) still generates `publication-list.markdown`
- [x] Plain variants are not required to invent a full `_lamd.yml` data-source block solely to satisfy list rules
- [x] CVs that already generate publication/talk lists keep current list behaviour

## Implementation Notes

Options: include `make-lists.mk` only when the source mentions list artefacts; or keep the include but give list rules no prerequisites until those artefacts are required; or split “flags” from “scan the world”. Prefer explicit over magic — the CV file or `_lamd.yml` should show whether lists are in play.

Do not overwrite existing user pandoc makefiles as part of this task.

## Related

- User CV probe, 2026-10-22
- Blocked by: `2026-10-22_make-lists-colon-filenames.md`

## Progress Updates

### 2026-10-22

Task created from a recent user-CV probe. Those short CVs currently compile with direct pandoc on purpose.

### 2026-10-22 (Completed)

`make-lists.mk` is still included, but find runs only when a list target is built. Plain CVs that never depend on those targets do not scan data trees.
