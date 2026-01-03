---
category: bugs
created: '2025-12-02'
dependencies: 'lynguine backlog: 2025-12-02_read-data-list-type-passes-dict'
github_issue: ''
id: 2025-12-02_mdlist-yaml-dataframe-error
last_updated: '2025-12-02'
owner: Neil Lawrence
priority: High
related_cips: []
status: Completed
tags:
- backlog
- mdlist
- bug
title: mdlist fails when using type='list' for multiple files
---

# Task: mdlist fails when using type='list' for multiple files

## Description

When running `mdlist` with multiple input files, it sets `type="list"` in the interface configuration. This causes an error because of a bug in lynguine's `read_data` function.

## Root Cause Analysis

The issue is **not in lamd** but in **lynguine**:

1. `lamd/mdlist.py` correctly sets up the interface:
   ```python
   interface["input"]["filename"] = args.file  # list of files
   interface["input"]["type"] = "list"
   ```

2. But `lynguine/access/io.py` `read_data` function passes the entire `details` dict to `read_list`:
   ```python
   elif ftype == "list":
       df = read_list(details)  # BUG: should extract filelist first
   ```

3. `read_list` expects a list of filenames, not a dict:
   ```python
   def read_list(filelist):  # expects list, gets dict
       return read_files(filelist)  # calls filelist.sort() which fails
   ```

## Resolution

Created backlog item in lynguine: `2025-12-02_read-data-list-type-passes-dict.md`

The fix should be in lynguine's `read_data` function to extract the filelist from the details dict before calling `read_list`.

## Related

- Lynguine backlog: `backlog/bugs/2025-12-02_read-data-list-type-passes-dict.md`
- File: `lynguine/access/io.py` line 1764
- Test confirms expected behavior: `lynguine/tests/test_access_io.py` line 228

## Progress Updates

### 2025-12-02

Task created. Initial diagnosis pointed to lamd, but further investigation revealed the bug is in lynguine's `read_data` function. Created proper backlog item in lynguine repository.