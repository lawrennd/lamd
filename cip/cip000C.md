---
author: "Neil Lawrence"
created: "2026-05-05"
id: "000C"
last_updated: "2026-05-05"
status: "Implemented"
compressed: false
related_requirements: []
related_cips: ["0007"]
tags:
- cip
- manim
- manim-slides
- slides
- animation
- output-format
title: "Manim Slides Output Format"
---

# CIP-000C: Manim Slides Output Format

## Status

- [x] Proposed - Initial idea documented
- [x] Accepted - Approved, ready to start work
- [x] In Progress - Actively being implemented
- [x] Implemented - Work complete, awaiting verification
- [ ] Closed - Verified and complete
- [ ] Rejected - Will not be implemented
- [ ] Deferred - Postponed

## Summary

Add Manim (via `manim-slides`) as a new LaMD output format, enabling authors to generate animated Manim video presentations and Reveal.js HTML slides from the same LaMD markdown source that already produces HTML slides, PDF notes, and PPTX. A new macro `\slidesmanim{code}` allows Manim-specific Python scene code to be embedded inline; existing slide macros (`\newslide`, `\slides`, `\slidesincremental`, `\speakernotes`) are mapped to their `manim-slides` equivalents in a new format-specific macro file.

## Motivation

[Manim](https://docs.manim.community/) is the standard tool for mathematical and scientific animations in academic video presentations (most famously used by 3Blue1Brown). Academics producing talks in LaMD currently have no path to Manim output; they must either maintain a separate Manim codebase or abandon the single-source authoring model. This CIP closes that gap.

The core LaMD tenet *"Write once, present everywhere"* (Single Source, Multiple Contexts) motivates adding Manim as a peer output format alongside `html`, `pptx`, and `tex`. The tenet *Explicit over implicit* motivates the `\slidesmanim{}` escape hatch: Manim-specific code is always visibly annotated, never silently injected.

Note: this CIP is distinct from CIP-0007 (Animation System Improvements), which fixes bugs in the *existing* `\startanimation`/`\newframe`/`\endanimation` HTML animation system. This CIP adds an entirely new output format; the two work streams do not conflict.

## Detailed Description

### Why manim-slides, not raw Manim

The implementation uses [`manim-slides`](https://manim-slides.eertmans.be/) rather than raw `manim` `Scene` classes. `manim-slides` is a thin layer over Manim that provides:

- **`Slide` class** (subclass of `Scene`) — the authoring primitive
- **`self.next_slide()`** — the slide-break method, equivalent to a reveal.js slide advance; creates the pause that the presenter must trigger to advance
- **`next_slide(notes="...")`** — attaches presenter notes (Markdown) to the preceding slide animations
- **`manim-slides convert MyTalk output.html`** — converts rendered animations to a Reveal.js HTML presentation, directly parallel to LaMD's existing pandoc `--to revealjs` path
- **`manim-slides convert MyTalk output.pptx`** — produces PPTX
- **`manim-slides MyTalk`** — runs the Qt live presenter

Because `manim-slides` outputs Reveal.js HTML, the Manim format is not just a video renderer; it is a complete, interactive presentation path. The two-step build (render → convert) maps naturally to a two-target makefile.

### Pipeline architecture

LaMD's existing build pipeline is:

```
.md  →  gpp (format-specific .gpp macros)  →  .slides.<format>.markdown  →  pandoc/tool  →  output
```

The Manim pipeline follows the same pattern but the intermediate file is Python rather than Markdown, and the final tools are the manim-slides CLI rather than pandoc:

```
.md  →  gpp (talk-macros-slides-manim.gpp)  →  .slides.manim.py
     →  manim-slides render (produces animation files in media/)
     →  manim-slides convert  →  .slides.html  (Reveal.js, interactive)
                               →  .slides.pptx  (PowerPoint, embedded video)

.md  →  gpp (talk-macros-video-manim.gpp)   →  .video.manim.py
     →  manim render          →  .video.mp4   (single continuous MP4)
```

The gpp preprocessor step is unchanged; only the set of macro definitions loaded for the `manim` format differs.

### New macro: `\slidesmanim{code}`

`\slidesmanim{code}` emits raw Manim Python code verbatim into the generated `.py` file. It is the escape hatch for Manim-specific constructs (custom Mobjects, camera moves, `VGroup` layouts, etc.) that have no general LaMD equivalent.

In all non-Manim output formats, `\slidesmanim{code}` is a no-op, following the same convention as `\slides{}` (no-op in notes) and `\notes{}` (no-op in slides).

### Text rendering: `MarkupText` + `MathTex`

LaMD slide content can contain plain text, Markdown formatting (`**bold**`, `*italic*`), and inline LaTeX (`$...$`, `\begin{equation}...\end{equation}`). Manim provides three text primitives:

- `Text(r"...")` — plain text via Pango (no formatting)
- `MarkupText(r"...")` — PangoMarkup: accepts `<b>bold</b>`, `<i>italic</i>`, colors
- `MathTex(r"...")` — LaTeX typesetting (requires a LaTeX installation)

The generated `.slides.manim.py` file includes a **helper module** (`_lamd_manim.py`, generated alongside the script) that provides:

```python
def lamd_text(md_string):
    """
    Convert a LaMD markdown string to a Manim VGroup of Text/MathTex objects.
    Inline math ($...$) is rendered as MathTex; surrounding text as MarkupText
    (with ** and * converted to <b> and <i> Pango tags).
    """
```

This keeps the generated scene code clean:

```python
content = lamd_text(r"A **bold** claim: $E = mc^2$")
self.play(FadeIn(content))
```

The helper is regenerated by `mdpp` on each run (it is a build artefact, not user-editable).

### Macro translation table

The file `lamd/macros/talk-macros-slides-manim.gpp` defines the following translations. The generated Python file is a self-contained `manim-slides` script; one class `Talk(Slide)` contains all slides sequentially, with `self.next_slide()` calls marking slide boundaries.

| LaMD macro | Manim Python output |
|---|---|
| `\newslide{Title}` | `self.next_slide()` + `self.wipe(...)` to clear; renders title via `lamd_text` |
| `\slides{text}` | `self.play(FadeIn(lamd_text(r"text")))` |
| `\slidesincremental{items}` | one `self.play(FadeIn(lamd_text(r"item")))` + `self.next_slide()` per bullet, all items kept on screen (cumulative reveal) |
| `\speakernotes{text}` | passed as `notes=r"text"` to the preceding `self.next_slide(...)` call |
| `\notes{text}` | no-op |
| `\slidesmanim{code}` | verbatim Python code, inserted directly into `construct()` |
| `\section{text}` | `self.next_slide()` + full-screen section title card via `lamd_text` |
| `\fragment{text}{type}` | `self.play(FadeIn(lamd_text(r"text")))` + `self.next_slide()` |

**One class for the whole talk**: unlike plain Manim (one class per slide), `manim-slides` works best with a single `Slide` subclass whose `construct()` method uses `self.next_slide()` to demarcate slides. This means the entire talk becomes one Python class:

```python
from manim import *
from manim_slides import Slide
from _lamd_manim import lamd_text

class Talk(Slide):
    def construct(self):
        # --- Slide 1 (title slide) ---
        title = lamd_text(r"My Talk Title")
        self.play(FadeIn(title))
        self.next_slide()

        # --- Slide 2 ---
        self.wipe(self.mobjects_without_canvas, [])
        heading = lamd_text(r"Introduction")
        self.play(FadeIn(heading))
        item1 = lamd_text(r"First point")
        self.play(FadeIn(item1))
        self.next_slide()  # incremental reveal
        item2 = lamd_text(r"Second point")
        self.play(FadeIn(item2))
        self.next_slide(notes=r"Remember to pause here")

        # \slidesmanim{} verbatim code:
        circle = Circle()
        self.play(Create(circle))
        self.next_slide()
```

### Build targets: `make-manim.mk`

```makefile
# Preprocess: md → Python script
%.slides.manim.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim --format slides --code none \
	    ${PPFLAGS} --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR)

# Render: Python → animation files (in media/)
${BASE}.slides.manim.rendered: ${BASE}.slides.manim.py
	manim-slides render ${MANIMFLAGS} $< Talk
	touch $@

# Convert: animation files → Reveal.js HTML
${BASE}.slides.html: ${BASE}.slides.manim.rendered
	manim-slides convert ${MANIMCONVERTFLAGS} Talk ${BASE}.slides.html

# Convert: animation files → PPTX
${BASE}.slides.pptx: ${BASE}.slides.manim.rendered
	manim-slides convert --to=pptx ${MANIMCONVERTFLAGS} Talk ${BASE}.slides.pptx
```

The render step is separated from the convert step so that multiple output formats can share one render pass.

### Separate video (MP4) pipeline: `make-video-manim.mk`

`manim-slides convert` does **not** support `--to=mp4`; its output formats are `html`, `pptx`, `pdf`, and `zip`. For a single continuous MP4, a separate pipeline using raw Manim (without `manim-slides`) is needed.

The key semantic difference between the two pipelines is in the generated `construct()` method:

- **`manim-slides` path**: inserts `self.next_slide()` calls at slide boundaries to create presenter-controlled pauses; the `Slide` class captures each segment as a separate animation clip.
- **Raw Manim path**: generates one linear `Scene` with no pause points; slide transitions are visual wipes or fades that play automatically; the result is a single MP4.

A second macro file `talk-macros-video-manim.gpp` handles this translation: `\newslide`, `\slides`, and `\slidesincremental` are mapped to in-scene animations without `self.next_slide()` calls, and `\speakernotes` becomes a no-op (video has no presenter notes).

```makefile
# Preprocess: md → Python script (linear Scene, no slide breaks)
%.video.manim.py: %.md ${DEPS}
	${PP} $< -o $@ --to manim-video --format slides --code none \
	    ${PPFLAGS} --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR)

# Render: Python → MP4 (raw manim, single output file)
${BASE}.video.mp4: ${BASE}.video.manim.py
	manim ${MANIMFLAGS} $< Talk -o ${BASE}.video.mp4
```

### YAML frontmatter options

Authors can control Manim rendering via a `manim:` block in the talk's YAML frontmatter:

```yaml
manim:
  quality: medium       # low | medium | high | fourk  (default: medium)
  fps: 30               # frames per second (default: 30)
  background_color: BLACK  # any Manim color name (default: BLACK)
  scene_class: Talk     # name of the generated Slide class (default: Talk)
```

`maketalk.py` (or the generated makefile) extracts these fields and passes them as `MANIMFLAGS` / `MANIMCONVERTFLAGS` to the respective CLI invocations.

### `_lamd_manim.py` helper module

The preprocessor generates `_lamd_manim.py` alongside `mytalk.slides.manim.py`. It provides:

```python
import re
from manim import *

def _md_to_pango(text):
    """Convert ** and * markdown to Pango <b> and <i> tags."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    return text

def lamd_text(md_string, font_size=36, **kwargs):
    """
    Parse a LaMD markdown string into a VGroup of Manim objects.
    Inline math ($...$) → MathTex; surrounding text → MarkupText.
    Returns a VGroup arranged vertically.
    """
    parts = re.split(r'(\$[^$]+\$)', md_string)
    mobjects = []
    for part in parts:
        if part.startswith('$') and part.endswith('$'):
            latex = part[1:-1]
            mobjects.append(MathTex(latex, font_size=font_size, **kwargs))
        elif part.strip():
            mobjects.append(MarkupText(_md_to_pango(part), font_size=font_size, **kwargs))
    if not mobjects:
        return VGroup()
    if len(mobjects) == 1:
        return mobjects[0]
    return VGroup(*mobjects).arrange(RIGHT)
```

Display math (`$$...$$` or `\begin{equation}...\end{equation}`) is handled by a separate `lamd_display_math(latex_string)` function that returns a centred `MathTex` at larger size.

### Relationship to `mdpp.py` / `--to` flag

`mdpp.py` already accepts `--to html`, `--to pptx`, `--to tex`, etc. Adding `--to manim`
and `--to manim-video` required several changes to `mdpp.py`:

- **GPP flag injection**: `--to manim` sets `-DMANIM=1 -DSLIDES=1`; `--to manim-video`
  sets `-DMANIM=1 -DVIDEO=1`. This fires the correct `\ifdef` guards in `talk-macros.gpp`
  so that the appropriate Manim macro file is included.
- **Python class header injection**: instead of relying on GPP macros to emit the
  `from manim import *` preamble and `class Talk(Slide): def construct(self):` header,
  `mdpp.py` injects a constant Python header string (`_MANIM_SLIDES_HEADER` or
  `_MANIM_VIDEO_HEADER`) directly before the GPP-processed body. This avoids GPP
  consuming the first line of the header.
- **Post-processing strip**: GPP emits verbatim content from included `.gpp` files
  (HTML comments, TeX `%` comments) before the Python code starts. A post-processing
  step reads the generated file, finds the first line beginning with `from manim import`,
  and discards everything before it.
- **Helper copy**: after `gpp` runs, `mdpp.py` copies `lamd/util/lamd_manim_helper.py`
  to `_lamd_manim.py` in the output directory so the generated script can import it.

### What is out of scope

- Changes to any existing macro file (no regressions possible)
- Integration with CIP-0007's `\startanimation`/`\newframe` HTML system
- Full Manim Python API coverage (goal is useful defaults, not complete wrapping)
- Block-level math in `lamd_text` (display math via `\begin{equation}` is handled separately)
- Non-English / RTL text layout (Pango supports it, but not tested)

## Implementation Plan

### Phase 1: Macro skeleton + text slides

1. Create `lamd/macros/talk-macros-slides-manim.gpp` with:
   - `\newslide{title}` → `self.next_slide()` + wipe + title rendering
   - `\slides{text}` → `self.play(FadeIn(lamd_text(r"...")))`
   - `\notes{text}` → no-op
   - `\speakernotes{text}` → `notes=r"..."` argument on preceding `next_slide()`
2. Create `lamd/util/lamd_manim_helper.py` (source for the generated `_lamd_manim.py`) implementing `lamd_text`, `lamd_display_math`, `_md_to_pango`
3. Add `--to manim` handling in `mdpp.py`: load the new `.gpp` file and write `_lamd_manim.py` to the output directory
4. Manual smoke test: run `mdpp` on a minimal talk, verify valid Python + `python -m py_compile`

### Phase 2: `\slidesmanim{}` + build target

1. Add `\slidesmanim{code}` macro definition (verbatim passthrough in manim format, no-op elsewhere — add no-op to `talk-macros-notes.gpp`, `talk-macros-slides-html.gpp`, etc.)
2. Create `lamd/makefiles/make-manim.mk` with the two-step targets (preprocess → render → convert)
3. Create `lamd/makefiles/make-video-manim.mk` with the two-step targets for raw MP4 (preprocess → render)
4. Create `talk-macros-video-manim.gpp` with linear `Scene` translations (no `self.next_slide()`, `\speakernotes` is a no-op)
5. Wire both into `make-talk.mk` via `include` directives
6. Add `manim` and `manim-video` to `maketalk.py` `--to` choices
7. Extract `manim:` frontmatter block and pass as `MANIMFLAGS` / `MANIMCONVERTFLAGS`

### Phase 3: Incremental reveals

1. Implement `\slidesincremental{items}` — parse bullet list, generate one `FadeIn` + `next_slide()` per item (keeping previous items on screen: cumulative reveal)
2. Implement `\fragment{text}{type}` → `FadeIn` + `next_slide()` (type-aware refinement deferred to Phase 4)
3. Ensure correct vertical stacking of bullet items using `VGroup().arrange(DOWN)`

### Phase 4: Math and figure macros

1. Implement `\begin{equation}...\end{equation}` → `lamd_display_math()`
2. Implement `\includediagram` / `\includepng` → Manim `ImageMobject`
3. Refine `\fragment{text}{type}` to use Manim animation types matching reveal.js fragment names where possible

### Phase 5: Tests and documentation

1. Unit tests: verify macro expansion for `\newslide`, `\slides`, `\slidesmanim`, `\speakernotes`, `\slidesincremental` produce correct Python tokens
2. No-op tests: assert that `\slidesmanim{code}` expands to empty string in `html`, `tex`, and `notes` formats
3. Integration test: run `mdpp --to manim` on a fixture talk and assert the `.py` file passes `python -m py_compile`
4. Update `docs/` with a Manim output format guide including dependency requirements (`pip install manim manim-slides`)
5. Add a worked example in the snippets repository

## Backward Compatibility

All changes are additive:

- New macro file `talk-macros-slides-manim.gpp` — no effect on existing formats
- New makefile `make-manim.mk` — only included when Manim format is requested
- `\slidesmanim{code}` — no-op in all existing formats (added as empty define to existing macro files)
- `--to manim` flag — new option, existing `--to html` etc. are unchanged
- YAML `manim:` block — ignored by all existing build paths
- `_lamd_manim.py` — a build artefact, never committed, no impact on version control

No existing talks, macros, or build targets are modified. Full backward compatibility is guaranteed.

## Testing Strategy

1. **Unit tests** (`lamd/tests/`): macro expansion tests asserting the Python text output of each macro in `manim` format
2. **No-op tests**: assert that `\slidesmanim{code}` expands to empty string in `html`, `tex`, `notes` formats
3. **Integration test**: run `mdpp` on a fixture talk with `--to manim`, validate the generated `.py` is syntactically valid Python (via `python -m py_compile`)
4. **Helper tests**: test `lamd_text()` for plain text, markdown formatting, inline math, and mixed content
5. **Build test** (optional, CI): if `manim` and `manim-slides` are installed, run `manim-slides render --dry-run` to verify the generated script loads without error

## Related Requirements

This CIP contributes to the broad requirement that LaMD support multiple output formats from a single source. No existing numbered requirement directly covers Manim output; a new requirement may be created as part of accepting this CIP.

## Implementation Status

- [x] Phase 1: Create `talk-macros-slides-manim.gpp` skeleton (`\newslide`, `\slides`, `\notes`, `\speakernotes`)
- [x] Phase 1: Create `lamd/util/lamd_manim_helper.py` with `lamd_text`, `lamd_display_math`, `_md_to_pango`
- [x] Phase 1: Add `--to manim` support in `mdpp.py` (load new `.gpp`, write `_lamd_manim.py`)
- [x] Phase 1: Smoke test with minimal talk (`py_compile` check)
- [x] Phase 2: Add `\slidesmanim{}` macro (manim passthrough + no-op in all other formats)
- [x] Phase 2: Create `lamd/makefiles/make-manim.mk` (preprocess → render → convert targets for html/pptx)
- [x] Phase 2: Create `talk-macros-video-manim.gpp` (linear Scene translations, no slide breaks)
- [x] Phase 2: Create `lamd/makefiles/make-video-manim.mk` (preprocess → raw manim render → mp4)
- [x] Phase 2: Wire both makefiles into `make-talk.mk`
- [x] Phase 2: Add `manim` and `manim-video` to `maketalk.py` `--to` choices
- [x] Phase 2: Extract `manim:` frontmatter and pass as `MANIMFLAGS` / `MANIMCONVERTFLAGS`
- [x] GPP refactor: Create `talk-macros-manim.gpp` (shared definitions common to slides and video)
- [x] GPP refactor: Trim `talk-macros-slides-manim.gpp` to slide-break macros only (`self.next_slide()`)
- [x] GPP refactor: Trim `talk-macros-video-manim.gpp` to video-break macros only (`self.wait(1)`)
- [x] GPP refactor: Update `talk-macros.gpp` to two-level include structure (`\ifdef{MANIM}` for shared; `\ifdef{SLIDES}\ifdef{MANIM}` and `\ifdef{VIDEO}\ifdef{MANIM}` for format-specific)
- [x] GPP refactor: Update `mdpp.py` flags (`-DSLIDES=1` for `--to manim`; `-DVIDEO=1` replacing `-DMANIM_VIDEO` for `--to manim-video`)
- [x] Phase 3: `\slidesincremental{}` → `FadeIn` + `next_slide()` (simplified single-object; per-bullet deferred to Phase 6+)
- [x] Phase 3: `\fragment{text}{type}` → `FadeIn`
- [x] Phase 4: Display math macros → `lamd_display_math()`
- [x] Phase 4: Figure macros → `SVGMobject` / `ImageMobject`
- [x] Phase 5: Unit and integration tests (`test_mdpp_manim.py` — 24 tests passing)
- [x] Phase 5: Documentation in `docs/guides/manim-output.md`
- [x] Phase 6: `\htmlmanim{html_content}{manim_alt}` dispatching macro (HTML shows html_content, Manim shows manim_alt, all others no-op)

## References

- [manim-slides documentation](https://manim-slides.eertmans.be/)
- [manim-slides API reference](https://manim-slides.eertmans.be/latest/reference/api.html)
- [manim-slides Quickstart](https://manim-slides.eertmans.be/latest/quickstart.html)
- [Manim Community Edition: Rendering Text and Formulas](https://docs.manim.community/en/latest/guides/using_text.html)
- [`lamd/macros/talk-macros-slides-html.gpp`](../lamd/macros/talk-macros-slides-html.gpp) — existing HTML slides macros (reference for pattern)
- [`lamd/macros/talk-macros-slides.gpp`](../lamd/macros/talk-macros-slides.gpp) — base slides macros (`\slides`, `\slidesincremental`, `\newslide`)
- [`lamd/makefiles/make-slides.mk`](../lamd/makefiles/make-slides.mk) — reference makefile for slides build targets
- CIP-0007: Animation System Improvements (fixes HTML animation bugs; independent of this CIP)
