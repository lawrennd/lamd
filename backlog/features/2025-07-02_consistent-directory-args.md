---
category: features
created: '2025-07-02'
dependencies: mdpp refactor
github_issue: ''
id: 2025-07-02_consistent-directory-args
last_updated: '2025-07-02'
owner: '@lawrennd'
priority: High
related_cips: []
status: Completed
tags:
- backlog
- feature
- build-system
title: 'Feature: Consistent Directory Argument Handling Across Build System'
---

# Task: Consistent Directory Argument Handling Across Build System

## Description

Inconsistent handling of directory arguments across Makefiles and scripts led to fragile builds and hard-to-diagnose errors. Standardizing these conventions improves maintainability and reliability.

## Acceptance Criteria

- [x] All build scripts and Makefiles use the same conventions for directory arguments
- [x] Documentation is up to date
- [x] Builds are robust and reproducible

## Implementation Notes

- Standardized use of `--macros-path`, `--snippets-path`, etc. across all Makefiles and scripts
- Updated documentation and error messages
- Validated end-to-end builds

## Related

- CIP: CIP-0005
- Backlog: 2025-05-21_refactor_mdpp
- Backlog: 2025-05-22_path-handling-consistency

## Progress Updates

### 2025-07-02
Standardized directory argument handling across the build system.