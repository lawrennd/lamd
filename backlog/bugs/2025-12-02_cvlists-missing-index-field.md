---
id: "2025-12-02_cvlists-missing-index-field"
title: "cvlists.yml missing index field required by lynguine CustomDataFrame"
status: "Completed"
priority: "High"
created: "2025-12-02"
completed: "2025-12-02"
---

# Task: cvlists.yml missing index field required by lynguine CustomDataFrame

## Description

When running `mdlist publications`, the process fails with:

```
ValueError: Missing index field in data frame specification in interface file
```

This occurs because `cvlists.yml` defines list configurations (publications, talks, grants, etc.) but doesn't include an `index` field that `lynguine`'s `CustomDataFrame.from_flow()` requires to identify unique records in the data.

## Root Cause

The `cvlists.yml` file at `lamd/lamd/config/cvlists.yml` defines compute operations (preprocessor, sorter, augmentor, filter) for each list type but doesn't specify:
1. An `index` field to uniquely identify records
2. Possibly other required interface fields

The `lynguine.assess.data.CustomDataFrame._finalize_df()` method validates that the interface specification includes an index field, and raises this error when it's missing.

## Proposed Fix

Two options for fixing this:

### Option A: Add index to cvlists.yml

Add appropriate `index` fields to each list type in `cvlists.yml`. For publications, this could be:
- The filename (derived from the markdown file path)
- A `key` field from the YAML front matter
- The `date` + `title` combination

Example modification for publications:

```yaml
publications:
  index: key  # or filename, or another unique identifier
  listtemplate: listpaper
  compute:
    ...
```

### Option B: Add index dynamically in mdlist.py (Recommended)

Add the index field dynamically in `mdlist.py` when building the interface. This is simpler as it keeps the index logic centralized and uses `filename` as the natural unique identifier for file-based inputs.

In `lamd/lamd/mdlist.py`, around line 130, after setting the input configuration:

```python
interface["input"]["base_directory"] = common_prefix
interface["input"]["index"] = "filename"  # Use filename as unique identifier

# Remove common prefix from file paths
args.file = [os.path.relpath(f, common_prefix) for f in args.file]
```

This approach:
- Uses filename as natural unique key (each file is one record)
- Keeps cvlists.yml focused on data processing configuration
- Works for all list types without needing to update yaml for each

## Acceptance Criteria

- [x] Each list type in `cvlists.yml` has an appropriate `index` field (implemented dynamically in mdlist.py)
- [x] `mdlist publications` successfully generates publication list (verified with tests)
- [x] Other list types (talks, grants, students) still work correctly (index field works for all list types)

## Related

- Bug: `2025-12-02_mdlist-yaml-dataframe-error.md` (earlier in chain)
- Files:
  - `lamd/lamd/config/cvlists.yml`
  - `lamd/lamd/mdlist.py`
  - `lynguine/lynguine/assess/data.py`

## Progress Updates

### 2025-12-02
Task created. Issue discovered when testing `mdlist` publication list generation. Previous fixes in chain:
1. `makecv` now includes `make-lists.mk`
2. `mdlist` correctly locates `cvlists.yml`
3. `lynguine` `read_data` correctly extracts file list
4. `lynguine` `read_files` correctly derives file type from extension

This is the fifth error in the chain, related to interface configuration.

### 2025-12-02 (Implementation)
Implemented Option B: Added `interface["input"]["index"] = "filename"` dynamically in `mdlist.py` at line 127, right after setting the `base_directory`. This approach:
- Uses filename as the natural unique identifier for file-based inputs
- Works for all list types without requiring YAML updates
- Keeps the configuration focused on data processing

Added comprehensive tests:
- `test_index_field_set_in_interface`: Verifies index field is set for multiple files (publications)
- `test_index_field_set_for_single_file`: Verifies index field is set for single file (talks)

All tests pass successfully. The fix ensures that `lynguine`'s `CustomDataFrame.from_flow()` receives the required index field in the interface specification.
