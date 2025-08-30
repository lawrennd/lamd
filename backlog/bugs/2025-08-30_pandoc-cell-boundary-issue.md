---
id: "2025-08-30_pandoc-cell-boundary-issue"
title: "Pandoc Cell Boundary Issue in LaMD Pipeline"
status: "Proposed"
priority: "High"
created: "2025-08-30"
last_updated: "2025-08-30"
owner: "Neil Lawrence"
dependencies: []
---

# Task: Fix Pandoc Cell Boundary Issue in LaMD Pipeline

## Description

The LaMD pipeline has an issue where pandoc is not properly creating cell boundaries when converting markdown to Jupyter notebooks. While notedown is used as a fallback, this is a workaround that masks the underlying problem rather than solving it. The issue is why isn't pandoc handling the cell boundary syntax correctly?

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

1. **Pandoc configuration**: Check if pandoc template or flags need adjustment
2. **Markdown structure**: Verify the intermediate markdown structure is correct
3. **Pandoc version**: Test with different pandoc versions
4. **Template issues**: Investigate if the pandoc-jekyll-ipynb-template has issues
5. **Cell boundary syntax**: Verify that pandoc supports the `::: {.cell .*}` syntax
6. **Alternative approaches**: Consider if different pandoc flags or templates would work better

## Acceptance Criteria

- [ ] Pandoc generates at least 9 cells from the test file
- [ ] `test_cell_boundary_pipeline()` test passes without notedown fallback
- [ ] Full LaMD pipeline works with pandoc only
- [ ] Notedown can be removed as a dependency (optional)

## Implementation Notes

- The test is currently failing as expected, confirming the issue
- Focus on pandoc template and configuration first
- May need to modify the pandoc-jekyll-ipynb-template
- Consider if this is a pandoc limitation or configuration issue
- The notedown fallback is a workaround, not a solution - it masks the underlying problem
- Goal is to eliminate the need for notedown entirely by fixing pandoc's cell boundary handling

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
