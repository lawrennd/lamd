---
author: "Neil Lawrence"
created: "2026-11-23"
id: "001C"
last_updated: "2026-11-23"
status: "In Progress"
compressed: false
related_requirements: []
related_cips: []
tags:
- cip
- installs
- packaging
title: "Shared install package catalog"
---

# CIP-001C: Shared install package catalog

## Status

- [ ] Proposed - Initial idea documented
- [x] Accepted - Approved, ready to start work
- [x] In Progress - Actively being implemented
- [ ] Implemented - Work complete, awaiting verification
- [ ] Closed - Verified and complete
- [ ] Rejected - Will not be implemented
- [ ] Deferred - Postponed

## Summary

Centralise the default `name → pip/uv requirement` map used by `\installcode`
and downstream repos (notably SheffieldML/notebook) in
`lamd/installs/packages.yml`, with a JSON twin for stdlib-safe loading.

## Motivation

The same package sources were duplicated in `talk-macros-code.gpp` and in
consumer CI configs. Updating pods/GPy/mlai defaults required editing multiple
repos. A shared catalog lets one change propagate; consumers keep only
profiles and temporary overrides.

## Detailed Description

### Layers

1. **Catalog** (`lamd/installs/packages.yml` + `packages.json`) — default specs.
2. **Loader** (`lamd.installs`) — resolve local files, env paths, optional remote JSON.
3. **Talk macros** — `\installcode` loads via `lamd.installs` when available, else
   packaged JSON / remote JSON / embedded fallback matching the catalog.
4. **Consumers** — e.g. notebook `installs.yml` references the catalog URL and
   applies `overrides` + per-profile `pins`.

### Resolution order (consumers)

`profile pin` > `repo overrides` > `catalog` > bare package name

### Sync rule

YAML is the editable source; JSON must match. A unit test fails if they drift.

## Implementation Plan

1. Add `lamd/installs/` catalog + loader module
2. Point `talk-macros-code.gpp` at the catalog
3. Add unit tests for load/sync
4. Document raw GitHub URLs for external consumers

## Backward Compatibility

`\installcode{library}` behaviour unchanged for known names; unknown names still
install as the bare requirement string. Duplicate `pods` key in the old dict is
collapsed to the effective git ODS source.

## Testing Strategy

- Unit tests: YAML/JSON parity, override merge, resolve_spec
- Manual: talk snippet still installs pods/GPy from catalog defaults

## Implementation Status

- [x] Catalog YAML + JSON
- [x] `lamd.installs` loader
- [x] Wire `talk-macros-code.gpp`
- [x] Unit tests
- [x] Update CIP README

## References

- Prior inline map: `lamd/macros/talk-macros-code.gpp`
- Consumer: SheffieldML/notebook CIP-0008
