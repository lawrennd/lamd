---
id: "2026-05-05_cip000c-make-video-manim-mk"
title: "Create make-video-manim.mk build targets (preprocess → raw manim → mp4)"
status: "Completed"
priority: "High"
created: "2026-05-05"
last_updated: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: ""
dependencies: ["2026-05-05_cip000c-video-manim-gpp", "2026-05-05_cip000c-mdpp-manim-format"]
tags:
- backlog
- manim
- makefile
- cip-000c
---

# Task: Create make-video-manim.mk

## Description

Create `lamd/makefiles/make-video-manim.mk` with build targets for the raw Manim MP4 pipeline. This produces a single continuous video file from the talk source. This is Phase 2 of CIP-000C.

## Acceptance Criteria

- [ ] `%.video.manim.py` target: runs `mdpp --to manim-video` to preprocess `.md` → Python script
- [ ] `${BASE}.video.mp4` target: runs `manim ${MANIMFLAGS} $< Talk -o ${BASE}.video.mp4`
- [ ] `MANIMFLAGS` variable used (defaulting to empty) to allow quality/resolution flags
- [ ] File follows conventions of other `make-*.mk` files in the `makefiles/` directory
- [ ] `manim-video` target (phony) builds `${BASE}.video.mp4` when invoked

## Implementation Notes

```makefile
MANIMFLAGS ?=

%.video.manim.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim-video --format slides --code none \
	    ${PPFLAGS} --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR)

${BASE}.video.mp4: ${BASE}.video.manim.py
	manim ${MANIMFLAGS} $< Talk -o ${BASE}.video.mp4

.PHONY: manim-video
manim-video: ${BASE}.video.mp4
```

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-video-manim-gpp`, `2026-05-05_cip000c-mdpp-manim-format`

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 2.
