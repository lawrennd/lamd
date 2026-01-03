---
category: bugs
created: '2025-07-02'
dependencies: mdpp refactor
github_issue: ''
id: 2025-07-02_macro-directory-argument-handling
last_updated: '2025-07-02'
owner: '@lawrennd'
priority: High
related_cips: []
status: Completed
tags:
- backlog
- bug
- macros
title: 'Bug: Macro Directory Argument Handling in mdpp and Makefiles'
---

# Task: Macro Directory Argument Handling in mdpp and Makefiles

## Description

After refactoring `mdpp.py` for testability, the macro directory argument (`--macros` → `--macros-path`) was not consistently updated in all Makefiles, leading to missing macro expansion and broken outputs. This caused issues with slides, posts, and other outputs that rely on macro expansion.

## Acceptance Criteria

- [x] All Makefiles use `--macros-path=$(MACROSDIR)`
- [x] Macro directory is correctly passed to `mdpp.py`
- [x] Builds expand macros correctly for all formats
- [x] No missing macro errors in output

## Implementation Notes

- Updated all Makefiles to use the new argument
- Improved error messages for missing macros
- Validated builds for slides, posts, notes, etc.

## Related

- CIP: CIP-0005
- Backlog: 2025-05-21_refactor_mdpp
- Backlog: 2025-05-22_path-handling-consistency

## Progress Updates

### 2025-07-02
Identified and fixed macro directory argument handling issues after mdpp refactor.