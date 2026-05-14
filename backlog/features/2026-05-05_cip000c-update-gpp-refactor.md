---
category: features
created: '2026-05-05'
id: 2026-05-05_cip000c-update-gpp-refactor
last_updated: '2026-05-05'
priority: Medium
related_cips:
- 000C
status: Completed
owner: "Neil Lawrence"
title: 'Update CIP-000C: fix mdpp description, add GPP refactor items'
---

# Task: Update CIP-000C to reflect Phase 1 reality and GPP refactor plan

## Description

CIP-000C (`cip/cip000C.md`) was written before the actual implementation of Phase 1
and before the GPP macro refactor design was finalised. Three targeted corrections are
needed:

1. **Fix "Relationship to `mdpp.py`" paragraph** — the original text claimed "No
   changes to `mdpp.py` logic are needed". This is wrong. `mdpp.py` was substantively
   changed: Python class header injection (`_MANIM_SLIDES_HEADER` /
   `_MANIM_VIDEO_HEADER`), post-processing to strip non-Python prefix content (HTML/TeX
   comments emitted by included `.gpp` files), and `--to manim-video` support. The
   paragraph is updated to reflect the actual implementation.

2. **Check off `talk-macros-video-manim.gpp`** — Phase 2 listed creating this file, but
   it was completed during Phase 1. The implementation status checkbox is corrected.

3. **Add GPP refactor implementation status items** — the refactor (new
   `talk-macros-manim.gpp` shared file, trimmed format-specific files, two-level include
   structure in `talk-macros.gpp`, `-DSLIDES=1`/`-DVIDEO=1` flags in `mdpp.py`) was
   designed after the CIP was committed. New checklist items are added so progress can
   be tracked.

## Acceptance Criteria

- [ ] `cip/cip000C.md` "Relationship to `mdpp.py`" paragraph accurately describes the
  implemented behaviour
- [ ] Phase 2 `talk-macros-video-manim.gpp` item is marked `[x]`
- [ ] Five new GPP refactor items are present in the Implementation Status section

## Related

- CIP: 000C
- Backlog: 2026-05-05_cip000c-manim-gpp-skeleton.md (Phase 1 work)

## Progress Updates

### 2026-05-05
Task created. CIP updated and committed as part of the GPP macro refactor work.