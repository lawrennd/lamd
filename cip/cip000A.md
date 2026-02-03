---
author: "lawrennd"
created: "2026-02-03"
id: "000A"
last_updated: "2026-02-03"
status: "In Progress"
compressed: false
related_requirements: []
related_cips: []
tags:
- cip
- installer
- tooling
- agents
- cursor
title: "LaMD minimal installer for agent hints and local venv"
---

# CIP-000A: LaMD minimal installer for agent hints and local venv

> **Note**: This CIP is retroactive. The implementation exists; this document captures the rationale and design choices and defines the remaining verification steps.

## Status

- [x] Proposed - Initial idea documented
- [x] Accepted - Approved, ready to start work
- [x] In Progress - Actively being implemented
- [ ] Implemented - Work complete, awaiting verification
- [ ] Closed - Verified and complete
- [ ] Rejected
- [ ] Deferred

## Summary

Provide a **curl-able minimal installer** that an agent (or a human) can run from the root of a repository that *uses* LaMD (e.g. `talks/`, `execed/`) to populate:

- local **Cursor rule(s)** with LaMD authoring/build guidance
- minimal **agent hint files** (`AGENTS.md`, `CLAUDE.md`)
- optional **local virtual environment** that installs `lamd` so `maketalk` works without relying on system Python packaging

This is implemented as `scripts/install-minimal.sh` in the LaMD repo and intended to be run via:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/lamd/main/scripts/install-minimal.sh)"
```

## Motivation

Repositories that use LaMD (talks, lecture notes, exec-ed sites) often need:

- **Agent-context hints** for tools like Cursor / Codex / Claude Code
- A consistent, reproducible way to ensure the `maketalk` entrypoint is available
- A lightweight “drop-in” installer that is safe to re-run and doesn’t require repo-specific manual setup

Placing these hints directly inside the LaMD Python package repository is not helpful to end users; the hints must be installed **into the target repository** where the agent is working.

## Detailed Description

### Installer behavior (high level)

The installer (`scripts/install-minimal.sh`) is designed to be executed from a *target* repo root and will:

1. **Write/update Cursor rule(s)** into:
   - `.cursor/rules/lamd_talks.mdc`

2. **Create `.cursorrules` only if missing**
   - This avoids clobbering repo-specific Cursor configuration (e.g. `talks/.cursorrules` already exists and is richer/more tailored).

3. **Upsert LaMD blocks into `AGENTS.md` and `CLAUDE.md`**
   - Blocks are delimited by `<!-- LAMD:BEGIN -->` and `<!-- LAMD:END -->`
   - If the markers exist, the installer replaces only the marked section
   - If the markers do not exist, it appends the block

4. **Optional venv bootstrap** (enabled by `--with-venv`)
   - Creates a venv (default directory `.venv-lamd`, configurable via `--venv-dir`)
   - Installs/updates `lamd` inside that venv so `maketalk` is available

### Why this design

- **Idempotent**: safe to re-run; avoids rewriting unchanged files.
- **Locality**: everything is installed into the target repo, not into the LaMD repo.
- **Non-prescriptive**: doesn’t attempt to install system-level dependencies (e.g. `gpp`, `pandoc`) because those are OS/package-manager concerns.
- **Agent-friendly**: provides short, actionable guidance near where agents look (`.cursor/rules`, `AGENTS.md`, `CLAUDE.md`).

### Non-goals / explicit exclusions

- Installing OS packages (brew/apt) automatically.
- Enforcing a single repo layout for LaMD content.
- Modifying existing `.cursorrules` content when it already exists.

## Implementation Plan

1. Add `scripts/install-minimal.sh` to LaMD repository.
2. Ensure it writes target-repo files (`.cursor/rules/*`, `AGENTS.md`, `CLAUDE.md`) relative to `pwd`.
3. Make venv optional and isolated (default `.venv-lamd`).
4. Document usage in `README.md`.

## Backward Compatibility

- **No breaking changes** to existing LaMD users.
- Target repos with existing `.cursorrules` are preserved.
- Existing `AGENTS.md` / `CLAUDE.md` content is preserved outside the marked block.

## Testing Strategy

- **Static**:
  - `bash -n scripts/install-minimal.sh`

- **Behavioral (manual verification)**:
  - In `~/lawrennd/talks`:
    - run installer (no venv) and confirm `.cursor/rules/lamd_talks.mdc` created/updated
    - confirm `.cursorrules` is not overwritten
    - confirm `AGENTS.md` and `CLAUDE.md` get a marked LaMD block
    - re-run installer and confirm idempotence (no unexpected diffs)
  - In `~/mlatcl/execed`:
    - run installer with `--with-venv`
    - verify `PATH="$(pwd)/.venv-lamd/bin:$PATH" maketalk some.md` works from a directory containing `_lamd.yml`

## Implementation Status

- Implementation and verification are tracked as DO-work in backlog:
  - `backlog/features/2026-02-03_implement-lamd-minimal-installer.md`
  - `backlog/features/2026-02-03_validate-lamd-minimal-installer.md`

## References

- LaMD docs: `https://inverseprobability.com/lamd/`
- Entry points (pyproject): `maketalk`, `mdpp`, `mdfield`, `mdpeople`
- Examples of LaMD-using repos:
  - `~/lawrennd/talks`
  - `~/mlatcl/execed`
