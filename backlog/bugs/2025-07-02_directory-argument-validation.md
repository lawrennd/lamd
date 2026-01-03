---
category: bugs
created: '2025-07-02'
dependencies: mdpp refactor
github_issue: ''
id: 2025-07-02_directory-argument-validation
last_updated: '2025-07-02'
owner: '@lawrennd'
priority: High
related_cips: []
status: Completed
tags:
- backlog
- bug
- directory-arguments
title: 'Bug: Directory Argument Validation and Expansion in mdpp.py'
---

# Task: Directory Argument Validation and Expansion in mdpp.py

## Description

Directory arguments for snippets, includes, and macros were not always validated or expanded correctly in `mdpp.py`, causing missing content and build failures. This was especially problematic after the refactor for testability.

## Acceptance Criteria

- [x] All directory arguments are validated
- [x] Missing directories are reported with clear errors
- [x] Colon-separated lists for directory arguments are supported

## Implementation Notes

- Refactored `mdpp.py` to support colon-separated lists for all directory arguments
- Added robust validation for all required directories
- Improved error messages for missing directories

## Related

- CIP: CIP-0005
- Backlog: 2025-05-21_refactor_mdpp
- Backlog: 2025-05-21_content-distribution-caching

## Progress Updates

### 2025-07-02
Refactored and validated directory argument handling in mdpp.py.