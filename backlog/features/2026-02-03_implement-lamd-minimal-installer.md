---
id: "2026-02-03_implement-lamd-minimal-installer"
title: "Implement LaMD minimal installer (agent hints + venv) to project standards"
status: "Proposed"
priority: "High"
created: "2026-02-03"
last_updated: "2026-02-03"
category: "features"
related_cips: ["000A"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- installer
- agents
- cursor
- lamd
---

# Task: Implement LaMD minimal installer (agent hints + venv) to project standards

## Description

`CIP-000A` specifies a curl-able minimal installer that can be run from the root of a LaMD-using repository (e.g. `talks/`, `execed/`) to install:

- Cursor rules for LaMD authoring/build conventions
- Agent guidance files (`AGENTS.md`, `CLAUDE.md`), updated safely via marked blocks
- Optional isolated venv (default `.venv-lamd`) that installs `lamd` so `maketalk` works

 The goal is to make the installer robust, maintainable, testable, and aligned with the “clean reinstallation” philosophy (safe to re-run; system files updated; user content preserved).

## Acceptance Criteria

### Installer script quality
- [ ] `scripts/install-minimal.sh` is explicitly documented as a **target-repo installer** (writes into `pwd`)
- [ ] Script is idempotent: reruns do not create unexpected diffs
- [ ] Script has clear, actionable error messages for missing prerequisites (without trying to install OS packages)
- [ ] Script behavior is configurable via flags (at minimum what CIP-000A enumerates)
- [ ] Installs `lamd` inside the venv (default `.venv-lamd`, configurable) and makes `maketalk` available via `PATH="$(pwd)/.venv-lamd/bin:$PATH"`
- [ ] (Optional but preferred) supports installing from a local checkout (editable install) for development workflows

### Documentation Section for Agents
- [ ] Need to add a specific documentation section for agents that operates as the source for the agent rules below.

### Agent rule installation
- [ ] Creates/updates `.cursor/rules/lamd_talks.mdc` in the target repo
- [ ] Does **not** overwrite existing `.cursorrules` (only creates it when missing) but adds to it if present
- [ ] Content is correct for LaMD authoring conventions and build execution (`maketalk`, `_lamd.yml`)
- [ ] Upserts a marked LaMD block in `AGENTS.md` (preserves everything outside the block)
- [ ] Upserts a marked LaMD block in `CLAUDE.md` (preserves everything outside the block)
- [ ] Sources these rules from the lamd documentation directly. 

### Venv bootstrap (optional)
- [ ] `--without-venv` doesn't create the venv directory 

### Maintainability / single source of truth
- [ ] The “installed content” (Cursor rules + agent blocks) is maintained in a way that avoids copy/paste drift:
  - either by downloading versioned template files from the LaMD repo, or
  - by clearly isolating templates inside the installer with strong delimiting and minimal duplication

## Implementation Notes

- Ensure **implementation quality** (robustness, portability, maintainability).
- Verification in real repos is tracked separately in:
  - `backlog/features/2026-02-03_validate-lamd-minimal-installer.md`

## Related

- CIP: 000A
- Documentation: `https://inverseprobability.com/lamd/`

## Progress Updates

### 2026-02-03

Task created to bring CIP-000A implementation up to expected project standards.

### 2026-02-03Improved the installed agent guidance content to better match how talks are authored and presented:

- Added coverage for **incremental / progressive reveal** in slides (`\slidesincremental{...}` and `\fragment{...}{type}`).
- Added coverage for **presenter-only speaker notes** in reveal.js (`\speakernotes{...}`).
- Updated all installer-emitted hint locations consistently:
  - `.cursor/rules/lamd_talks.mdc`
  - `.cursorrules` (only when missing)
  - `AGENTS.md` / `CLAUDE.md` (marked blocks)
