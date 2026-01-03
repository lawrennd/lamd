---
category: bugs
created: '2025-08-30'
dependencies: []
id: 2025-08-30_pandoc-cell-boundary-issue
last_updated: '2025-08-30'
owner: Neil Lawrence
priority: High
related_cips: []
status: Completed
title: Pandoc Cell Boundary Issue in LaMD Pipeline
---

# Task: Fix Pandoc Cell Boundary Issue in LaMD Pipeline

## Description

The LaMD pipeline has an issue where pandoc is not properly creating cell boundaries when converting markdown to Jupyter notebooks. The root cause is that the custom pandoc template (`pandoc-jekyll-ipynb-template`) is designed for Jekyll blog posts and doesn't handle the `::: {.cell .*}` syntax correctly for notebook generation. While notedown is used as a fallback, this is a workaround that masks the underlying template issue rather than solving it.

## Current Behavior

When running the full LaMD pipeline:
1. **mdpp preprocessing** works correctly (converts `\code{}` to proper markdown)
2. **pandoc template processing** works correctly
3. **pandoc final conversion** fails to create proper cell boundaries (only 4 cells vs expected 9+)
4. **notedown fallback** works correctly (17 cells) but shouldn't be necessary

## Expected Behavior

Pandoc should be able to create proper cell boundaries without requiring notedown as a fallback. The pipeline should work end-to-end with just pandoc. The intermediate markdown contains proper cell boundary syntax (`::: {.cell .*}`) that pandoc should recognize and convert correctly.

## Impact

- **Build complexity**: Requires notedown as additional dependency
- **Maintenance burden**: Two different conversion paths to maintain
- **Potential failures**: If notedown breaks, the entire pipeline fails
- **Performance**: Additional processing step adds time to builds

## Technical Details

The issue is confirmed by the test `test_cell_boundary_pipeline()` in `tests/unit/test_cell_boundaries.py`:

- Pandoc generates only 4 cells from test file with 3 headers + 3 code blocks
- Expected minimum: 9 cells (headers, code blocks, metadata)
- Notedown generates 17 cells from the same input (overly aggressive cell separation)

The intermediate markdown contains proper cell boundary syntax:
```markdown
::: {.cell .markdown}
# Header 1
:::

::: {.cell .code}
```python
print("Code block 1")
```
:::
```

Pandoc should recognize these `::: {.cell .*}` markers and create proper cells, but it's not doing so.

## Investigation Needed

1. **Template analysis**: Investigate the pandoc-jekyll-ipynb-template to understand why it doesn't handle cell boundaries
2. **Template modification**: Modify the template to properly handle `::: {.cell .*}` syntax
3. **Alternative templates**: Consider using a notebook-specific pandoc template instead
4. **Pandoc configuration**: Test different pandoc flags and configurations for notebook generation
5. **Template testing**: Verify that pandoc works correctly with cell boundaries when using the right template

## Acceptance Criteria

- [x] Pandoc generates at least 9 cells from the test file (✅ Now generates 10 cells)
- [x] `test_cell_boundary_pipeline()` test passes without notedown fallback (✅ Test now passes)
- [x] Full LaMD pipeline works with pandoc only (✅ Template fixed)
- [ ] Notedown can be removed as a dependency (optional - not implemented yet)

## Implementation Notes

- The test is currently failing as expected, confirming the issue
- **Root cause identified**: The pandoc-jekyll-ipynb-template doesn't handle cell boundaries correctly
- **Solution**: Fix the template or use a notebook-specific template
- **Notedown is unnecessary**: Pandoc can handle cell boundaries correctly with the right template
- **Goal**: Eliminate notedown dependency entirely by fixing the pandoc template
- **Validation**: The validation script should check pandoc output, not notedown fallback

## Related

- Test: `tests/unit/test_cell_boundaries.py::TestCellBoundaries::test_cell_boundary_pipeline`
- Makefile: `lamd/lamd/makefiles/make-ipynb.mk`
- Template: `lamd/lamd/templates/pandoc/pandoc-jekyll-ipynb-template`

## Progress Updates

### 2025-08-30
Task created. Issue confirmed by failing test. Pandoc generates only 4 cells vs expected 9+, while notedown correctly generates 17 cells.

### 2025-08-30 (Update)
Added improved error detection and validation utilities to `tests/unit/test_cell_boundaries.py`:
- Enhanced test to detect when both pandoc AND notedown fail (critical failure)
- Added `validate_notebook_cells()` utility function for build process integration
- Added `test_notedown_failure_detection()` to warn about notedown issues
- Added `test_validation_utility()` to test the validation function
- These utilities can be integrated into the build process to detect and warn about conversion failures

### 2025-08-30 (Root Cause Identified)
**BREAKTHROUGH**: Identified the real root cause of the issue:
- Pandoc **can** handle `::: {.cell .*}` syntax correctly (tested directly)
- The problem is the **pandoc-jekyll-ipynb-template** which is designed for Jekyll blog posts
- This template doesn't handle cell boundaries correctly for notebook generation
- **Solution**: Fix the template or use a notebook-specific template
- **Notedown is unnecessary** - pandoc can work correctly with the right template

### 2025-08-30 (ISSUE RESOLVED)
**🎉 FIXED**: Successfully resolved the pandoc cell boundary issue!

**Root Cause**: The template was creating **nested cell boundaries** by wrapping `$body$` content in `::: {.cell .markdown}`, but the body already contained individual `::: {.cell .code}` blocks. Pandoc cannot handle nested cell boundaries properly.

**Solution Applied**: Modified `pandoc-jekyll-ipynb-template.markdown` to remove the wrapping cell boundary around `$body$`, allowing individual cell boundaries to be processed correctly.

**Results**:
- ✅ **Pandoc now generates 10 cells** (vs previous 4 cells)
- ✅ **Test passes**: `test_cell_boundary_pipeline()` now passes
- ✅ **No notedown fallback needed**: Pandoc works correctly with fixed template
- ✅ **Proper cell structure**: Alternating markdown/code cells as expected

**Technical Details**:
- **Before**: Nested structure caused pandoc to create only 4 template cells
- **After**: Flat structure allows pandoc to create 10 cells (4 template + 6 content cells)
- **Template change**: Removed `::: {.cell .markdown}` wrapper around `$body$` content
- **Validation**: Confirmed with minimal examples and full pipeline test