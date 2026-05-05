# Manim Output

LaMD can compile a talk into Manim presentations and videos through two pipelines:

| Pipeline | `--to` flag | Output |
|---|---|---|
| Interactive presentation | `manim` | `.manim.html` and `.manim.pptx` via `manim-slides` |
| Continuous video | `manim-video` | `.manim-video.mp4` via raw Manim |

## Prerequisites

- [Manim](https://www.manim.community/) (`pip install manim`)
- [manim-slides](https://eertmans.be/manim-slides/) (`pip install manim-slides`) — interactive pipeline only

## Writing a Manim Talk

Use the same macros you use for other LaMD outputs. The Manim pipeline automatically
translates them into Manim Python code:

| LaMD macro | Manim output |
|---|---|
| `\slides{text}` | `self.play(FadeIn(lamd_text(r"""text""")))` |
| `\newslide{Title}{}` | `self.next_slide()` + title FadeIn |
| `\slidesincremental{...}` | `self.play(FadeIn(...))` then `self.next_slide()` (interactive) |
| `\fragment{text}{type}` | `self.play(FadeIn(lamd_text(r"""text""")))` |
| `\includediagram{file}{width}{}{}` | `SVGMobject("file.svg")` + FadeIn |
| `\includeimg{file}{width}{}` | `ImageMobject("file")` + FadeIn |
| `\displaymath{expr}` | `self.play(FadeIn(lamd_display_math(r"""expr""")))` |
| `\notes{text}` | suppressed (no-op) |
| `\speakernotes{text}` | Python comment |

### `\slidesmanim` — Raw Manim Code

For effects not expressible through standard macros, use `\slidesmanim{code}` to
inject Python code directly into the `construct` method. This block is a **no-op**
in all non-Manim output formats (HTML, PDF, PPTX, etc.), making it safe to include
in any talk file.

```markdown
\slidesmanim{
        _title = Text("My Talk", font_size=60)
        self.play(Write(_title))
        self.wait(1)
        self.play(FadeOut(_title))
}
```

## Building

### Interactive presentation (HTML + PPTX)

```bash
maketalk your-talk.md --to manim
```

This runs:
1. `mdpp your-talk.md --to manim` → `your-talk.manim.py`  (a `manim-slides` `Slide` subclass)
2. `manim-slides render your-talk.manim.py Talk -ql`
3. `manim-slides convert --to html Talk your-talk.manim.html`
4. `manim-slides convert --to pptx Talk your-talk.manim.pptx`

### Continuous video (MP4)

```bash
maketalk your-talk.md --to manim-video
```

This runs:
1. `mdpp your-talk.md --to manim-video` → `your-talk.manim-video.py`  (a raw Manim `Scene` subclass)
2. `manim render your-talk.manim-video.py Talk -ql`
3. Copies `media/videos/.../Talk.mp4` → `your-talk.manim-video.mp4`

## YAML Frontmatter

Use the `manim:` and `manim-convert:` blocks to pass extra flags to the render
and convert steps respectively:

```yaml
---
title: My Talk
manim: "--disable_caching"
manim-convert: "--open"
---
```

These are passed to `manim-slides render` (`MANIMFLAGS`) and
`manim-slides convert` (`MANIMCONVERTFLAGS`) via the Makefile.

## Helper Module

LaMD auto-generates a `_lamd_manim.py` file alongside the output `.py` file.
This provides:

- `lamd_text(markdown_string)` — converts Markdown + LaTeX to a Manim `MarkupText`
  or `MathTex` object.
- `lamd_display_math(latex_string)` — wraps a LaTeX expression in a `MathTex` object.

Do not edit `_lamd_manim.py` directly; it is regenerated each time `mdpp` runs.

## Known Limitations

- **Per-bullet incremental animation** (`\slidesincremental`) currently animates the
  entire bullet list as a single object.  True per-bullet `FadeIn` is deferred to a
  future phase (CIP-000C Phase 6+).
- **Text styling**: only basic Pango markup is supported inside `lamd_text`.
  Complex LaTeX formatting is not rendered; use `\displaymath` for formulae.
- **Image formats**: `\includediagram` expects an SVG file; `\includeimg` expects
  a raster image path accepted by Manim's `ImageMobject`.
