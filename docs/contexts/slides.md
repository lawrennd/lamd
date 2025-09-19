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

The animation system creates interactive animations in HTML slides with fallback support for other formats.

#### HTML Slides (Interactive)
```markdown
\startanimation{group}{start}{finish}{name}
    Creates interactive animation controls
    Args:
        group: Animation group identifier (used in JavaScript)
        start: Starting frame number (minimum slider value)
        finish: Ending frame number (maximum slider value)
        name: Display name for the animation
    Output: Range slider, navigation buttons, JavaScript initialization
    Requirements: figure-animate.js JavaScript library

\newframe{contents}{name}{style}
    Creates individual animation frame
    Args:
        contents: Frame content
        name: CSS class name for show/hide logic
        style: CSS styling for frame
    Output: HTML div with specified class and styling

\endanimation
    Closes animation sequence
    Output: Closes animation container div
```

#### Other Formats (Fallback)
- **Notes**: Shows all frames with clear labeling
- **IPynb**: Displays frames as structured sections
- **Graceful degradation** ensures content is always visible

#### JavaScript Dependencies
- Requires `figure-animate.js` library
- Functions: `showDivs()`, `setDivs()`, `plusDivs()`
- Loaded via: `https://inverseprobability.com/assets/js/figure-animate.js`

#### Accessibility Features
- ARIA labels for screen readers
- Proper labeling for range sliders
- Keyboard navigation support
- Semantic HTML structure

Example animation:
```markdown
\startanimation{neural-net}{1}{5}{Neural Network Training}

\newframe{\includediagram{nn-frame1}{80%}}{frame1}{}
\newframe{\includediagram{nn-frame2}{80%}}{frame2}{}
\newframe{\includediagram{nn-frame3}{80%}}{frame3}{}

\endanimation
```

#### Troubleshooting
- **Animations not working**: Check that `figure-animate.js` is loaded
- **Frames not showing**: Verify JavaScript console for errors
- **Accessibility issues**: Ensure ARIA labels are properly set

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

