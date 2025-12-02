---
id: "2025-12-02_makecv-missing-lists-include"
title: "makecv doesn't include make-lists.mk for publication/talk list generation"
status: "In Progress"
priority: "High"
created: "2025-12-02"
last_updated: "2025-12-02"
owner: "Neil Lawrence"
github_issue: ""
dependencies: ""
tags:
- backlog
- makecv
- makefiles
---

# Task: makecv missing make-lists.mk include

## Description

The `makecv` tool generates a makefile that includes `make-cv-flags.mk` and `make-cv.mk`, but does **not** include `make-lists.mk`. This means that CVs cannot automatically generate:

- `publication-list.markdown` (from publications data)
- `invited-talk-list.markdown` (from talks data)
- `meetings-organised-list.markdown` (from meetings data)
- `current-grant-list.markdown` (from grants data)
- `phd-list.markdown` (from group data)
- And other dynamic lists defined in `make-lists.mk`

When a CV includes `\include{publication-list.md}` which in turn includes `publication-list.markdown`, the build fails because the `.markdown` file doesn't exist and there's no make target to generate it.

## Current Behaviour

`makecv.py` generates:

```makefile
include $(MAKEFILESDIR)/make-cv-flags.mk
include $(MAKEFILESDIR)/make-cv.mk
```

## Expected Behaviour

The generated makefile should also include `make-lists.mk`:

```makefile
include $(MAKEFILESDIR)/make-cv-flags.mk
include $(MAKEFILESDIR)/make-lists.mk
include $(MAKEFILESDIR)/make-cv.mk
```

## Acceptance Criteria

- [ ] `makecv.py` includes `make-lists.mk` in generated makefile
- [ ] Running `makecv cv.md` with a CV that includes `publication-list.md` works without manual intervention
- [ ] All list types (publications, talks, meetings, grants, students, etc.) can be generated automatically
- [ ] Existing CVs continue to work (backward compatible)

## Implementation Notes

The fix is straightforward - add one line to `makecv.py`:

```python
f.write("include $(MAKEFILESDIR)/make-lists.mk\n")
```

This should be added between `make-cv-flags.mk` and `make-cv.mk` includes.

## Related

- File: `lamd/makecv.py` (line ~61)
- File: `lamd/makefiles/make-lists.mk`
- File: `lamd/makefiles/make-cv-flags.mk` (defines PUBLICATIONLISTFILES, etc.)

## Progress Updates

### 2025-12-02

Task created. Issue discovered while attempting to add publication list to Sheffield visiting professor CV.

