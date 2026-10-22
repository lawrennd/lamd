---
category: bugs
created: "2026-10-22"
dependencies:
- 2026-10-22_make-lists-colon-filenames
github_issue: ""
id: 2026-10-22_cv-missing-check-reference-docs
last_updated: "2026-10-22"
owner: Neil Lawrence
priority: High
related_cips: ["0005"]
status: Proposed
tags:
- backlog
- bug
- makecv
- make-docx
- flags
title: CV makefile chain has no check-reference-docs target
---

# Task: Define check-reference-docs on the CV flag chain

## Description

`make-docx.mk` requires `check-reference-docs` before preprocessing:

```makefile
${BASE}.preprocessed.md: ${BASE}.md ${DEPS} check-reference-docs
```

That phony target lives only in `make-talk-flags.mk` (added 2026-08-09 with `resolve_reference_doc()`). `makecv` includes `make-cv-flags.mk`, not the talk flags, so CV builds fail with:

```
No rule to make target `check-reference-docs', needed by `….preprocessed.md'.
```

This is the second failure after the `make-lists.mk` parse crash. It is leftover from lamd CIP-0005 Phase 4 template-path validation, which was exercised on talks/PPTX, not CVs.

## Acceptance Criteria

- [ ] `make-cv-flags.mk` defines `check-reference-docs` (share with talk flags, do not duplicate logic ad hoc)
- [ ] A CV makefile that includes `make-cv-flags.mk` + `make-docx.mk` can run `make ${BASE}.docx` without a missing-target error
- [ ] Missing `dotx` still fails fast with the existing “reference template not found” message
- [ ] Talk builds keep the same check

## Implementation Notes

Extract the target to a shared snippet, or copy the block into `make-cv-flags.mk` to match `NOTATION` already being defaulted there.

Depends on the lists crash being fixed, or tests must use a talks tree without colons.

## Related

- CIP: 0005 (mdpp validation; Phase 4 template paths)
- Completed: `2026-08-09_reference-doc-template-resolution.md`
- User CV probe, 2026-10-22

## Progress Updates

### 2026-10-22

Confirmed in isolated copies of recent user CVs after pointing `talksdir` at an empty directory.
