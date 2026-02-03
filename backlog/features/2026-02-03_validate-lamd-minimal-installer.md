---
id: "2026-02-03_validate-lamd-minimal-installer"
title: "Validate LaMD minimal installer in talks/ and execed/"
status: "Proposed"
priority: "Medium"
created: "2026-02-03"
last_updated: "2026-02-03"
category: "features"
related_cips: ["000A"]
owner: "Neil Lawrence"
dependencies:
- "2026-02-03_implement-lamd-minimal-installer"
tags:
- backlog
- installer
- agents
- lamd
---

# Task: Validate LaMD minimal installer in talks/ and execed/

## Description

Run the LaMD minimal installer (`lamd/scripts/install-minimal.sh`) **in real target repositories** that use LaMD (not in the LaMD repo itself) and confirm it behaves as intended:

- writes agent hints into the *current repo* (Cursor rules + agent files)
- preserves existing `.cursorrules` if present
- is idempotent (safe to re-run)
- optionally creates a dedicated venv (`.venv-lamd`) and installs `lamd` such that `maketalk` works

## Acceptance Criteria

### talks repository (`~/lawrennd/talks`)
- [ ] Running the installer from repo root creates/updates `.cursor/rules/lamd_talks.mdc`
- [ ] Existing `.cursorrules` is **not overwritten**
- [ ] `AGENTS.md` contains a `<!-- LAMD:BEGIN --> ... <!-- LAMD:END -->` block (without clobbering other content)
- [ ] `CLAUDE.md` contains a `<!-- LAMD:BEGIN --> ... <!-- LAMD:END -->` block (without clobbering other content)
- [ ] Re-running the installer produces no unexpected diffs (idempotence)

### execed repository (`~/mlatcl/execed`)
- [ ] Running the installer from repo root creates/updates `.cursor/rules/lamd_talks.mdc`
- [ ] Installer run with `--with-venv` creates `.venv-lamd/`
- [ ] With `PATH="$(pwd)/.venv-lamd/bin:$PATH"`, `maketalk` is available
- [ ] `maketalk` successfully runs from a directory containing `_lamd.yml` (sanity check)
- [ ] Re-running the installer produces no unexpected diffs (idempotence)

## Implementation Notes

- Prefer running via the published curl form:
  - `bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/lamd/main/scripts/install-minimal.sh)"`
  - For venv: `... -- --with-venv`
- The installer intentionally does **not** install system dependencies (e.g. `gpp`, `pandoc`). Verify failures are clearly attributable to missing external tools.

## Related

- CIP: 000A
- Documentation: `https://inverseprobability.com/lamd/`

## Progress Updates

### 2026-02-03

Task created to validate the retroactive CIP-000A implementation in real repos.

Dependencies:
- `2026-02-03_implement-lamd-minimal-installer`

