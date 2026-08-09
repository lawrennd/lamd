---
category: features
created: '2025-05-22'
dependencies: []
effort: Medium
github_issue: null
id: 2025-05-22_path-handling-consistency
last_updated: '2026-08-09'
owner: "Neil Lawrence"
priority: High
related_cips: ["0010"]
status: Ready
title: Standardize Path Handling Between URLs and Local Files
type: feature
---

# Task: Standardize Path Handling Between URLs and Local Files

## Description

Umbrella task for architectural path handling between URL paths and local filesystem
paths in LaMD builds. Design and audit live in [CIP-0010](../../cip/cip0010.md);
execution is split into phased backlog tasks (2026-08-09).

## Execution tasks (CIP-0010)

| Phase | Backlog task | Status |
|-------|--------------|--------|
| 1 | [2026-08-09_cip0010-paths-resolver-module](2026-08-09_cip0010-paths-resolver-module.md) | Ready |
| 2 | [2026-08-09_cip0010-wire-mdpp-dependencies](2026-08-09_cip0010-wire-mdpp-dependencies.md) | Ready |
| 3 | [2026-08-09_cip0010-makefiles-copy-web-scripts](2026-08-09_cip0010-makefiles-copy-web-scripts.md) | Ready |
| 4 | [2026-08-09_cip0010-migrate-pattern-a-lamd-yml](2026-08-09_cip0010-migrate-pattern-a-lamd-yml.md) | Ready |
| 5 | [2026-08-09_cip0010-integration-validation](2026-08-09_cip0010-integration-validation.md) | Ready |
| 6 | [2026-08-09_cip0010-compress-directory-paths-docs](2026-08-09_cip0010-compress-directory-paths-docs.md) | Proposed (after CIP close) |

Close this umbrella task when all execution tasks are complete and CIP-0010 is Closed.

## Historical context

The `copy_web_diagrams.sh` script previously detected `_lamd` cwd and prepended `../`
to `diagrams_dir` only — a localized workaround superseded by CIP-0010.

## Acceptance Criteria

- [ ] All CIP-0010 execution tasks (phases 1–6) completed
- [ ] CIP-0010 Closed and validated
- [ ] [directory-paths.md](../../docs/guides/directory-paths.md) compressed to post-implementation reference (phase 6)

## Implementation Notes

The implementation will need to:

1. Audit all path usage in:
   - Makefiles in `~/lawrennd/lamd/lamd/makefiles/`
   - Build scripts
   - Configuration files
2. Document current path usage patterns
3. Implement chosen solution
4. Update documentation
5. Add tests

## Related

- CIP: [CIP-0010: Unified Diagram Path Resolution](../../cip/cip0010.md)
- Scripts: `lamd/lamd/scripts/copy_web_diagrams.sh`
- Makefiles: All files in `lamd/lamd/makefiles/`
- Configuration: `_lamd.yml`

## Progress Updates

### 2026-08-09

Split execution into six phased backlog tasks under CIP-0010. Trimmed
[directory-paths.md](../../docs/guides/directory-paths.md) to reference-only (problem
analysis stays in CIP). Umbrella task set to Ready.

### 2025-05-22

Initial analysis of path handling issues:
- Identified inconsistent path handling between URLs and local files
- Documented current workaround in `copy_web_diagrams.sh`
- Proposed three potential solutions
- Created backlog item to track implementation