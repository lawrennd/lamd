---
category: features
created: '2025-07-08'
dependencies: mdpp, Makefile integration
github_issue: ''
id: 2025-07-08_format-flags-global-vars
last_updated: '2025-07-08'
owner: '@lawrennd'
priority: High
related_cips: []
status: Completed
tags:
- backlog
- bugfix
- mdpp
- build-system
title: 'Fix: Ensure Global Format Flags (-DNOTES, -DSLIDES, etc.) Are Passed to mdpp'
---

# Task: Ensure Global Format Flags Are Passed to mdpp

## Description

Previously, global format flags such as `-DNOTES` and `-DSLIDES` were not reliably passed to the preprocessor (`mdpp`) from the Makefile targets. This led to missing or incorrect macro expansion in generated outputs (e.g., notes/slides HTML, TeX, DOCX, PPTX, IPYNB). The fix ensures that all relevant format flags (`-DNOTES`, `-DSLIDES`, `-DHTML`, `-DTEX`, `-DDOCX`, `-DPPTX`, `-DIPYNB`) are set based on the `--format` and `--to` arguments in `mdpp.py`, making macro conditionals work as intended in all output formats.

## Acceptance Criteria

- [x] `-DNOTES=1` is set for notes format
- [x] `-DSLIDES=1` is set for slides format
- [x] Output format flags (`-DHTML=1`, `-DTEX=1`, `-DDOCX=1`, `-DPPTX=1`, `-DIPYNB=1`) are set as appropriate
- [x] All Makefile targets produce correct macro expansion in output
- [x] Tests verify correct flag propagation

## Implementation Notes

- Updated `setup_gpp_arguments` in `mdpp.py` to set all relevant format and output flags
- Added/updated tests to verify flag propagation
- No changes required to Makefile `PPFLAGS` usage; flags are now handled by mdpp argument parsing
- Linked to ongoing work in CIP-0005 (mdpp error handling and validation)

## Related

- CIP: CIP-0005
- PRs: []
- Documentation: [LaMD Documentation](https://inverseprobability.com/lamd)

## Progress Updates

### 2025-07-08
Fixed global format flag propagation in mdpp and verified with new and existing tests. All output formats now receive correct macro flags for conditional expansion.