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

## HTML and JavaScript Content

Manim output is Python code, so raw HTML tags and JavaScript are not valid inside
it.  Always wrap HTML-only content in `\html{}`, which is a **no-op** in all
non-HTML formats (including both Manim pipelines).

```markdown
\figure{\html{
<div style="width:100%">
  <canvas id="my-canvas"></canvas>
  <button id="my-btn">Reset</button>
</div>
\include{_scripts/includes/my-widget-js.md}
}}{Figure caption}{fig-label}
```

In HTML slide output the `\html{}` wrapper expands normally, producing the
interactive widget.  In Manim (and PDF, PPTX, etc.) the entire block is
suppressed.  If you omit `\html{}`, `mdpp` will generate a Python file
containing raw HTML tags, which will fail with a `SyntaxError` when compiled —
this is intentional: the error tells you where the fix needs to go.

### Future: `\htmlmanim{}` dispatching macro

A future enhancement (`backlog/features/2026-05-05_htmlmanim-macro.md`) will
introduce a `\htmlmanim{html_content}{manim_alt}` macro, allowing you to provide
a Manim-native alternative for HTML widgets:

```markdown
\htmlmanim{
  \html{<canvas id="sim"></canvas>\include{_scripts/...}}
}{
  \slidesmanim{
      _img = ImageMobject("simulation-screenshot.png")
      self.play(FadeIn(_img))
  }
}
```

- In HTML output → renders the JS widget (first argument)
- In Manim output → renders the Manim alternative (second argument)
- In all other formats → both arguments are no-ops

## Known Limitations

- **Per-bullet incremental animation** (`\slidesincremental`) currently animates the
  entire bullet list as a single object.  True per-bullet `FadeIn` is deferred to a
  future phase (CIP-000C Phase 6+).
- **Text styling**: only basic Pango markup is supported inside `lamd_text`.
  Complex LaTeX formatting is not rendered; use `\displaymath` for formulae.
- **Image formats**: `\includediagram` expects an SVG file; `\includeimg` expects
  a raster image path accepted by Manim's `ImageMobject`.
