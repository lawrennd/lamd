---
id: "2025-08-27_practical-directory-mdfield-priority"
title: "Fix mdfield Priority: Practical Files Not Going to Correct Directory"
status: "Completed"
priority: "High"
created: "2025-08-27"
last_updated: "2025-08-27"
owner: "@lawrennd"
github_issue: ""
dependencies: ""
tags:
- backlog
- bug
- mdfield
- practical-directory
---

# Task: Fix mdfield Priority: Practical Files Not Going to Correct Directory

## Description

The `maketalk` command was not correctly moving practical files to the `practicalsdir` when the layout was set to "practical" in the markdown file. This was due to a bug in the `mdfield` command where it was prioritizing configuration files over markdown files when extracting metadata fields.

### Root Cause

The `mdfield` command was checking `_lamd.yml` first, then falling back to the markdown file. This meant that when `_lamd.yml` had `layout: lecture`, it would return `lecture` even if the markdown file had `layout: practical`. The makefiles then used this incorrect `layout` value, so the conditional copying to `practicalsdir` never triggered.

### Impact

- Practical files with `layout: practical` were being copied to default directories instead of `practicalsdir`
- Files were getting incorrect prefixes (e.g., `01-02-` instead of `01-02-01-`)
- The practical directory system was not working as intended

## Solution

### Fixed mdfield.py Priority Logic

Changed the priority in `mdfield.py` from config-first to markdown-first:

```python
# OLD (incorrect): Config first, markdown fallback
if args.field in iface:
    answer = iface[args.field]  # Returns config value
else:
    answer = nt.talk_field(...)  # Falls back to markdown

# NEW (correct): Markdown first, config fallback  
try:
    answer = nt.talk_field(...)  # Try markdown first
except FileFormatError:
    if args.field in iface:
        answer = iface[args.field]  # Falls back to config
```

### Enhanced Makefiles

Added conditional copying logic to relevant makefiles:

- `make-post.mk`: Added conditional copying for `posts.html` files
- `make-notes.mk`: Added conditional copying for `notes.html` files
- `make-talk-flags.mk`: Added layout and practicalsdir extraction

### Comprehensive Testing

Created a comprehensive test suite (`test_directory_system.py`) covering:
- All layout types: practical, lecture, talk, topic, background, notebook, casestudy
- All directory extractions: snippetsdir, bibdir, slidesdir, postsdir, notesdir, notebooksdir, texdir, practicalsdir
- Prefix generation for each layout type
- Error handling for missing fields
- Complete workflows for practical, lecture, and talk layouts

## Acceptance Criteria

- [x] `mdfield layout probability-practical.md` returns `practical` instead of `lecture`
- [x] Practical files are copied to `practicalsdir` when layout is "practical"
- [x] Correct prefix generation for practical files (e.g., `01-02-01-`)
- [x] All existing functionality continues to work
- [x] Comprehensive test coverage for directory system
- [x] All tests pass (95/95)

## Implementation Notes

### Files Modified

1. **`lamd/mdfield.py`**
   - Fixed field extraction priority to prioritize markdown over config
   - Updated error handling for the new priority order

2. **`lamd/lamd/makefiles/make-post.mk`**
   - Added conditional copying for practical files
   - Ensures `posts.html` files go to `practicalsdir` when layout is "practical"

3. **`lamd/lamd/makefiles/make-notes.mk`**
   - Added conditional copying for practical files
   - Ensures `notes.html` files go to `practicalsdir` when layout is "practical"

4. **`lamd/lamd/makefiles/make-talk-flags.mk`**
   - Added `LAYOUT` and `PRACTICALSDIR` variable extraction
   - Added validation for practicalsdir when layout is "practical"

5. **`tests/unit/test_directory_system.py`**
   - Comprehensive test suite for entire directory system
   - Tests all layout types and directory extractions
   - Tests error handling and complete workflows

6. **`tests/unit/test_mdfield.py`**
   - Updated tests to reflect new priority order
   - Tests markdown-first, config-fallback behavior

### Verification

**Before the fix:**
```bash
mdfield layout probability-practical.md
# Output: lecture (from _lamd.yml)
```

**After the fix:**
```bash
mdfield layout probability-practical.md  
# Output: practical (from markdown file)
```

**Result:**
- Practical files now correctly get copied to `../_practicals/01-probability-practical.html`
- Prefix generation works correctly: `01-` (from practical: 1)
- All tests pass (95/95)

## Related

- Related to CIP-0005 (Improve mdpp Error Handling and Validation)
- Affects practical directory system functionality
- Related to mdfield command-line tool
- Related to makefile directory handling

## Progress Updates

### 2025-08-27
- Identified root cause: mdfield priority bug
- Fixed mdfield.py to prioritize markdown over config files
- Enhanced makefiles with conditional copying for practicals
- Created comprehensive test suite for directory system
- All tests passing (95/95)
- Task completed successfully
