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
