---
status: proposed
priority: medium
path: backlog/features/2025-05-16_implement-extract-snippets.md
type: feature
title: Implement extract_snippets Function in lynguine.util.talk
---

# Task: Implement extract_snippets Function in lynguine.util.talk

## Metadata
- **ID**: 2025-05-16_implement-extract-snippets
- **Status**: Proposed
- **Priority**: Medium
- **Created**: 2025-05-16
- **Owner**: Unassigned
- **Dependencies**: None

## Description

The `dependencies.py` module offers a `snippets` dependency type to extract code snippets from markdown files, but the required `extract_snippets` function is not currently implemented in the `lynguine.util.talk` module. This function should be implemented to properly extract code snippets referenced in markdown files.

Currently, the `snippets` option in the `dependencies.py` module is commented out to prevent errors when users try to use this functionality.

## Acceptance Criteria

- [ ] Implement the `extract_snippets` function in the `lynguine.util.talk` module with parameters:
  - `filename` - The markdown file to analyze
  - `absolute_path` - Whether to return absolute or relative paths
  - `snippets_path` - Base directory for snippet files
- [ ] The function should identify and extract paths to code snippet files referenced in the markdown
- [ ] The function should return a list of snippets filenames
- [ ] Update the `dependencies.py` module to uncomment the `snippets` option
- [ ] Add tests for the new function
- [ ] Update documentation to describe how the snippets extraction works

## Implementation Notes

The implementation should follow the pattern of similar extraction functions in the `lynguine.util.talk` module, such as `extract_inputs` and `extract_diagrams`. It should handle various forms of snippet inclusion such as code blocks that reference external files.

The regular expression pattern should identify common code inclusion patterns in markdown, such as:
```
\includeCode{filename}
```

## Related

- **GitHub Issue**: None yet
- **CIP**: None

## Progress Updates

### 2025-05-16
Task created with Proposed status. 