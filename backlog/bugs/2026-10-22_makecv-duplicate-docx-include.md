---
category: bugs
created: "2026-10-22"
dependencies: []
github_issue: ""
id: 2026-10-22_makecv-duplicate-docx-include
last_updated: "2026-10-22"
owner: Neil Lawrence
priority: Medium
related_cips: []
status: Completed
tags:
- backlog
- bug
- makecv
- make-docx
title: makecv includes make-docx.mk twice
---

# Task: Include make-docx.mk only once in the CV makefile chain

## Description

`makecv.py` writes:

```makefile
include $(MAKEFILESDIR)/make-cv.mk
include $(MAKEFILESDIR)/make-docx.mk
```

`make-cv.mk` already has `include $(MAKEFILESDIR)/make-docx.mk`. Make then warns:

```
make-docx.mk:6: warning: overriding commands for target `cv.preprocessed.md'
make-docx.mk:9: warning: overriding commands for target `cv.docx'
```

Harmless once the other blockers are fixed, but it hides real errors and means the last include wins.

## Acceptance Criteria

- [x] Generated CV makefile includes `make-docx.mk` exactly once
- [x] `make ${BASE}.docx` still preprocesses then runs pandoc
- [x] No “overriding commands for target” warnings from `make-docx.mk` on a clean CV build

## Implementation Notes

Either drop the extra include from `makecv.py` (keep it in `make-cv.mk`) or stop including it from `make-cv.mk`. Prefer one place so talk/CV sharing stays obvious.

## Related

- User CV probe, 2026-10-22
- Files: `lamd/makecv.py`, `lamd/makefiles/make-cv.mk`

## Progress Updates

### 2026-10-22

Seen on every isolated `makecv` run that got as far as Make.

### 2026-10-22 (Completed)

Dropped the extra include from `makecv.py`. `make-cv.mk` remains the single include.
