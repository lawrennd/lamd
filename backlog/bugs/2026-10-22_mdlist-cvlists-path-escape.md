---
category: bugs
created: "2026-10-22"
dependencies: []
github_issue: ""
id: 2026-10-22_mdlist-cvlists-path-escape
last_updated: "2026-10-22"
owner: Neil Lawrence
priority: High
related_cips: []
status: Completed
tags:
- backlog
- bug
- mdlist
- cvlists
title: mdlist cannot load package cvlists.yml from a CV working directory
---

# Task: mdlist cannot load package cvlists.yml from a CV working directory

## Description

`mdlist` locates `lamd/config/cvlists.yml` via `__file__` and passes that absolute path to `Interface.from_file(user_file=cvlists_path)`. lynguine confines config files to the current working directory. A CV build therefore dies with `PathEscapeError` as soon as a generated list (for example `publication-list.markdown`) is required.

This is the remaining blocker for CVs that `\include{}` list snippets. Plain markdown CVs do not hit `mdlist`.

## Acceptance Criteria

- [x] `mdlist` loads package `cvlists.yml` when the working directory is not the lamd package
- [x] A test fails if that load raises `PathEscapeError`
- [x] A CV that includes `publication-list.md` can generate `publication-list.markdown`

## Implementation Notes

Pass `directory` as the package `config/` directory and `allowed_roots` including that directory, rather than an absolute `user_file` joined onto `.`.

## Related

- Backlog: `2025-12-02_mdlist-cvlists-path.md` (package path without lynguine confinement)
- PR: 19

## Progress Updates

### 2026-10-22

Found while compiling an include-based CV against the compile-blocker branch. Plain CVs built; list generation did not.

`load_cvlists_interface()` now passes `directory` and `allowed_roots` as the package `config/` directory. `test_load_cvlists_interface_from_other_cwd` is the regression test. Isolated include-based CV then produced `.docx` including the generated publication list.
