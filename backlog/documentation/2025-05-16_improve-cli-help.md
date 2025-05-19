---
id: "2025-05-16_improve-cli-help"
title: "Improve Command Line Help Text for All lamd Utilities"
status: "In Progress"
priority: "High"
effort: "Medium"
type: "documentation"
created: "2025-05-16"
last_updated: "2025-05-16"
owner: lawrennd
github_issue: null
dependencies: []
---

## Description

The lamd project provides several command line utilities for academic content generation and management, but the help text displayed when using these utilities with the `-h` or `--help` flag is minimal and lacks detailed explanations and examples. This task involves improving the command line help text for all lamd utilities to make them more user-friendly and informative.

The utilities to improve include:
1. `mdpp` - Markdown preprocessor ✅
2. `flags` - Extracts pandoc flags
3. `dependencies` - Lists dependencies in markdown files
4. `mdfield` - Extracts fields from markdown headers
5. `maketalk` - Converts talk files to different formats
6. `makecv` - Converts CVs to different formats 
7. `mdlist` - Generates lists from YAML definitions
8. `mdpeople` - Generates people macros from YAML definitions

## Acceptance Criteria

- [ ] Updated help text for all command line utilities that includes:
  - Clear description of the utility's purpose
  - Detailed explanation of each command line option
  - Information about default values
  - Examples of common usage patterns
- [ ] Help text is properly formatted for console display
- [ ] Help text is consistent across all utilities
- [ ] Help text includes references to related utilities where appropriate
- [ ] All updates are tested to ensure they display correctly

## Implementation Notes

The improvement will focus on enhancing the `argparse` configurations in each utility's main function. For each utility:

1. Add a more detailed description to the `ArgumentParser` initialization
2. Enhance the help text for each argument
3. Add examples in the epilog section
4. Ensure consistent terminology and formatting across all utilities

Example of improved argument help text:
```python
parser.add_argument("--format", type=str, 
                    choices=['notes', 'slides', 'code'],
                    help="Specify the output format. 'notes' generates full notes with explanations, \
                         'slides' generates presentation slides with bullet points, \
                         'code' extracts only code sections.")
```

## Related

- CIP: 0001
- Documentation: README.md

## Progress Updates

### 2025-05-16

Task created with Proposed status. Initial analysis of current help text shows significant room for improvement in clarity and thoroughness.

### 2025-05-16

Improved the help text for the `mdpp` utility:
- Added comprehensive docstring to the main function with examples
- Enhanced argument descriptions for all options
- Added proper ArgumentParser description and epilog
- Made help text work without requiring configuration files
- Added error handling for missing configuration files
- Committed changes to the cip0001-cli-documentation branch

Next steps:
- Improve help text for other utilities following the same pattern
- Ensure consistent style and terminology across all utilities 