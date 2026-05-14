---
id: "2026-05-05_cip000c-maketalk-to-choices"
title: "Add manim and manim-video to maketalk.py --to choices"
status: "Completed"
priority: "Medium"
created: "2026-05-05"
last_updated: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: "Neil Lawrence"
dependencies: ["2026-05-05_cip000c-wire-into-make-talk"]
tags:
- backlog
- manim
- maketalk
- cip-000c
---

# Task: Add manim/manim-video to maketalk.py

## Description

Extend `lamd/maketalk.py` to accept `manim` and `manim-video` as `--to` argument choices. Also extract any `manim:` block from the talk YAML frontmatter and pass the options as `MANIMFLAGS` / `MANIMCONVERTFLAGS` to the generated makefile. This is Phase 2 of CIP-000C.

## Acceptance Criteria

- [ ] `maketalk --to manim talk.md` invokes the `manim` make target (builds `talk.slides.html` via manim-slides)
- [ ] `maketalk --to manim-video talk.md` invokes the `manim-video` make target (builds `talk.video.mp4`)
- [ ] A `manim:` key in the talk YAML frontmatter is extracted and its sub-keys mapped to `MANIMFLAGS` (e.g. `quality: high` → `-ql` or `--quality=high`)
- [ ] `maketalk --help` lists `manim` and `manim-video` in the `--to` choices
- [ ] No regression in behaviour of existing `--to` choices

## Implementation Notes

The frontmatter extraction can follow the same pattern as how `geometry:` or `transition:` are currently handled. The mapping from frontmatter keys to manim CLI flags:

| frontmatter key | manim flag |
|---|---|
| `quality: low` | `-ql` |
| `quality: medium` | `-qm` |
| `quality: high` | `-qh` |
| `quality: production` | `-qp` |
| `fps: 30` | `--fps 30` |
| `background_color: WHITE` | `--background_color WHITE` |

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-wire-into-make-talk`

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 2.
