---
id: "2025-08-30_remove-notedown-dependency"
title: "Remove notedown Dependency from LaMD Pipeline"
status: "Proposed"
priority: "Medium"
created: "2025-08-30"
last_updated: "2025-08-30"
owner: "Neil Lawrence"
github_issue: ""
dependencies: ["2025-08-30_pandoc-cell-boundary-issue"]
tags:
- backlog
- optimization
- dependency-reduction
- build-system
---

# Task: Remove notedown Dependency from LaMD Pipeline

## Description

With the successful fix of the pandoc cell boundary issue (2025-08-30_pandoc-cell-boundary-issue), we can now remove the notedown dependency from the LaMD pipeline. The original issue was that pandoc wasn't creating proper cell boundaries, requiring notedown as a fallback. Now that pandoc works correctly with the fixed template, notedown is no longer necessary.

This task involves:
1. **Updating makefiles** to use pandoc directly instead of notedown
2. **Testing the pandoc-only pipeline** thoroughly across different content types
3. **Removing notedown** from dependencies and installation requirements
4. **Updating documentation** to reflect the simplified pipeline
5. **Ensuring backward compatibility** during the transition

## Current State

The LaMD pipeline currently uses this flow:
1. **mdpp preprocessing** → converts `\code{}` macros to `::: {.cell .*}` syntax
2. **pandoc template processing** → applies Jekyll template
3. **notedown conversion** → converts markdown to Jupyter notebook (fallback)

## Target State

The simplified pipeline should be:
1. **mdpp preprocessing** → converts `\code{}` macros to `::: {.cell .*}` syntax  
2. **pandoc direct conversion** → converts markdown to Jupyter notebook using fixed template

## Benefits

- **Reduced dependencies**: One less Python package to install and maintain
- **Simpler pipeline**: Fewer conversion steps and potential failure points
- **Better performance**: Direct pandoc conversion is likely faster than pandoc→notedown
- **Cleaner builds**: Fewer intermediate files and processing steps
- **Maintenance**: Less code to maintain and debug

## Acceptance Criteria

- [ ] Makefile updated to use pandoc directly for notebook generation
- [ ] All existing notebooks generate correctly with pandoc-only pipeline
- [ ] Test suite passes with pandoc-only conversion
- [ ] notedown dependency removed from requirements/setup files
- [ ] Documentation updated to reflect new pipeline
- [ ] Validation scripts updated to work with pandoc output
- [ ] Performance benchmarking shows no regression (or improvement)
- [ ] Backward compatibility maintained for existing content

## Implementation Notes

### Phase 1: Makefile Updates
- Modify `make-ipynb.mk` to use pandoc directly instead of notedown
- Update pandoc flags and template usage for direct notebook generation
- Test with existing content to ensure compatibility

### Phase 2: Dependency Cleanup  
- Remove notedown from `requirements.txt`, `setup.py`, or `pyproject.toml`
- Update installation documentation
- Check for any remaining notedown references in code/docs

### Phase 3: Testing & Validation
- Run comprehensive tests across different content types
- Verify cell boundaries, metadata, and output formatting
- Performance testing to ensure no regression
- Update validation scripts if needed

### Technical Considerations
- **Pandoc flags**: May need to adjust pandoc command-line options for direct notebook output
- **Template compatibility**: Ensure the fixed template works for all content types
- **Cell metadata**: Verify that pandoc preserves necessary notebook metadata
- **Error handling**: Update error messages and validation for pandoc-only pipeline

## Related

- **Resolved Issue**: 2025-08-30_pandoc-cell-boundary-issue (pandoc template fix)
- **Test**: `tests/unit/test_cell_boundaries.py` (validates pandoc cell creation)
- **Makefile**: `lamd/makefiles/make-ipynb.mk` (current notedown usage)
- **Template**: `lamd/templates/pandoc/pandoc-jekyll-ipynb-template.markdown` (fixed template)

## Progress Updates

### 2025-08-30

Task created following successful resolution of pandoc cell boundary issue. With pandoc now working correctly, notedown is no longer needed as a fallback and can be removed to simplify the pipeline.
