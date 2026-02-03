---
author: "Neil Lawrence"
created: "2026-02-03"
id: "000B"
last_updated: "2026-02-03"
status: "Closed"
compressed: true
related_requirements: ["0003"]
tags:
- cip
- documentation
- process
- compression
- sphinx
- myst
title: "Sphinx/MyST documentation spec and CIP compression workflow"
---

# CIP-000B: Sphinx/MyST documentation spec and CIP compression workflow

## Summary

This CIP defines **where** LaMD’s “formal documentation” lives (Sphinx/MyST under `docs/`), and introduces a small, explicit **documentation specification** (`.vibesafe/documentation.yml`) that allows tooling (`whats-next`) to guide and verify **CIP compression** (Closed CIPs → stable documentation pages).

## Motivation

LaMD already uses Sphinx/MyST, but the governance tooling could not determine compression targets, leading to:

- repeated “compress closed CIPs” prompts without a clear place to put the compressed outcomes
- higher risk of documentation drift (stable outcomes trapped in CIPs only)
- inconsistent expectations around when work is “done”

This CIP aligns with the project’s tenets (especially *Explicit over implicit*) by making documentation targets explicit and machine-readable.

## Detailed Description

### Documentation system

- **System**: Sphinx with MyST markdown (`docs/conf.py` already enables `myst_parser`)
- **Root**: `docs/`

### Documentation specification (`.vibesafe/documentation.yml`)

We add a small YAML spec that defines:

- which documentation system is in use (`sphinx-myst`)
- where documentation lives (`docs`)
- how to build it (a hint command)
- where to compress different categories of CIPs (targets)

This spec is consumed by `scripts/whats_next.py` to group closed CIPs by compression target.

### Compression workflow

For a CIP that is **Closed**:

1. Distill the stable outcomes into the relevant Sphinx/MyST docs page(s)
2. Keep the CIP as the full design/history record
3. Mark the CIP frontmatter as `compressed: true`

This makes “current truth” easy to find without losing development context.

### Tenet support

To keep this behavior durable, we introduce an explicit tenet:

- `tenets/documentation-lifecycle.md`: **Documentation Lifecycle and Compression**

## Implementation Plan

- [x] Add `.vibesafe/documentation.yml`
- [x] Add stable doc pages to host compressed outcomes
- [x] Mark compressed CIPs with `compressed: true` after docs are updated
- [x] Add/activate tenet for the documentation lifecycle and compression

## Backward Compatibility

No user-facing breaking changes. This is documentation/governance only.

## Testing Strategy

- `scripts/validate_vibesafe_structure.py` passes
- `scripts/whats_next.py` no longer prompts to compress already-compressed closed CIPs
- (Optional) `cd docs && make html` succeeds in a docs-enabled environment

## References

- `.vibesafe/documentation.yml`
- `docs/`
- Tenet: `tenets/documentation-lifecycle.md`

## Closure Note

**Status: Closed (2026-02-03)**.

Implementation was completed as a documentation/governance change and is tracked as DO-work in:

- `backlog/documentation/2026-02-03_sphinx-doc-spec-and-cip-compression.md`

