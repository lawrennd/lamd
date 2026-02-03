---
id: "2026-02-03_sphinx-doc-spec-and-cip-compression"
title: "Add Sphinx/MyST doc spec and compress closed CIPs into docs"
status: "Completed"
priority: "High"
created: "2026-02-03"
last_updated: "2026-02-03"
category: "documentation"
related_cips: ["000B"]
owner: "Neil Lawrence"
dependencies: []
tags:
- documentation
- sphinx
- myst
- compression
- vibesafe
---

# Task: Add Sphinx/MyST doc spec and compress closed CIPs into docs

## Description

Define LaMD’s formal documentation targets for VibeSafe “compression” and perform an initial compression pass for the currently closed CIPs.

This task is the DO-work that implements `CIP-000B`:

- add `.vibesafe/documentation.yml` so `whats-next` can map CIP types → doc targets
- compress the closed CIPs into stable Sphinx/MyST pages under `docs/`
- mark the compressed CIPs with `compressed: true`
- add an explicit tenet for the documentation lifecycle and compression

## Acceptance Criteria

- [x] `.vibesafe/documentation.yml` exists and points to Sphinx/MyST docs
- [x] Stable docs pages exist for compressed outcomes
- [x] Closed CIPs flagged by `whats-next` are marked `compressed: true`
- [x] `scripts/validate_vibesafe_structure.py` passes
- [x] `scripts/whats_next.py` no longer prompts to compress those closed CIPs

## Related

- CIP: 000B

## Progress Updates

### 2026-02-03

Completed initial documentation spec + compression pass.

