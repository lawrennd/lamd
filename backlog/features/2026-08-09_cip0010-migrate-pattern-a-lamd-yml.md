---
id: "2026-08-09_cip0010-migrate-pattern-a-lamd-yml"
title: "CIP-0010 Phase 4: Migrate Pattern A diagramsdir in course configs"
status: "Ready"
priority: "Medium"
created: "2026-08-09"
last_updated: "2026-08-09"
category: "features"
related_cips: ["0010"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- paths
- migration
- mlatcl
---

# Task: CIP-0010 Phase 4 — Migrate Pattern A `diagramsdir` in course configs

## Description

Batch-fix mlatcl course `_lamd.yml` files that use `diagramsdir: ./slides/diagrams/`
with `slidesdir: ../slides/` (Pattern A in CIP-0010 audit). Update course templates so
new projects ship the consistent relative path. Talks configs already use
`../slides/diagrams/` and need no change.

## Acceptance Criteria

- [ ] All Pattern A mlatcl `_lamd.yml` files use `diagramsdir: ../slides/diagrams/`
- [ ] `course-template` and vibecourse template updated
- [ ] Spot-check: `ls` from `_lamd/` finds SVG sources under resolved `diagramsdir`
- [ ] No reliance on `copy_web_diagrams.sh` `_lamd` prepend for migrated repos (after Phase 3)

## Implementation Notes

Repos identified in CIP-0010 audit (12 configs): advds, dsa, deepnn, execed, gpss, iei,
mlphysical, r250, r255, tig, course-template, vibecourse template. mlfc already fixed.

This task can proceed in parallel with lamd code phases; it reduces PPTX/make failures
even before the full resolver lands.

## Related

- CIP: [CIP-0010](../../cip/cip0010.md) — “Observed configuration patterns” / Pattern A

## Progress Updates

### 2026-08-09

Task created from CIP-0010 implementation plan step 4 (config migration subset).
