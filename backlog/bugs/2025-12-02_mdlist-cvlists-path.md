---
id: "2025-12-02_mdlist-cvlists-path"
title: "mdlist looks for cvlists.yml in current directory instead of lamd package"
status: "Proposed"
priority: "High"
created: "2025-12-02"
last_updated: "2025-12-02"
owner: "Neil Lawrence"
github_issue: ""
dependencies: ""
tags:
- backlog
- mdlist
- bug
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

This looks for `cvlists.yml` in the **current working directory** (`./cvlists.yml`), but the file is actually located in the **lamd package directory** at `lamd/lamd/cvlists.yml`.

## Expected Behavior

`mdlist` should find `cvlists.yml` in the lamd package directory regardless of where the command is run from.

## Proposed Fix

Update `mdlist.py` to construct the path to `cvlists.yml` relative to the package:

```python
# Look for cvlists.yml in the lamd package directory
lamd_dir = os.path.dirname(os.path.abspath(__file__))
cvlists_path = os.path.join(lamd_dir, "cvlists.yml")
interface = Interface.from_file(user_file=cvlists_path)[args.listtype]
```

## Acceptance Criteria

- [ ] `mdlist` finds `cvlists.yml` when run from any directory
- [ ] `mdlist publications` works correctly for CV generation
- [ ] Existing functionality is preserved

## Related

- File: `lamd/mdlist.py` line 107
- Config file: `lamd/cvlists.yml`
- Related backlog: `2025-12-02_mdlist-yaml-dataframe-error.md` (depends on this fix)

## Progress Updates

### 2025-12-02

Task created. Issue discovered when testing `mdlist` after fixing lynguine's `read_list` bug. The `cvlists.yml` lookup was using a relative path that only works when running from the lamd directory.

