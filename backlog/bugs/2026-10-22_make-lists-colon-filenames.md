---
category: bugs
created: "2026-10-22"
dependencies: []
github_issue: ""
id: 2026-10-22_make-lists-colon-filenames
last_updated: "2026-10-22"
owner: Neil Lawrence
priority: High
related_cips: []
status: Completed
tags:
- backlog
- bug
- makecv
- make-lists
- talks
title: make-lists.mk crashes Make when talksdir contains colon filenames
---

# Task: Stop make-lists.mk treating every talks-tree file as a Make prerequisite

## Description

`make-cv-flags.mk` sets:

```makefile
TALKLISTFILES=$(shell ${FIND} ${TALKSDIR} -type f)
```

`make-lists.mk` then uses that expansion as prerequisites:

```makefile
invited-talk-list.markdown: ${TALKLISTFILES}
	mdlist talks $^ -o $@ -s ${TALKSINCE}
```

GNU Make treats `:` in a prerequisite as a static-pattern separator. A file in the talks tree named with a URL path:

`talks/_notebooks/https:/example.com/path/file.gif`

causes:

```
make-lists.mk:1: *** multiple target patterns.  Stop.
```

This fires at **makefile parse time**, before any CV content is built. It blocks every `makecv` run, including CVs that do not include a talk list.

The same `gfind -type f` also pulls ~23k files (logs, images, binaries). Empty `TALKSDIR` makes `gfind` search `.`.

This became a CV blocker when `makecv` started including `make-lists.mk` (completed task `2025-12-02_makecv-missing-lists-include`).

## Acceptance Criteria

- [x] `make -n all` on a CV makefile succeeds even when `talksdir` contains a filename with a colon
- [x] Talk/publication/group list sources are `*.md` discovered at recipe time, not Make prerequisites
- [x] Empty or unset `TALKSDIR` / `PUBLICATIONSDIR` / `GROUPDIR` does not make `gfind` search the CV directory
- [x] Existing CVs that include `publication-list.markdown` / `invited-talk-list.markdown` still have a way to rebuild those lists
- [x] Unit or makefile test covers a colon in a dummy talks tree

## Implementation Notes

Do not pass raw `find` output into Make's prerequisite list. Narrow the glob (markdown sources only) and/or use a stamp file that `mdlist` rebuilds from a file list written to disk.

`PUBLICATIONLISTFILES` and `GROUPLISTFILES` use the same pattern; fix all three.

## Related

- User CV probe, 2026-10-22
- Completed: `2025-12-02_makecv-missing-lists-include.md` (this include made the crash reachable)
- Follow-on: `2026-10-22_optional-cv-list-generation.md`

## Progress Updates

### 2026-10-22

Found while compiling isolated copies of recent user CVs. Original artefacts were not overwritten.

### 2026-10-22 (Completed)

List rules now find `*.md` in the recipe. Empty/unset dirs skip find. Tests in `tests/unit/test_cv_makefiles.py`.
