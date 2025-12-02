---
id: "2025-12-02_mdlist-yaml-dataframe-error"
title: "mdlist fails with 'Mixing dicts with non-Series' error when loading publications"
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

# Task: mdlist YAML DataFrame conversion error

## Description

When running `mdlist publications` with multiple YAML files from the publications directory, it fails with:

```
ValueError: Mixing dicts with non-Series may lead to ambiguous ordering.
```

The error occurs in `lynguine/access/io.py` when trying to convert YAML data to a pandas DataFrame. The publication YAML files may have inconsistent structures that cause pandas to fail.

## Error Traceback

```
File "/Users/neil/lawrennd/lynguine/lynguine/access/io.py", line 204, in read_yaml
    return pd.DataFrame(data)
ValueError: Mixing dicts with non-Series may lead to ambiguous ordering.
```

## Steps to Reproduce

```bash
cd /Users/neil/lawrennd/cv/sheffield
conda activate py311
mdlist publications /Users/neil/lawrennd/publications/*.yml -o publication-list.markdown -s 2020
```

## Acceptance Criteria

- [ ] `mdlist publications` successfully generates publication-list.markdown
- [ ] Handle inconsistent YAML structures gracefully
- [ ] Provide clear error messages when data format issues occur

## Implementation Notes

The issue is likely in how `lynguine/access/io.py` handles YAML files with varying structures. Options:
1. Pre-process YAML files to normalize structure
2. Handle dict/list mixtures in the DataFrame conversion
3. Use a more flexible data loading approach

This may be a lynguine issue rather than lamd.

## Related

- File: `lynguine/access/io.py` line 204
- File: `lamd/mdlist.py`
- Depends on: lynguine data loading

## Progress Updates

### 2025-12-02

Task created. Issue discovered while attempting to generate publication list for Sheffield CV.

