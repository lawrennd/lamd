---
author: "Neil Lawrence"
created: "2026-05-06"
id: "000D"
last_updated: "2026-05-06"
accepted: "2026-05-06"
status: "Accepted"
compressed: false
related_requirements: []
related_cips: ["000C"]
tags:
- cip
- manim
- svg
- revealjs
- slides
- animation
- output-format
title: "SVG-Based Manim Output Format"
---

# CIP-000D: SVG-Based Manim Output Format

## Status

- [x] Proposed - Initial idea documented
- [x] Accepted - Approved, ready to start work
- [ ] In Progress - Actively being implemented
- [ ] Implemented - Work complete, awaiting verification
- [ ] Closed - Verified and complete
- [ ] Rejected - Will not be implemented
- [ ] Deferred - Postponed

## Summary

Add a `--to manim-svg` output format to LaMD that uses the SVG renderer from [lawrennd/manim](https://github.com/lawrennd/manim) instead of `manim-slides`. Rather than encoding each animation as an MP4 video clip, the SVG renderer exports per-frame SVG files and an `animation.json` manifest per animation block. A companion JavaScript plugin (`js/manim-svg.js`) plays these back in RevealJS by cycling through SVG frames as CSS `background-image` updates on the slide's background layer.

This CIP is related to CIP-000C (Manim Slides Output Format), which it supplements. CIP-000C's `--to manim` pipeline remains unchanged; this CIP adds a parallel, independent `--to manim-svg` pipeline that produces lossless vector output with no video codec dependency.

## Motivation

CIP-000C's `manim-slides` render step produces one MP4 per animation segment. This creates several problems for web presentations:

- **Video codec dependency**: browsers require codec negotiation; VP9/H.264 support varies
- **Autoplay policies**: browsers block autoplay video by default; presenters must click to start
- **Rasterization**: MP4 encodes pixel data at a fixed resolution; zooming reveals compression artefacts
- **File size**: even short animations produce multi-MB MP4s; 60 SVG frames are typically a few hundred KB
- **No vector precision**: mathematical equations and diagrams, which Manim stores internally as Bézier curves, are immediately rasterised to pixels by the video encoder

The SVG renderer in [lawrennd/manim](https://github.com/lawrennd/manim) (CIP-0001 in that repo) preserves the vector geometry throughout. Each `self.play()` call produces a directory of numbered SVG frames and an `animation.json` manifest. The `js/manim-svg.js` plugin cycles through them in RevealJS by updating the `.slide-background` CSS layer — no video element, no codec, no autoplay policy.

This aligns with LaMD's `web-native-output` and `mathematical-precision` tenets and with the broader goal of single-source authoring with high-fidelity web output.

## Detailed Description

### Pipeline Architecture

```
.md  →  gpp (talk-macros-slides-svg-manim.gpp)  →  mytalk.manim-svg.py
     →  manim --renderer svg mytalk.manim-svg.py Talk
     →  media/svg/Talk/
          animation_0/  frame_0000.svg … frame_NNNN.svg  animation.json
          animation_1/  …
          …
     →  python -m lamd.util.svg_to_html media/svg/Talk mytalk.manim-svg.html
```

The GPP preprocessing step and the Python header injection in `mdpp.py` follow exactly the same pattern as CIP-000C's `--to manim` path; only the loaded macro file, the Python class header, and the render/convert commands differ.

### Python Class Structure

`mdpp.py` injects a constant header before the GPP-processed body:

```python
from manim import *
from manim.constants import RendererType

config.renderer = RendererType.SVG

class Talk(Scene):
    def construct(self):
```

This is a standard Manim `Scene` (not a `manim-slides` `Slide`). There is no `self.next_slide()`. Each `self.play()` call in `construct()` produces one `animation_N/` directory under `media/svg/Talk/`.

### GPP Macro File

`talk-macros-slides-svg-manim.gpp` is intentionally thin. The shared `talk-macros-manim.gpp` (unchanged) already provides `\slides{}`, `\notes{}`, `\speakernotes{}`, `\slidesincremental{}`, `\fragment{}`, `\displaymath{}`, `\includediagram{}`, `\includeimg{}`, and `\slidesmanim{}`. The only macro that differs from CIP-000C's slides path is `\newslide`: in the SVG pipeline it does not call `self.next_slide()` because there is no `Slide` class.

```gpp
\ifndef{talkMacrosSlidessvgManim}
\define{talkMacrosSlidessvgManim}

\define{\newslide{title}{commands}}{
        self.play(FadeIn(lamd_text(r"""\title""")))}

\define{\subsection{title}}{
        self.play(FadeIn(lamd_text(r"""\title""")))}

\define{\subsubsection{title}}{
        self.play(FadeIn(lamd_text(r"""\title""")))}

\define{\section{title}}{
        self.play(FadeIn(lamd_text(r"""\title""")))}

\define{\slidesincremental{items}}{
        self.play(FadeIn(lamd_text(r"""\items""")))}

\endif
```

### HTML Generator (`lamd/util/svg_to_html.py`)

After the render step, the animation directories are at `media/svg/Talk/animation_N/`. The HTML generator:

1. Scans for `animation.json` files (sorted by animation index)
2. Produces one `<section data-manim-svg="..." data-manim-loop="false">` per animation
3. Wraps in a RevealJS boilerplate that includes `js/manim-svg.js` (located via the `lamd` package data or a configurable path)
4. Writes to the output `.html` file

The generated HTML is a self-contained RevealJS presentation; the SVG frame directories must be served from the same origin (or the same local directory via `python -m http.server`).

### Makefile Targets (`make-svg-manim.mk`)

```makefile
# Preprocess: md → Python scene
%.manim-svg.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim-svg --format slides --code none ${PPFLAGS} \
		--snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) \
		--diagrams-dir ${DIAGRAMSDIR}

# Render: Python → SVG frame directories
${BASE}.manim-svg.rendered: ${BASE}.manim-svg.py
	manim ${MANIMSVGFLAGS} --renderer svg $< Talk
	touch $@

# Generate: SVG dirs → RevealJS HTML
${BASE}.manim-svg.html: ${BASE}.manim-svg.rendered
	python -m lamd.util.svg_to_html media/svg/Talk ${BASE}.manim-svg.html \
		--title "$(TITLE)" --js-src $(MANIMSVGJS)

.PHONY: manim-svg
manim-svg: ${BASE}.manim-svg.html
```

The variable `MANIMSVGJS` defaults to the path of `js/manim-svg.js` within the installed `lawrennd/manim` fork (or can be overridden in the user's makefile).

### Dependency

The fork must be installed:

```bash
pip install "manim[svg] @ git+https://github.com/lawrennd/manim.git"
```

This provides both the `manim` CLI with `RendererType.SVG` support and `svgwrite` (via the `[svg]` optional extra).

### Relationship to CIP-000C

CIP-000C's `--to manim` and `--to manim-video` pipelines are unchanged. This CIP adds a third pipeline, `--to manim-svg`, as a sibling. Users who need video-compatible output (PPTX, offline viewing) should continue to use `--to manim`. Users who want lossless vector output for web presentations should use `--to manim-svg`.

### Out of Scope

- Changes to any CIP-000C macro file or makefile
- PPTX or PDF output from the SVG pipeline (SVG frames are not compatible with `manim-slides convert`)
- Continuous MP4 from SVG frames
- Packaging `js/manim-svg.js` as a standalone npm/PyPI package (deferred to a future CIP)

## Implementation Plan

### Phase 1: GPP macro file
Create `lamd/macros/talk-macros-slides-svg-manim.gpp` with `\newslide` (and section variants) that emit `self.play(FadeIn(...))` without `self.next_slide()`. All other macros fall through to `talk-macros-manim.gpp`.

### Phase 2: `mdpp.py` — `--to manim-svg`
Add `manim-svg` to the `--to` choices. Inject the SVG Python header (`config.renderer = RendererType.SVG`, `class Talk(Scene):`). Load `talk-macros-slides-svg-manim.gpp` via the existing GPP flag mechanism.

### Phase 3: HTML generator
Write `lamd/util/svg_to_html.py` as a module callable via `python -m lamd.util.svg_to_html`. Accepts the animation root directory and output HTML path. Reads each `animation.json`, generates the RevealJS slide sections, and copies/inlines `js/manim-svg.js`.

### Phase 4: Makefile and wiring
Write `lamd/makefiles/make-svg-manim.mk`. Include it in `make-talk.mk` alongside the existing `make-manim.mk`. Add `manim-svg` as a target choice in `maketalk.py`.

### Phase 5: Tests
- Unit test: `\newslide` in `manim-svg` format does not contain `next_slide`
- Unit test: `\slides{}` in `manim-svg` format emits `self.play(FadeIn(...))`
- Unit test: `\slidesmanim{}` passthrough works
- Integration test: `mdpp --to manim-svg` on a fixture talk → `py_compile` passes
- Unit test: `svg_to_html.py` produces correct `data-manim-svg` attributes given a mock animation directory tree

## Backward Compatibility

All changes are additive. The new macro file, makefile, and `--to manim-svg` flag are entirely independent of the existing `--to manim` and `--to manim-video` pipelines. No existing macro files, makefiles, or test fixtures are modified.

## Testing Strategy

1. Macro expansion unit tests in `lamd/tests/test_mdpp_manim_svg.py`
2. `py_compile` integration test on generated `.manim-svg.py`
3. HTML structure test: `svg_to_html.py` output contains correct number of `<section data-manim-svg=...>` elements
4. No-op tests: `\slidesmanim{}` is empty string in `html`, `tex`, `notes` formats (already covered by CIP-000C tests; verify no regression)

## Related Requirements

This CIP contributes to the requirement for multiple high-fidelity web output formats from a single LaMD source. It directly implements the `web-native-output` principle: SVG is the natural web format for Manim's internal vector geometry.

## Implementation Status

- [ ] Phase 1: Create `talk-macros-slides-svg-manim.gpp`
- [ ] Phase 2: Add `--to manim-svg` to `mdpp.py`
- [ ] Phase 3: Write `lamd/util/svg_to_html.py`
- [ ] Phase 4: Write `make-svg-manim.mk` and wire into `make-talk.mk`
- [ ] Phase 5: Tests

## References

- [lawrennd/manim](https://github.com/lawrennd/manim) — the SVG renderer fork (CIP-0001 in that repo)
- [js/manim-svg.js](https://github.com/lawrennd/manim/blob/main/js/manim-svg.js) — RevealJS plugin
- [CIP-000C](cip000C.md) — Manim Slides Output Format (manim-slides / MP4 pipeline)
- [talk-macros-manim.gpp](../lamd/macros/talk-macros-manim.gpp) — shared Manim macros (unchanged)
- [make-manim.mk](../lamd/makefiles/make-manim.mk) — reference makefile pattern
