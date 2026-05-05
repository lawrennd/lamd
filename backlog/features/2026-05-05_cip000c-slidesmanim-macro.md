---
id: "2026-05-05_cip000c-slidesmanim-macro"
title: "Add \\slidesmanim{} macro (passthrough in manim, no-op elsewhere)"
status: "Completed"
priority: "High"
created: "2026-05-05"
last_updated: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: ""
dependencies: ["2026-05-05_cip000c-manim-gpp-skeleton"]
tags:
- backlog
- manim
- macros
- cip-000c
---

# Task: Add \slidesmanim{} macro

## Description

Implement the `\slidesmanim{code}` macro across all LaMD macro files. In the manim and manim-video formats it emits `code` verbatim into `construct()`; in all other formats (html, pptx, tex, notes) it is a no-op. This is Phase 2 of CIP-000C.

## Acceptance Criteria

- [ ] `\slidesmanim{code}` defined in `talk-macros-slides-manim.gpp` as a verbatim passthrough
- [ ] `\slidesmanim{code}` defined in `talk-macros-video-manim.gpp` as a verbatim passthrough
- [ ] `\slidesmanim{code}` defined as an empty no-op in all existing macro files: `talk-macros-notes.gpp`, `talk-macros-slides-html.gpp`, `talk-macros-slides.gpp`, and any other format-specific files
- [ ] No-op test: assert `\slidesmanim{circle = Circle()}` expands to empty string in `html`, `tex`, and `notes` formats
- [ ] Passthrough test: assert `\slidesmanim{circle = Circle()}` expands to `circle = Circle()` in `manim` and `manim-video` formats

## Implementation Notes

In gpp, a no-op macro is defined as:
```
#define \slidesmanim(code)
```

The passthrough in manim formats is:
```
#define \slidesmanim(code) code
```

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-manim-gpp-skeleton`

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 2.
