---
id: "2026-05-05_cip000c-mdpp-manim-format"
title: "Add --to manim support in mdpp.py"
status: "Completed"
priority: "High"
created: "2026-05-05"
last_updated: "2026-05-05"
completed: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: "Neil Lawrence"
dependencies: ["2026-05-05_cip000c-manim-gpp-skeleton", "2026-05-05_cip000c-lamd-manim-helper"]
tags:
- backlog
- manim
- mdpp
- cip-000c
---

# Task: Add --to manim support in mdpp.py

## Description

Extend `mdpp.py` to handle `--to manim` and `--to manim-video` format flags. This is Phase 1 of CIP-000C (the `--to manim-video` wiring is also done here for completeness, though the video macro file is a Phase 2 deliverable).

## Acceptance Criteria

- [ ] `--to manim` loads `talk-macros-slides-manim.gpp` as the format-specific macro file
- [ ] `--to manim-video` loads `talk-macros-video-manim.gpp` as the format-specific macro file
- [ ] After preprocessing with `--to manim`, `mdpp.py` writes `_lamd_manim.py` (copied from `lamd/util/lamd_manim_helper.py`) into the same output directory as the generated `.slides.manim.py` file
- [ ] The generated `.slides.manim.py` file is valid Python (passes `python -m py_compile`)
- [ ] `--to manim` and `--to manim-video` are listed in `mdpp.py` help/choices alongside existing formats
- [ ] Existing `--to html`, `--to pptx`, `--to tex`, `--to notes` behaviour is unchanged

## Implementation Notes

The `--to` flag in `mdpp.py` already selects a format-specific gpp macro file. The change is:
1. Add `"manim"` and `"manim-video"` to the accepted choices
2. Map them to the new `.gpp` files
3. Add a post-processing step: when `--to manim` or `--to manim-video` is used, copy `lamd_manim_helper.py` to the output directory as `_lamd_manim.py`

The copy step ensures the helper is always co-located with the generated script and can be imported with `from _lamd_manim import lamd_text`.

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-manim-gpp-skeleton`, `2026-05-05_cip000c-lamd-manim-helper`

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 1.
