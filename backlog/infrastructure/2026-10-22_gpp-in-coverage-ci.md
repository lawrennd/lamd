---
id: "2026-10-22_gpp-in-coverage-ci"
title: "Install gpp in the Documentation and Test Coverage workflow"
status: "Proposed"
priority: "Medium"
created: "2026-10-22"
last_updated: "2026-10-22"
category: "infrastructure"
related_cips: []
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- ci
- gpp
- pytest
---

# Task: Install gpp in the Documentation and Test Coverage workflow

## Description

The Python Tests workflow installs `gpp` (`apt-get` on Linux, `brew` on macOS) before running pytest. The Documentation and Test Coverage workflow (`docs.yml`, job `test-coverage`) does not. Tests that invoke `gpp` via `subprocess` therefore fail there with `FileNotFoundError` unless they skip when `shutil.which("gpp")` is `None`.

That split is why existing gpp tests carry `@pytest.mark.skipif(..., reason="gpp not available")`. A new test without the skip failed the coverage job on [PR #13](https://github.com/lawrennd/lamd/pull/13) even though Python Tests passed.

This is a CI gap, not CIP-0005. CIP-0005 Phase 4 (`2026-08-08_cip0005-dependency-management`) is about `mdpp` checking that `gpp` is present at runtime. The installer (CIP-000A) still does not install system tools.

## Acceptance Criteria

- [ ] `docs.yml` `test-coverage` installs `gpp` on Ubuntu before pytest, matching Python Tests on Linux
- [ ] Tests that call `gpp` still skip when it is missing, so local runs without `gpp` do not fail
- [ ] Coverage CI runs the gpp tests instead of skipping them
- [ ] A short note in developer or CI docs records that Python Tests and coverage both need `gpp`

## Implementation Notes

Install in `docs.yml` with the same Linux steps as `.github/workflows/python-tests.yml`:

```yaml
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y gpp
```

Keep the skipif on tests that spawn `gpp`. Coverage Ubuntu will then execute those tests; developers without `gpp` still skip.

Optional follow-up: a shared pytest marker (for example `pytest.importorskip` style helper or `pytestmark` in a `gpp` fixture) so each new gpp test does not have to remember the skip.

## Related

- PRs: [lawrennd/lamd#13](https://github.com/lawrennd/lamd/pull/13) (coverage failure; skipif workaround)
- Backlog: `2026-08-08_cip0005-dependency-management` (runtime `mdpp` checks, not CI)
- Workflows: `.github/workflows/docs.yml`, `.github/workflows/python-tests.yml`

## Progress Updates

### 2026-10-22

Task created after the Documentation and Test Coverage job failed on PR #13 (`FileNotFoundError: gpp`). PR #13 now skips those tests when `gpp` is absent; this task tracks installing `gpp` in the coverage job so they actually run there.
