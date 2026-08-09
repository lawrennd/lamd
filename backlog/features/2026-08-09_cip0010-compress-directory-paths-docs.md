---
id: "2026-08-09_cip0010-compress-directory-paths-docs"
title: "CIP-0010 Phase 6: Compress directory-paths guide after closure"
status: "Proposed"
priority: "Medium"
created: "2026-08-09"
last_updated: "2026-08-09"
category: "documentation"
related_cips: ["0010"]
owner: "Neil Lawrence"
dependencies:
- "2026-08-09_cip0010-integration-validation"
tags:
- backlog
- paths
- documentation
- compression
---

# Task: CIP-0010 Phase 6 — Compress directory-paths guide after closure

## Description

After CIP-0010 is closed and validated, update [directory-paths.md](../../docs/guides/directory-paths.md)
to reflect **implemented** semantics only: `diagramsdir` as filesystem root,
`diagramsurl` / `diagramswebpath` for web, resolver behaviour, and migration notes
as stable user guidance. Problem analysis and audit patterns remain in the CIP only.

## Acceptance Criteria

- [ ] `docs/guides/directory-paths.md` documents post-CIP-0010 field semantics
- [ ] `diagramswebpath` documented when implemented
- [ ] Checklist updated for new resolver error messages
- [ ] No duplicate of CIP motivation, audit table, or “design debt” sections in docs
- [ ] CIP-0010 marked `compressed: true` after doc update

## Implementation Notes

Follow documentation lifecycle: design in CIP, durable reference in docs. Do not start
until integration validation passes and CIP status is Closed.

## Related

- CIP: [CIP-0010](../../cip/cip0010.md)
- Guide: [directory-paths.md](../../docs/guides/directory-paths.md)

## Progress Updates

### 2026-08-09

Task created; deferred until CIP-0010 closure (compression phase).
