# Media Context

The media context handles all types of media elements including figures, diagrams, videos, and images. It ensures consistent media handling across different output formats.

## Key Macros

### Figures
```markdown
\figure{contents}{caption}{label}
    Creates a complete figure with caption and reference
    Args:
        contents: Figure content (often an \include command)
        caption: Figure caption text
        label: Reference label for citations

\includediagram{filename}{width}{class}{style}
    Includes scalable diagrams (SVG/PNG)
    Args:
        filename: Path to diagram file
        width: Display width (e.g., "80%")
        class: Optional CSS class
        style: Optional CSS styling
```

### Video Content
```markdown
\includeyoutube{id}{width}{height}{start}{end}
    Embeds YouTube video
    Args:
        id: YouTube video ID
        width: Frame width
        height: Frame height
        start: Start time in seconds
        end: End time in seconds

\includevimeo{id}{width}{height}{start}{end}
    Embeds Vimeo video
    Args:
        id: Vimeo video ID
        width/height: Frame dimensions
        start/end: Clip timing

\includempfour{filename}{width}{height}
    Embeds local MP4 video
    Args:
        filename: Path to video file
        width/height: Display dimensions
```

### Images
```markdown
\includeimg{filename}{width}{class}{align}
    Includes generic images
    Args:
        filename: Image path
        width: Display width
        class: CSS class
        align: Alignment option
```

### Attribution (CIP-0016)

Third-party diagrams store TASL metadata in a sibling `{stem}.credit.yml` next to the image (in the filesystem `diagramsdir`, not the web `diagramsurl`). A one-line `{stem}.url` file remains a source-only shorthand and never claims a Creative Commons license.

```yaml
status: third-party   # own | third-party | public-domain | unknown | fair-use | trademark
title: "Portrait of Daniel Bernoulli"
author: "Unknown"
source: https://commons.wikimedia.org/wiki/File:Porträt_des_Daniel_Bernoulli_-_edit1.jpg
license: CC-BY-SA-4.0
license_url: https://creativecommons.org/licenses/by-sa/4.0/
modifications:
  - retouched
```

Credit is opt-in. `\includejpg` / `\includediagram` / `\includeimg` stay image-only. Place `\diagramcredit{stem}` after the figure; mdpp expands it before gpp using the filesystem diagrams root.

```markdown
\figure{\includejpg{\diagramsDir/physics/daniel-bernoulli}{35%}}{Daniel Bernoulli (1700--1782). …}{daniel-bernoulli}
\diagramcredit{\diagramsDir/physics/daniel-bernoulli}
```

| Context | Output |
|---|---|
| HTML / ipynb notes | Full TASL line (`*Credit:*` Title by Author. Source. License.) |
| Reveal HTML slides | Compact, slide-visible, right-aligned (not speaker-notes-only) |
| TeX notes | Same Markdown credit line (pandoc turns links into `\href`) |
| PPTX / DOCX / Manim | Empty in v1 |

`status: own` emits nothing unless `show_own: true`. `fair-use`, `unknown`, and legacy `.url` files render a source link without a CC label. `trademark` emits nothing.

Backfill Wikimedia sidecars (not part of the talk build):

```bash
lamd-backfill-credits --diagrams-dir /path/to/slides/diagrams --dry-run
```

Wikipedia-en uploads are classified as fair use and are never labelled CC. Other hosts stay manual.

The two-argument `\credit{name}{url}` primitive is unchanged for hand-written credits.

### Additional Media Types

```markdown
\includebbcvideo{id}{width}{height}{start}{end}
    Embeds BBC video content
    Args:
        id: BBC programme ID
        width/height: Display dimensions
        start/end: Clip timing

\includeredditvideo{id}{width}{height}{start}{end}
    Embeds Reddit video content
    Args:
        id: Reddit video ID
        width/height: Display dimensions
        start/end: Clip timing

\includepdf{filename}{page}{width}{height}
    Embeds PDF content
    Args:
        filename: PDF file path
        page: Page number
        width/height: Display dimensions

\includepdfclip{filename}{clip}{page}{width}{height}
    Embeds clipped PDF content
    Args:
        filename: PDF file path
        clip: Clip region
        page: Page number
        width/height: Display dimensions

\inlinediagram{svgcode}
    Inserts SVG code directly
    Args:
        svgcode: Raw SVG code
```

## Example Usage

```markdown
\ifndef{mediaExample}
\define{mediaExample}

\section{Neural Networks Visualization}

% Include a diagram
\figure{\includediagram{neural-net}{80%}}
{Architecture of a simple neural network}{fig:neural-net}

% Include a video explanation
\includeyoutube{dQw4w9WgXcQ}{800}{600}{0}{60}

% Include an image series
\columns{
    \includeimg{step1.png}{40%}{centered}{center}
}{
    \includeimg{step2.png}{40%}{centered}{center}
}{50%}{50%}

\endif
```

## Output Format Considerations

### HTML
- Responsive image sizing
- Video player embedding
- Interactive figure controls

### PDF/LaTeX
- High-resolution images
- Vector graphics support
- Static video thumbnails

### Slides
- Optimized image sizes
- Embedded video support
- Animation capabilities

## Best Practices

1. Use vector formats (SVG) when possible
2. Provide appropriate fallbacks
3. Consider bandwidth and loading times
4. Maintain consistent aspect ratios
5. Include meaningful captions
6. Use semantic figure references
7. Credit third-party images with `\diagramcredit` and a sidecar, not by mixing TASL into the pedagogical caption
