---
id: "2026-05-05_cip000c-slidesincremental-manim"
title: "Implement \\slidesincremental{} in manim macro files"
status: "Completed"
priority: "Medium"
created: "2026-05-05"
last_updated: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: "Neil Lawrence"
dependencies: ["2026-05-05_cip000c-manim-gpp-skeleton"]
tags:
- backlog
- manim
- macros
- cip-000c
---

# Task: Implement \slidesincremental in Manim macro files

## Description

Add the `\slidesincremental{items}` macro to both `talk-macros-slides-manim.gpp` and `talk-macros-video-manim.gpp`. This is Phase 2 of CIP-000C.

## Acceptance Criteria

**For `talk-macros-slides-manim.gpp` (manim-slides, interactive):**
- [ ] Each bullet item is revealed with a `FadeIn` animation
- [ ] `self.next_slide()` is called between each bullet so the presentation pauses for the presenter to advance
- [ ] Previously revealed bullets remain on screen (cumulative reveal)
- [ ] Each bullet is positioned below the previous one using `next_to(..., DOWN)`

**For `talk-macros-video-manim.gpp` (raw Manim, video):**
- [ ] Each bullet item fades in sequentially without `self.next_slide()` calls
- [ ] A short `self.wait(1)` pause is inserted between bullets for pacing
- [ ] Previously revealed bullets remain on screen

**Both formats:**
- [ ] Bullet items are parsed from a markdown list (lines starting with `* ` or `- `)
- [ ] Each item text is processed through `lamd_text(...)` for Markdown/math support
- [ ] An integration test with a fixture containing `\slidesincremental` generates valid Python for both formats

## Implementation Notes

The most robust approach is to implement `\slidesincremental` as a gpp macro that receives the whole block and generates the Python loop. Since gpp is not well-suited to iterating over a list of items, a helper in `_lamd_manim.py` can handle iteration:

```python
def lamd_incremental(items, scene, with_slides=True):
    """Render a list of strings as incrementally revealed bullets."""
    group = VGroup()
    for item in items:
        mob = lamd_text(item)
        if group:
            mob.next_to(group, DOWN, aligned_edge=LEFT)
        group.add(mob)
        scene.play(FadeIn(mob))
        if with_slides:
            scene.next_slide()
        else:
            scene.wait(1)
```

The macro then emits:
```python
lamd_incremental([r"item1", r"item2", r"item3"], self, with_slides=True)
```

The gpp macro parses out list items (one per line) and builds the Python list literal.

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-manim-gpp-skeleton`, `2026-05-05_cip000c-lamd-manim-helper`

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 2.
