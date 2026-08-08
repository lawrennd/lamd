---
id: "2026-08-08_mdpeople-missing-image-field"
title: "mdpeople crashes on people.yml entries missing image field"
status: "Proposed"
priority: "High"
created: "2026-08-08"
last_updated: "2026-08-08"
category: "bugs"
related_cips: ["000E"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- bug
- mdpeople
- robustness
---

# Task: Fix mdpeople crash on missing image field

## Description

`mdpeople.py` line 146 uses a hard key lookup `person_info["image"]`, which raises
`KeyError: 'image'` when a person entry in `_people/people.yml` has no `image` field.
The error is caught by the bare `except Exception as e` handler and printed as:

```
Error: 'image'
make: *** [talk-people.gpp] Error 1
```

This is the only error message the user sees, making it very hard to diagnose.

The bug is triggered by any module that has a placeholder or incomplete `people.yml` entry —
including freshly installed modules where the `_people/people.yml` template ships without
an `image` key.

## Acceptance Criteria

- [ ] `mdpeople` does not crash when a `people.yml` entry lacks an `image` field
- [ ] Either skip the person (with a warning) or use an empty/placeholder image path
- [ ] The error message when `image` is absent is actionable (names the person and field)

## Implementation Notes

In `generate_macros_file()` (and the call at line 146), change:

```python
person_info["image"],
```

to something like:

```python
person_info.get("image", ""),  # graceful fallback
```

Or add explicit validation before the loop that names the offending person:

```python
for person_info in people:
    if "image" not in person_info:
        name = f"{person_info.get('given','')} {person_info.get('family','')}".strip()
        print(f"Warning: person '{name}' has no 'image' field — skipping", file=sys.stderr)
        continue
```

## Related

- PRs: 
- Discovered via: vibecourse fresh-install testing (2026-08-08)
