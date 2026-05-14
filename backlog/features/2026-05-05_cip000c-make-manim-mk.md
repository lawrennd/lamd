---
id: "2026-05-05_cip000c-make-manim-mk"
title: "Create make-manim.mk build targets (preprocess → render → html/pptx)"
status: "Completed"
priority: "High"
created: "2026-05-05"
last_updated: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: "Neil Lawrence"
dependencies: ["2026-05-05_cip000c-mdpp-manim-format"]
tags:
- backlog
- manim
- makefile
- cip-000c
---

# Task: Create make-manim.mk

## Description

Create `lamd/makefiles/make-manim.mk` with build targets for the `manim-slides` output pipeline (interactive HTML and PPTX). This is Phase 2 of CIP-000C.

## Acceptance Criteria

- [ ] `%.slides.manim.py` target: runs `mdpp --to manim` to preprocess the source `.md` into a Python script
- [ ] `${BASE}.slides.manim.rendered` target: runs `manim-slides render` to produce animation clips; uses a `.rendered` sentinel file to avoid re-rendering when clips are current
- [ ] `${BASE}.slides.html` target: runs `manim-slides convert` (default HTML) from the `.rendered` sentinel
- [ ] `${BASE}.slides.pptx` target: runs `manim-slides convert --to=pptx` from the `.rendered` sentinel
- [ ] `MANIMFLAGS` and `MANIMCONVERTFLAGS` variables are used (defaulting to empty) so frontmatter options can be passed in
- [ ] File follows the conventions of `make-slides.mk` (variable naming, help comments, phony targets)

## Implementation Notes

The render step is separated from convert so that multiple output formats (html, pptx) share one render pass. The `.rendered` sentinel file approach is already used elsewhere in the LaMD makefiles.

```makefile
MANIMFLAGS ?=
MANIMCONVERTFLAGS ?=

%.slides.manim.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim --format slides --code none \
	    ${PPFLAGS} --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR)

${BASE}.slides.manim.rendered: ${BASE}.slides.manim.py
	manim-slides render ${MANIMFLAGS} $< Talk
	touch $@

${BASE}.slides.html: ${BASE}.slides.manim.rendered
	manim-slides convert ${MANIMCONVERTFLAGS} Talk ${BASE}.slides.html

${BASE}.slides.pptx: ${BASE}.slides.manim.rendered
	manim-slides convert --to=pptx ${MANIMCONVERTFLAGS} Talk ${BASE}.slides.pptx
```

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-mdpp-manim-format`

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 2.
