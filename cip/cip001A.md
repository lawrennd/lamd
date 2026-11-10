---
author: "Neil D. Lawrence"
created: "2026-11-10"
id: "001A"
last_updated: "2026-11-10"
status: "Proposed"
compressed: false
effort: small
priority: medium
related_requirements: ["0005"]
related_cips: ["0018"]
tags:
  - cip
  - packaging
  - tooling
  - uv
  - poetry
  - ci
  - maintainability
title: "Migrate developer packaging from Poetry to uv"
---

# CIP-001A: Migrate developer packaging from Poetry to uv

> CIPs describe HOW to achieve requirements (WHAT).  
> Implements [REQ-0005](../requirements/req0005_fast-build-operations.md) by keeping contributor/CI install overhead proportional to what lamd actually needs (no Poetry-only workflow, no accidental heavy transitive installs).  
> Parallel to [lynguine CIP-001B](https://github.com/lawrennd/lynguine/blob/main/cip/cip001B.md) (implemented) and [referia CIP-0027](https://github.com/lawrennd/referia/blob/main/cip/cip0027.md) (proposed).

## Status

- [x] Proposed - Initial idea documented
- [ ] Accepted - Approved, ready to start work
- [ ] In Progress - Actively being implemented
- [ ] Implemented - Work complete, awaiting verification
- [ ] Closed - Verified and complete
- [ ] Rejected - Will not be implemented
- [ ] Deferred - Postponed

## Summary

Replace Poetry as lamd’s developer packaging tool with **uv**: PEP 621 `pyproject.toml`, `uv.lock`, and CI/docs that use `uv sync` / `uv run` / `uv build` instead of `poetry install` / `poetry run` / `poetry build`.

**Prerequisite:** land [CIP-0018](cip0018.md) first (or as the opening step of this work). Referia is not needed for lamd — only `mdlist` imports it, and solely for `CustomDataFrame.from_flow`, which lynguine already provides. Dropping the git-pinned referia dependency removes Jupyter/spaCy/Thinc from every lamd install and makes `uv lock` tractable.

PyPI / `pip install lamd` consumers stay on the standard packaging surface. Console scripts (`maketalk`, `mdpp`, `mdlist`, …), package data under `lamd/` (macros, templates, makefiles, includes, scripts), and docs/dev dependency groups remain.

## Motivation

Lamd still uses a Poetry-native surface while its infrastructure sibling **lynguine** has already moved to uv (CIP-001B):

- `[tool.poetry]` metadata (not PEP 621)
- `poetry.lock` + `poetry-core` build backend
- CI workflows (`python-tests.yml`, `docs.yml`, `lint.yml`) install Poetry then wrap steps in `poetry run`
- README / CONTRIBUTING prescribe `poetry install` / `poetry run pytest`
- Runtime still pins **referia** via git rev, even though CIP-0018 already decided mdlist should load through lynguine

Migrating keeps the adjacent tooling story consistent, speeds CI installs, and aligns with PEP 621. Dropping referia first (CIP-0018) is part of making that migration honest: lamd should not lock a review-and-NLP stack it does not call.

This is a **tooling** change, not a LaMD macro/API change.

## Detailed Description

### Current state

| Piece | Today |
|-------|--------|
| Metadata | `[tool.poetry]` + `[tool.poetry.dependencies]` |
| Groups | `[tool.poetry.group.dev]`, `[tool.poetry.group.docs]` |
| Scripts | `[tool.poetry.scripts]` → `mdpp`, `maketalk`, `mdlist`, … |
| Build | `poetry-core` / `poetry.core.masonry.api` |
| Package data | Poetry `include` for macros/templates/makefiles/includes/scripts (files already live under `lamd/`) |
| Lock | `poetry.lock` |
| Hard deps | Git `lynguine` (`branch = main`); git `referia` (pinned rev) |
| CI | `python-tests.yml`, `docs.yml`, `lint.yml` all Poetry |
| Docs metadata | `docs/conf.py` hard-codes name/version/author (does not read `tool.poetry`) |
| Contributor docs | README + CONTRIBUTING Poetry commands |
| Installer | `scripts/install-minimal.sh --with-venv` may assume pip/Poetry-era install |

### Target state

| Piece | After |
|-------|--------|
| Metadata | PEP 621 `[project]` |
| Dev/docs deps | `[dependency-groups]` (`dev`, `docs`) — uv’s native groups |
| Scripts | `[project.scripts]` (same entry points) |
| Build | `hatchling` (same choice as lynguine CIP-001B) |
| Package data | hatchling `packages = ["lamd"]` (macros/templates/… already inside the package tree) |
| Lock | `uv.lock` (commit); remove `poetry.lock` |
| Hard deps | Git `lynguine` only (after CIP-0018); no referia |
| CI | `astral-sh/setup-uv` + `uv sync --group …` / `uv run` / `uv build` |
| Contributor docs | `uv sync` / `uv run` wording in README + CONTRIBUTING |
| Installer | `--with-venv` path uses `uv` when available (or documented pip editable against PEP 621) |

### Design decisions

1. **CIP-0018 before (or as step 0 of) the lock.** Confirm: nothing in lamd besides `mdlist` imports referia; `mdlist` only needs `lynguine.assess.data.CustomDataFrame.from_flow` plus the existing CIP-0015 pandas filter path (and lynguine dataframe helpers named by `cvlists.yml`). Do not keep a temporary `path = "../lynguine-mdlist"` develop dependency on main — depend on published/git `lynguine` `main`.

2. **Full migration, not dual tooling.** Drop Poetry as the supported contributor path. Do not keep `poetry.lock` alongside `uv.lock` long-term.

3. **Preserve install surface for users.**
   - `pip install lamd` / `pip install git+https://github.com/lawrennd/lamd.git`
   - Editable: `pip install -e ".[…]"` still works; contributors prefer `uv sync --group dev`

4. **Map Poetry groups explicitly.**
   - Poetry `dev` / `docs` groups → `[dependency-groups]`
   - No Poetry extras today → none required unless a later CIP adds optional stacks

5. **Hatchling package layout.** Prefer shipping everything under `lamd/` via the package discovery already used at runtime. Verify wheel contents include macros, templates, makefiles, includes, and scripts (replace Poetry top-level `include` paths that do not match the on-disk tree).

6. **Git lynguine.** Express with PEP 508 / `[tool.uv.sources]` as needed; smoke `uv lock` early after referia is gone.

7. **Version and publish.** Prefer `uv build`. Lamd has no `publish.yml` today; do not invent one in this CIP unless a release workflow already exists by implementation time. Keep lint/tests/docs green.

8. **VibeSafe `.venv-vibesafe`.** Unrelated; leave the whats-next venv alone.

9. **Sibling repos.** Downstream talks/CV/execed repos that `pip install` lamd from git are unaffected if they already use pip. Poetry-based checkouts of *this* package switch to `uv sync`.

### Alternatives considered

| Approach | Why not (for this CIP) |
|----------|-------------------------|
| Keep Poetry; only add uv for CI cache speed | Two lock/tool stories; diverges from lynguine |
| Migrate to uv while still pinning referia | Locks spaCy/Jupyter into every contributor/CI env; fights REQ-0005 and CIP-0018 |
| Dual `poetry.lock` + `uv.lock` for a transition | Drift risk; CIP-001B rejected this for lynguine |
| Wait for referia CIP-0027 | Unnecessary — lamd should not depend on referia at all |

### Risks

- CIP-0018 WIP previously used a local lynguine fork for `apply_flow_dataframe_ops`. Main must land a version that works against lynguine `main` (call lynguine helpers from `mdlist` if the registry helper is not upstream yet).
- Wildcard Poetry deps (`"*"`) should become explicit loose ranges where lynguine already tightened constraints; lockfile still pins installs.
- Wheel must still contain non-Python package data or talk/CV builds break after `pip install`.
- `install-minimal.sh --with-venv` must keep working for talks/execed agent-hint installs.

## Implementation Plan

0. **Complete CIP-0018 (drop referia)**
   - Replace `from referia import assess` with `from lynguine.assess.data import CustomDataFrame`
   - Remove `referia = { git = … }` from `pyproject.toml`; keep `lynguine` on git `main`
   - Retarget unit tests; add assertion that `pyproject.toml` does not name referia
   - No path dependency on a private lynguine fork on `main`

1. **Convert `pyproject.toml`**
   - Move package metadata to `[project]`
   - Move runtime deps (git lynguine + remaining PyPI deps)
   - Move `dev` / `docs` to `[dependency-groups]`
   - Move console scripts to `[project.scripts]`
   - Set hatchling build backend and confirm package data

2. **Lock and local verify**
   - `uv lock` → commit `uv.lock`
   - Remove `poetry.lock`
   - `uv sync --group dev`
   - `uv run pytest`, `uv run maketalk --help` (or equivalent)

3. **CI workflows**
   - `python-tests.yml`: setup-uv; sync; `uv run pytest`
   - `docs.yml`: sync with docs group; `uv run` sphinx / test_build; drop `snok/install-poetry`
   - `lint.yml`: sync with dev group; `uv run` black/isort/flake8/mypy

4. **Docs and installer**
   - Update README + CONTRIBUTING Poetry commands to uv
   - Update `scripts/install-minimal.sh --with-venv` if it still assumes Poetry
   - Optionally read `[project]` from `docs/conf.py` (today it hard-codes; keep behaviour, prefer PEP 621 if touched)

5. **Smoke package path**
   - Local `uv build` + install wheel in a clean env
   - Confirm `import lamd`, console scripts, and presence of macros/templates in the installed package

## Backward Compatibility

- **LaMD macros / makefile behaviour:** unchanged.
- **`pip install lamd` / git installers:** unchanged once the wheel still ships package data.
- **Contributors:** must use uv (or plain pip against the PEP 621 project) instead of Poetry.
- **Anyone who relied on lamd pulling in referia transitively:** must depend on referia themselves. Lamd never documented that re-export.

## Testing Strategy

- CIP-0018 tests: mdlist against lynguine `CustomDataFrame.from_flow`; pyproject has no referia
- CI matrix green after workflow swap (ubuntu/macos × 3.11/3.12 as today)
- Docs workflow builds Sphinx successfully
- Local: `uv run pytest` and a smoke `maketalk` / `mdpp` invocation
- Package: `uv build`; clean-env install; import + script + package-data checks

## Related Requirements

- [REQ-0005](../requirements/req0005_fast-build-operations.md) — install and tool startup should not drag unrelated heavy stacks; dropping referia and speeding CI sync both support that outcome
- Softly supports the CIP-0018 requirements already linked there ([REQ-0002](../requirements/req0002_clear-error-messages.md), REQ-0005)

## Implementation Status

Backlog: create only after this CIP is **Accepted** (VibeSafe rule). Suggested split:

- [ ] `YYYY-MM-DD_cip001A-complete-0018-drop-referia` — finish CIP-0018 against lynguine `main`
- [ ] `YYYY-MM-DD_cip001A-pep621-uv-lock` — PEP 621 + `uv.lock`
- [ ] `YYYY-MM-DD_cip001A-ci-workflows-uv` — tests/docs/lint workflows
- [ ] `YYYY-MM-DD_cip001A-docs-installer-uv` — README/CONTRIBUTING + install-minimal.sh

Checklist:

- [ ] CIP-0018 merged: no referia import or dependency
- [ ] Convert `pyproject.toml` to PEP 621 + hatchling + dependency-groups
- [ ] Generate `uv.lock`; remove `poetry.lock`
- [ ] Update `python-tests.yml`, `docs.yml`, `lint.yml` for uv
- [ ] Update README, CONTRIBUTING, and `--with-venv` installer path
- [ ] Verify build artifacts and package data in a clean install

## References

- Pattern sibling: [lynguine CIP-001B](https://github.com/lawrennd/lynguine/blob/main/cip/cip001B.md) (Poetry → uv, implemented)
- Parallel sibling: [referia CIP-0027](https://github.com/lawrennd/referia/blob/main/cip/cip0027.md) (Poetry → uv, proposed; not a blocker)
- Prerequisite: [CIP-0018](cip0018.md) (drop referia from mdlist)
- Current packaging: `pyproject.toml`, `poetry.lock`
- CI: `.github/workflows/python-tests.yml`, `docs.yml`, `lint.yml`
- Contributor docs: `README.md`, `CONTRIBUTING.md`
- Installer: `scripts/install-minimal.sh`
- [uv documentation — projects](https://docs.astral.sh/uv/concepts/projects/)
- [PEP 621 — project metadata](https://peps.python.org/pep-0621/)
