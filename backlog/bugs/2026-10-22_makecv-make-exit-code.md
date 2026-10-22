---
category: bugs
created: "2026-10-22"
dependencies: []
github_issue: ""
id: 2026-10-22_makecv-make-exit-code
last_updated: "2026-10-22"
owner: Neil Lawrence
priority: High
related_cips: []
status: Proposed
tags:
- backlog
- bug
- makecv
- exit-code
title: makecv reports success when Make fails
---

# Task: Propagate Make's exit code from makecv

## Description

`lamd/makecv.py` ends with:

```python
exit_code = os.system("make all")
return exit_code
```

`os.system` returns a wait status (`exit_code << 8` on Unix). `sys.exit(512)` (Make's exit 2) is truncated to 0. `python -m lamd.makecv …` therefore exits 0 after:

```
make-lists.mk:1: *** multiple target patterns.  Stop.
```

The same pattern should be checked in `maketalk` if it also uses `os.system("make …")`.

## Acceptance Criteria

- [ ] When `make all` fails, `makecv` exits non-zero (typically Make's 2)
- [ ] When `make all` succeeds, `makecv` exits 0
- [ ] Unit or integration test asserts a failing makefile is not reported as success
- [ ] `maketalk` matches if it has the same `os.system` wait-status bug

## Implementation Notes

Prefer `subprocess.run(..., check=False).returncode` over `os.system`. Do not `sys.exit` a wait status.

## Related

- CV CIP-0005 (2026-10-22 probe)
- File: `lamd/makecv.py`

## Progress Updates

### 2026-10-22

Observed during the recent-CV probe: wrapper `python_exit=0` while Make had already stopped.
