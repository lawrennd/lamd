# Presentation Context

The slides context is used when creating presentations. Content in this context typically appears in reveal.js slides or PowerPoint presentations.

## Key Macros

### Slide Creation
```markdown
\newslide{title}
    Creates a new slide
    Args:
        title: Title of the slide
```

### Content Control
```markdown
\slides{content}
    Specifies content that only appears in slides
    Args:
        content: Slide-specific content, often bullet points
```

### Animation Control
```markdown
\fragment{text}{type}
    Creates animated elements in reveal.js
    Args:
        text: Content to animate
        type: Animation type (e.g., 'fade-in', 'grow')
```

### Presenter Notes
```markdown
\speakernotes{text}
    Adds notes visible only to the presenter
    Args:
        text: Notes for the presenter
```

### Frame Animations (`\startanimation`, `\newframe`, `\endanimation`)

The frame animation system creates multi-step figure sequences in HTML slides: a range
slider and previous/next buttons let the audience step through frames. Other output formats
show all frames without interactive controls.

This is distinct from reveal.js `\fragment{}` animations (bullet-by-bullet reveal on a
single slide).

#### Macro reference

```markdown
\startanimation{group}{start}{finish}{name}
    Opens an animation sequence and renders interactive controls (HTML only).
    Args:
        group: Unique identifier shared by all frames in this sequence. Must match
               the `name` argument of every `\newframe` in the sequence — JavaScript
               uses this value as the CSS class to find frames.
        start: Minimum slider value (typically 0 or 1).
        finish: Maximum slider value. Should equal start + (number of frames − 1)
                when using consecutive numbering.
        name: Human-readable title shown beside the controls and used as the
              container's ARIA label. May be empty if you use the three-argument form
              via `\startslides{group}{start}{finish}`.

\newframe{contents}{name}{style}
    Adds one frame to the current animation sequence.
    Args:
        contents: Frame content (diagrams, text, etc.).
        name: CSS class for this frame — must equal `group` from `\startanimation`.
        style: Optional inline CSS appended to the frame div (e.g. `margin-top:1em`).

\endanimation
    Closes the animation container opened by `\startanimation`.
```

#### Worked example

The pattern below matches real talk content: eight frames numbered 0–7, all sharing the
same `group` class:

```markdown
\startanimation{correlated_velocities}{0}{7}{Correlated velocity samples}

\newframe{\includediagram{\diagramsDir/ml/correlated_velocities000}{\width}}{correlated_velocities}{}
\newframe{\includediagram{\diagramsDir/ml/correlated_velocities001}{\width}}{correlated_velocities}{}
\newframe{\includediagram{\diagramsDir/ml/correlated_velocities002}{\width}}{correlated_velocities}{}
\newframe{\includediagram{\diagramsDir/ml/correlated_velocities003}{\width}}{correlated_velocities}{}
\newframe{\includediagram{\diagramsDir/ml/correlated_velocities004}{\width}}{correlated_velocities}{}
\newframe{\includediagram{\diagramsDir/ml/correlated_velocities005}{\width}}{correlated_velocities}{}
\newframe{\includediagram{\diagramsDir/ml/correlated_velocities006}{\width}}{correlated_velocities}{}
\newframe{\includediagram{\diagramsDir/ml/correlated_velocities007}{\width}}{correlated_velocities}{}

\endanimation
```

#### JavaScript dependency

HTML slide builds load `figure-animate.js` from the slides header template
(`lamd/includes/slides-header.html`):

```html
<script src="https://inverseprobability.com/assets/js/figure-animate.js"></script>
<script>
  /* lamdFrameIndex, lamdSetDivs, lamdPlusDivs — see slides-header.html */
</script>
```

Reference implementation:
[figure-animate.js](https://github.com/lawrennd/jekyll-theme/blob/main/assets/js/figure-animate.js)

The library exposes `showDivs(n, group)` with **1-based** frame indices. LaMD slide
content typically uses **0-based** slider ranges (`\startanimation{group}{0}{4}` for five
frames). The header shim maps slider values to frame indices:

`frameIndex = sliderValue - min + 1`

| Function | Called from | Purpose |
|----------|-------------|---------|
| `showDivs(n, group)` | Init script | Show frame *n* (1-based), hide others with class `group` |
| `lamdSetDivs(group)` | Range slider | Read slider value, map to 1-based index, call `showDivs` |
| `lamdPlusDivs(delta, group)` | Prev/next buttons | Step slider within min/max, then call `showDivs` |

Initialization runs on `DOMContentLoaded` and calls `showDivs(1, group)` so the first
frame matches the slider at its minimum value.
If the script fails to load, lamd degrades gracefully: controls are hidden, the first
frame is shown, and a `[lamd] figure-animate.js not loaded` warning appears in the browser
console.

#### HTML output structure

Each animation sequence renders a container with stable attributes for styling, testing,
and scripting:

| Attribute / element | Purpose |
|---------------------|---------|
| `id="animation-{group}"` | Unique container id |
| `class="lamd-animation"` | Shared class for all animation containers |
| `data-animation-group="{group}"` | Programmatic lookup |
| `role="region"` + `aria-label` | Landmark for assistive technology |
| `.animation-controls` | Wrapper around slider and buttons |
| `data-animation-frame` on each frame | Per-frame identification |

#### Format-specific behaviour

| Format | `\startanimation` | `\newframe` | `\endanimation` |
|--------|-------------------|-------------|-----------------|
| **HTML slides** | Full interactive controls + JS init | Frame div with show/hide class | Closes container |
| **Notes** | Prints `**Animation sequence: {name}**` | Emits frame content | No-op |
| **IPynb** | No-op (HTML macros included, then overridden) | Emits frame content | No-op |
| **TeX / PDF slides** | No-op | Emits frame content | No-op |
| **PPTX** | No-op | Emits frame content | No-op |

In non-HTML formats every frame appears in document order. Authors should write frames
so they read sensibly when shown sequentially (e.g. with diagram captions or brief labels).

#### Accessibility

HTML animations follow [WCAG 2.1](https://www.w3.org/TR/WCAG21/) guidance for interactive
controls:

- **Container**: `role="region"` with `aria-label` set from the `\startanimation` title.
- **Slider**: `aria-label`, `aria-valuemin`, `aria-valuemax`, and `aria-valuenow`.
- **Buttons**: `aria-label="Previous frame"` / `"Next frame"`.
- **Frames**: `role="img"` with `aria-label` from the frame `name` parameter.

Keyboard access uses native control behaviour: Tab to reach the slider and buttons; arrow
keys adjust the range input when it has focus. Provide a descriptive `\startanimation`
title so screen-reader users understand the sequence purpose.

Because every frame currently shares the same `name` class (and thus the same
`aria-label`), put the meaningful description in the visible frame content where possible.

#### Troubleshooting

| Symptom | Likely cause | What to check |
|---------|--------------|---------------|
| Controls appear but frames do not change | `\newframe` `name` ≠ `\startanimation` `group` | Use the same identifier on every frame |
| Slider at left/right shows wrong frame | 0-based slider passed directly to 1-based `showDivs` | Rebuild with current lamd (uses `lamdSetDivs` shim in `slides-header.html`) |
| `[lamd] figure-animate.js not loaded` in console | Script blocked or offline build | Confirm `slides-header.html` is included; check network tab |
| Only first frame visible, no controls | Expected degradation without JS | Enable JavaScript, or rely on noscript/fallback (first frame only) |
| Empty animation area | No `\newframe` calls before `\endanimation` | Add at least one frame between start and end |
| Top slider stops before last frame (nested animations) | `\startanimation` `{finish}` smaller than outer frame count | Set `{finish}` to last index (e.g. six outer frames → `{0}{5}`); count only frames with the outer `group` class |
| Frames flash all at once briefly | Race before `DOMContentLoaded` init | Normal; init hides non-active frames once JS runs |

#### Related macros

```markdown
\fragment{text}{type}
    Reveal.js fragment animation on a single slide (fade-in, grow, etc.) — not frame sequences.

\startslides{group}{start}{finish}
    Shorthand for `\startanimation{group}{start}{finish}` without a display title.
```

### Additional Display Controls

```markdown
\slidesmall{block}
    Makes content smaller in slides only
    Args:
        block: Content to reduce in size

\slidenotes{slidetext}{notetext}
    Different content for slides vs notes
    Args:
        slidetext: Content for slides
        notetext: Content for notes
```

## Example Usage

```markdown
\ifndef{machineLearningIntro}
\define{machineLearningIntro}

\newslide{Introduction to Machine Learning}

\slides{
* Supervised Learning
* Unsupervised Learning
* Reinforcement Learning
}

\fragment{Deep Learning}{fade-in}

\speakernotes{
Remember to mention real-world applications for each type
}

\endif
```

## Output Formats

- reveal.js presentations (HTML)
- PowerPoint (PPTX)

## Tips

1. Keep slide content concise
2. Use fragments for building complex ideas
3. Include speaker notes for important points
4. Consider both HTML and PPTX output when formatting
5. For multi-frame diagrams, use `\startanimation`/`\newframe`/`\endanimation` and repeat
   the same `group` class on every frame (see Frame Animations above)

### Colored math in PPTX

PowerPoint output converts display math through pandoc's TeX→OMML converter. That path
does not support LaTeX `\color{...}{...}` inside `$$...$$` blocks. If color commands
reach pandoc unchanged, the build emits a warning such as:

```text
[WARNING] Could not convert TeX math '... {\color{red}{w_0}} ...', rendering as TeX
```

and the equation may not render correctly in PowerPoint.

For PPTX builds, `talk-macros-pptx.gpp` therefore no-ops color at the gpp stage:

- `\color{name}{text}` → `text`
- `\colorred{...}`, `\colorblue{...}`, and the other `\color*` wrapper macros → content only

Colored math is preserved in HTML slides (MathJax), PDF/LaTeX, and notes. Authors who
need color emphasis in PowerPoint should rely on diagram colors or surrounding slide
text rather than math-mode `\color`.

The same no-op pattern applies when `blackAndWhite` is set in `color-scheme.gpp` for
other formats; PPTX always strips math color regardless of that flag.

