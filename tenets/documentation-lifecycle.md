---
id: "documentation-lifecycle"
title: "Documentation Lifecycle and Compression"
status: "Active"
created: "2026-02-03"
last_reviewed: "2026-02-03"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- documentation
- governance
- compression
---

# Tenet: Documentation Lifecycle and Compression

## Tenet

**Description**: Documentation has a lifecycle. During design and implementation, CIPs and backlog items are the right place for detail because they are easy to iterate on. Once a change is implemented and validated, its key outcomes should be **compressed** into stable, user-facing documentation (Sphinx/MyST) so the current truth is easy to find without reading development history. The detailed rationale remains in the CIP, but the durable guidance belongs in the docs.

This tenet prevents documentation drift by making “compression” an explicit completion step for closed work.

**Quote**: *"Design lives in CIPs; truth lives in docs."*

**Examples**:
- Closing a CIP and updating `docs/` to reflect the new default behavior, then setting `compressed: true`
- Distilling a long performance investigation CIP into a short “how to enable fast builds” guide
- Moving stable conventions (file layout, CLI usage, common workflows) into docs rather than keeping them scattered across backlog items

**Counter-examples**:
- Leaving a CIP closed but never updating docs, so users must read old design history to learn current behavior
- Duplicating the full CIP verbatim into docs (monolithic, hard to maintain)
- Creating multiple competing “sources of truth” across README, wiki, and ad-hoc notes

**Conflicts**:
- **Speed vs. Thoroughness**: Compression takes time after code is done
- Resolution: Keep compression lightweight (bulleted outcomes, links back to the CIP) and do it as part of closure for significant changes

