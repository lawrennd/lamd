---
id: "2026-08-09_cip0010-integration-validation"
title: "CIP-0010 Phase 5: Integration validation on mlfc builds"
status: "Ready"
priority: "High"
created: "2026-08-09"
last_updated: "2026-08-09"
category: "features"
related_cips: ["0010"]
owner: "Neil Lawrence"
dependencies:
- "2026-08-09_cip0010-wire-mdpp-dependencies"
- "2026-08-09_cip0010-makefiles-copy-web-scripts"
tags:
- backlog
- paths
- testing
- integration
---

# Task: CIP-0010 Phase 5 — Integration validation on mlfc builds

## Description

Validate the full resolver + consumer changes against real course builds. Confirm
pptx, html slides, TeX notes, and web diagram copy agree on filesystem paths without
`_lamd` directory-name hacks.

## Acceptance Criteria

- [ ] `mlfc/_lamd/basis-functions-and-generalisation.pptx` builds cleanly
- [ ] HTML slides target for the same talk builds; `\diagramsDir` URLs sane for publish
- [ ] At least one TeX notes target uses `$(DIAGRAMSDIR)` end-to-end
- [ ] `copy_web_diagrams.sh` run from `_lamd` succeeds without path adjustment hack
- [ ] `dependencies batch` and markdown image paths match for the same source file
- [ ] Regression check: repo with flat `diagrams/` beside source still builds (if fixture exists)

## Implementation Notes

Document manual checklist in CIP-0010 Implementation Status when complete. Consider
adding a minimal integration fixture under `tests/integration/` if repeatable in CI.

## Related

- CIP: [CIP-0010](../../cip/cip0010.md)
- Depends on Phases 2 and 3 backlog tasks

## Progress Updates

### 2026-08-09

Task created from CIP-0010 implementation plan step 5.
