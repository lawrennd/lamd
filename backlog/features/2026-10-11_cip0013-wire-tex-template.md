---
id: "2026-10-11_cip0013-wire-tex-template"
title: "Wire tex_template selection into notes PDF build"
status: "Completed"
priority: "High"
created: "2026-10-11"
last_updated: "2026-10-11"
category: "features"
related_cips: ["0013"]
owner: "Neil D. Lawrence"
dependencies: []
tags:
- backlog
- cip0013
- makefile
- pandoc
- notespdf
---

# Task: Wire tex_template into notes PDF build

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).

## Description

Extract `tex_template` from frontmatter in `make-talk-flags.mk`, default to `exercise` when `assignment` is true and unset otherwise `notes`, and use `pandoc-$(TEX_TEMPLATE)-tex-template.tex` in `make-tex.mk`.

## Acceptance Criteria

- [x] `tex_template` extracted via mdfield batch
- [x] Convenience: `assignment: True` ⇒ exercise when unset
- [x] Explicit `tex_template: notes` wins over assignment convenience
- [x] Notes PDF pandoc rule uses resolved template path

## Implementation Notes

See CIP-0013 Detailed Description / Plumbing.

## Related

- CIP: 0013

## Progress Updates

### 2026-10-11

Task created on CIP acceptance; implementing immediately.

### 2026-10-11 (later)

Implemented and validated on IEI Worksheet 1.
