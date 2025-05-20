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

### Animation Controls

```markdown
\startanimation{group}{start}{finish}{name}
    Controls multi-step animations
    Args:
        group: Animation group identifier
        start: Starting frame number
        finish: Ending frame number
        name: Animation name for reference

\newframe{contents}{name}{style}
    Creates individual animation frame
    Args:
        contents: Frame content
        name: Frame identifier
        style: CSS styling for frame

\endanimation
    Ends an animation sequence
    No arguments
```

Example animation:
```markdown
\startanimation{neural-net}{1}{5}{Neural Network Training}

\newframe{\includediagram{nn-frame1}{80%}}{frame1}{}
\newframe{\includediagram{nn-frame2}{80%}}{frame2}{}
\newframe{\includediagram{nn-frame3}{80%}}{frame3}{}

\endanimation
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

