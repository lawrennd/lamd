---
id: "2026-08-08_cip0005-testing-and-docs"
title: "CIP-0005 Phase 5: Testing and Documentation for mdpp Error Handling"
status: "Proposed"
priority: "Medium"
created: "2026-08-08"
last_updated: "2026-08-08"
category: "features"
related_cips: ["0005"]
owner: "Neil Lawrence"
dependencies: ["2026-08-08_cip0005-dependency-management"]
tags:
- backlog
- mdpp
- testing
- documentation
---

# Task: CIP-0005 Phase 5 — Testing and Documentation

## Description

Add a comprehensive test suite and user documentation for the mdpp error handling and validation improvements introduced in CIP-0005. This is the final phase before closing the CIP.

## Acceptance Criteria

- [ ] Unit tests for all validation functions in `lamd/validation.py`
- [ ] Integration tests covering include-file handling, template processing, and bibliography handling
- [ ] Error-case tests for missing files, invalid arguments, and dependency failures
- [ ] User-facing debugging guide added to docs
- [ ] Troubleshooting section added covering common failure modes
- [ ] All existing tests continue to pass

## Implementation Notes

- Tests go in `tests/test_validation.py` and `tests/test_mdpp_errors.py`
- Documentation goes in `docs/source/` (Sphinx)
- Aim for ≥ 90 % coverage of `lamd/validation.py`

## Related

- CIP: 0005
- Documentation: cip/cip0005.md

## Progress Updates

### 2026-08-08

Task created — tracking Phase 5 of CIP-0005.
