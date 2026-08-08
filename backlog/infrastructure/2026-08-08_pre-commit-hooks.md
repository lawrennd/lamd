---
id: "2026-08-08_pre-commit-hooks"
title: "Add pre-commit hooks for black, isort, and mypy"
status: "Proposed"
priority: "Medium"
created: "2026-08-08"
last_updated: "2026-08-08"
category: "infrastructure"
related_cips: []
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- linting
- developer-experience
---

# Task: Add pre-commit hooks for black, isort, and mypy

## Description

Several CI lint failures during development could have been caught locally before
pushing, saving repeated push-wait-fix cycles. Adding pre-commit hooks for the
formatters and type checker would catch these errors at the right point: before
the commit lands, not after CI runs.

The CI pipeline runs black, isort, mypy (blocking), and flake8 (non-blocking).
Pre-commit hooks should mirror the blocking checks.

## Acceptance Criteria

- [ ] `pre-commit` is added as a dev dependency in `pyproject.toml`
- [ ] `.pre-commit-config.yaml` is created at the repo root
- [ ] `black` runs on staged Python files and blocks commit on failure
- [ ] `isort` runs on staged Python files and blocks commit on failure
- [ ] `mypy` runs as a pre-push hook (not pre-commit, to keep commits fast)
- [ ] Developer setup instructions note `pre-commit install` and `pre-commit install --hook-type pre-push`
- [ ] Hooks match the CI configuration (same flags, same mypy strictness)

## Implementation Notes

Use the [pre-commit framework](https://pre-commit.com). A minimal
`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: stable
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: stable
    hooks:
      - id: isort
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: stable
    hooks:
      - id: mypy
        args: [--strict, --ignore-missing-imports, --disallow-untyped-defs, --disallow-incomplete-defs]
        stages: [pre-push]
        additional_dependencies: [types-PyYAML]
```

Key decisions:
- `black` and `isort` on `pre-commit` (fast, auto-fixable)
- `mypy` on `pre-push` (slower, depends on full module graph)
- `flake8` intentionally omitted from pre-commit — CI runs it `--exit-zero`,
  so it is advisory. Fix the underlying issues rather than add a noisy hook.
- Pin `rev` values to specific tags (not `stable`) once working, for
  reproducibility.

## Related

- PRs: —
- Documentation: `.github/workflows/lint.yml` for the CI configuration to mirror

## Progress Updates

### 2026-08-08

Task created after repeated push/wait/fix cycles for black, isort, and mypy
errors that pre-commit hooks would have caught locally.
