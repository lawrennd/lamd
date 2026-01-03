---
category: bugs
created: '2025-12-02'
dependencies: ''
github_issue: ''
id: 2025-12-02_mdlist-cvlists-path
last_updated: '2025-12-02'
owner: Neil Lawrence
priority: High
related_cips: []
status: Completed
tags:
- backlog
- mdlist
- bug
title: mdlist looks for cvlists.yml in current directory instead of lamd package
---

# Task: mdlist looks for cvlists.yml in current directory instead of lamd package

## Diagnosis

When running `mdlist` from any directory, it fails with:

```
ValueError: No configuration file found at "./cvlists.yml".
```

The issue is in `lamd/mdlist.py` at line 107:

```python
interface = Interface.from_file(user_file="cvlists.yml")[args.listtype]
```

This looks for `cvlists.yml` in the **current working directory** (`./cvlists.yml`), but the file is actually located in the **lamd config directory** at `lamd/lamd/config/cvlists.yml`.

## Expected Behavior

`mdlist` should find `cvlists.yml` in the lamd config directory (`lamd/lamd/config/cvlists.yml`) regardless of where the command is run from.

## Proposed Fix

Update `mdlist.py` to construct the path to `cvlists.yml` relative to the config directory:

```python
# Look for cvlists.yml in the lamd config directory
lamd_dir = os.path.dirname(os.path.abspath(__file__))
config_dir = os.path.join(lamd_dir, "config")
cvlists_path = os.path.join(config_dir, "cvlists.yml")
interface = Interface.from_file(user_file=cvlists_path)[args.listtype]
```

## Acceptance Criteria

- [x] `mdlist` finds `cvlists.yml` when run from any directory
- [x] `mdlist publications` works correctly for CV generation
- [x] Existing functionality is preserved

## Related

- File: `lamd/mdlist.py` line 107
- Config file: `lamd/config/cvlists.yml`
- Related backlog: `2025-12-02_mdlist-yaml-dataframe-error.md` (depends on this fix)

## Progress Updates

### 2025-12-02

Task created. Issue discovered when testing `mdlist` after fixing lynguine's `read_list` bug. The `cvlists.yml` lookup was using a relative path that only works when running from the lamd directory.

### 2025-12-02 (Completed)

Implemented fix using `__file__` to locate the config directory. The `cvlists.yml` file has been moved to `lamd/lamd/config/cvlists.yml` (alongside `interface.py`) and the code now looks for it there, regardless of the current working directory. This is more consistent with the package structure, as configuration files belong in the `config/` subdirectory.