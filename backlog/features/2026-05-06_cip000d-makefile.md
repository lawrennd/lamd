---
id: "2026-05-06_cip000d-makefile"
title: "Write make-svg-manim.mk and wire into make-talk.mk and maketalk.py"
status: "Proposed"
priority: "High"
created: "2026-05-06"
last_updated: "2026-05-06"
category: "features"
related_cips: ["000D"]
owner: "Neil Lawrence"
dependencies: ["2026-05-06_cip000d-mdpp-to-manim-svg", "2026-05-06_cip000d-svg-to-html"]
tags:
- backlog
- manim
- svg
- makefile
- cip-000d
---

# Task: Write make-svg-manim.mk and wire into make-talk.mk and maketalk.py

## Description

Write `lamd/makefiles/make-svg-manim.mk` and wire the new `manim-svg` target into `make-talk.mk` and `maketalk.py`. This is Phase 4 of CIP-000D.

Pattern follows `lamd/makefiles/make-manim.mk` (CIP-000C). The key difference is the render command uses `manim --renderer svg` rather than `manim-slides render`, and the convert step is replaced by `python -m lamd.util.svg_to_html`.

## Acceptance Criteria

- [ ] `make-svg-manim.mk` exists at `lamd/makefiles/make-svg-manim.mk`
- [ ] Three targets defined:
  - `%.manim-svg.py` — preprocess step (calls `${PP} --to manim-svg`)
  - `${BASE}.manim-svg.rendered` — render step (calls `manim --renderer svg`)
  - `${BASE}.manim-svg.html` — generate step (calls `python -m lamd.util.svg_to_html`)
- [ ] `.PHONY: manim-svg` target that builds `${BASE}.manim-svg.html`
- [ ] `make-talk.mk` includes `make-svg-manim.mk` alongside `make-manim.mk` (one `include` line added, nothing else changed)
- [ ] `maketalk.py` accepts `manim-svg` as a valid `--to` choice and invokes `make manim-svg`
- [ ] Variables `MANIMSVGFLAGS` (for `manim` render flags) and `MANIMSVGJS` (path to `js/manim-svg.js`) are documented in the makefile with sensible defaults

## Implementation Notes

Reference: [`lamd/makefiles/make-manim.mk`](../../lamd/makefiles/make-manim.mk)

Makefile structure:

```makefile
# SVG Manim presentation pipeline (lawrennd/manim SVG renderer)
MANIMSVGFLAGS ?=
MANIMSVGJS ?= $(shell python -c "import manim; import os; print(os.path.join(os.path.dirname(manim.__file__), '..', 'js', 'manim-svg.js'))" 2>/dev/null)

%.manim-svg.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim-svg --format slides --code none ${PPFLAGS} \
		--snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) \
		--diagrams-dir ${DIAGRAMSDIR}

${BASE}.manim-svg.rendered: ${BASE}.manim-svg.py
	manim ${MANIMSVGFLAGS} --renderer svg $< Talk
	touch $@

${BASE}.manim-svg.html: ${BASE}.manim-svg.rendered
	python -m lamd.util.svg_to_html media/svg/Talk ${BASE}.manim-svg.html \
		--title "$(TITLE)" --js-src "$(MANIMSVGJS)"

.PHONY: manim-svg
manim-svg: ${BASE}.manim-svg.html
```

## Related

- CIP: 000D
- Backlog: 2026-05-06_cip000d-mdpp-to-manim-svg (dependency)
- Backlog: 2026-05-06_cip000d-svg-to-html (dependency)

## Progress Updates

### 2026-05-06
Task created with Proposed status.
