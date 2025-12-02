---
id: "2025-12-02_mdlist-preprocess-filtering"
title: "mdlist filtering not working due to preprocess/Compute interface mismatch"
status: "Proposed"
priority: "Medium"
created: "2025-12-02"
---

# Task: mdlist filtering not working due to preprocess/Compute interface mismatch

## Description

The `mdlist` tool successfully generates publication lists but **filtering is not being applied** (e.g., `-s 2020` for "since year 2020" returns all publications regardless).

This is caused by a mismatch between how `mdlist` calls preprocessing and how lynguine/referia's Compute system expects to receive the interface.

### Current Workaround

In `mdlist.py`, we have a try/except block that catches the TypeError and skips preprocessing:

```python
# Preprocess the data
# Note: preprocess() may require interface but referia's CustomDataFrame
# doesn't pass it through. Try without for now.
try:
    data.preprocess()
except TypeError as e:
    # Skip preprocessing if interface argument issue
    pass
```

### Root Cause

When `data.preprocess()` is called:
1. `referia.assess.data.CustomDataFrame.preprocess()` calls `self.compute.preprocess(data=self)`
2. But `lynguine.assess.compute.Compute.preprocess()` now expects an `interface` argument
3. This causes: `TypeError: Compute.preprocess() missing 1 required positional argument: 'interface'`

This appears to be related to recent changes in how lynguine handles compute operations, where the interface needs to be passed explicitly rather than being stored in the data object.

## Impact

Without preprocessing:
- Year filters (`-s` / `--since-year`) don't work - all entries are included
- Sorters may not be applied
- Augmentors may not be applied
- Other filters (e.g., "current" vs "former") don't work

## Possible Fixes

### Option A: Fix in lamd (mdlist.py)

Pass the interface to preprocess if the method signature supports it:

```python
# Check if preprocess accepts interface argument
import inspect
sig = inspect.signature(data.preprocess)
if 'interface' in sig.parameters:
    data.preprocess(interface=interface)
else:
    data.preprocess()
```

### Option B: Fix in referia

Update `referia.assess.data.CustomDataFrame.preprocess()` to pass the interface to `Compute.preprocess()`.

### Option C: Fix in lynguine

Either:
- Make the interface argument optional in `Compute.preprocess()`
- Or store the interface in the CustomDataFrame so it can be accessed during compute

### Option D: Implement manual filtering in mdlist

Bypass the preprocess system entirely and implement basic filtering (since_year, etc.) directly in mdlist.py using pandas operations on the DataFrame.

## Acceptance Criteria

- [ ] Year filtering works: `mdlist publications -s 2020` returns only 2020+ publications
- [ ] Other filters (current/former for grants, students) work correctly
- [ ] Sorting is applied correctly
- [ ] No workaround/try-except needed in mdlist.py

## Related

- Bug chain from CV build:
  - `2025-12-02_makecv-missing-lists-include.md` (fixed)
  - `2025-12-02_mdlist-cvlists-path.md` (fixed)
  - `2025-12-02_cvlists-missing-index-field.md` (fixed)
  - This issue (current)
- Files:
  - `lamd/lamd/mdlist.py` (workaround implemented)
  - `referia/referia/assess/data.py` (calls compute.preprocess)
  - `lynguine/lynguine/assess/compute.py` (expects interface argument)
- Related to lynguine Compute system refactoring

## Progress Updates

### 2025-12-02
Task created. Issue discovered when testing `mdlist publications -s 2020` which returned all publications instead of just those from 2020 onwards. Currently working around with try/except in mdlist.py that skips preprocessing entirely. CV generation works but without filtering.

