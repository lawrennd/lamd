---
id: "2026-02-03_interface-schema-compute-section"
title: "Phase 1: Define interface schema including `compute` section"
status: "Proposed"
priority: "High"
created: "2026-02-03"
last_updated: "2026-02-03"
category: "features"
related_cips: ["0006"]
owner: "Neil Lawrence"
dependencies: []
tags:
- interface
- schema
- workflow
- transparency
---

# Task: Define interface schema including `compute` section

## Description

Specify the interface file format that `lamd talk --generate` and `lamd cv --generate` will emit, so workflows are transparent and can be executed separately from configuration.

This is the core “WHAT gets written” artifact for the two-stage model.

## Acceptance Criteria

- [ ] Interface schema includes `input`, `output`, and `compute` at minimum
- [ ] `compute` can represent the key build steps (e.g. Makefile targets) at a useful granularity
- [ ] `input` can represent include dependencies (snippets/includes) well enough to support “what should I refresh?” analysis later
- [ ] Interface files are deterministic/stable (small diffs when inputs unchanged)
- [ ] Interface file can be loaded back for execution (`--execute`) without needing the original markdown flags
- [ ] Document the schema briefly in docs (link to docs task)

## Related

- CIP: 0006
- Requirement: `requirements/req0003_workflow-transparency.md`
- Cross-reference: ExecEd “material review” inventory/freshness tooling (potential downstream consumer of interface dependencies):
  - `~/mlatcl/execed/cip/cip0002.md`
  - `~/mlatcl/execed/tools/material_review/inventory.py`
  - `~/mlatcl/execed/tools/material_review/snippet_freshness.py`

## Progress Updates

### 2026-02-03

Task created to decompose CIP-0006 Phase 1 into concrete DO-work.

