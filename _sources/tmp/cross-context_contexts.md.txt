# Cross-Context Features

Some LAMD features work across multiple contexts, adapting their behavior to the output format while maintaining consistent syntax.

## Universal Macros

### Text Formatting
```markdown
\linebreak
    Creates appropriate line break for format
    No arguments
    Behavior:
        - HTML: <br>
        - LaTeX: \\
        - Slides: Slide break

\href{url}{text}
    Creates hyperlink
    Args:
        url: Link target
        text: Link text
    Behavior:
        - HTML: Clickable link
        - PDF: Underlined link
        - Slides: Interactive link
```

### Conditional Processing
```markdown
\ifdef{FORMAT}
    Includes content only if FORMAT is defined
    Examples:
        \ifdef{SLIDES} Slides only \endif
        \ifdef{NOTES} Notes only \endif
        \ifdef{DRAFT} Draft content \endif

\comment{text}
    Adds hidden comment
    Args:
        text: Comment content
    Behavior:
        - Never appears in output
        - Preserved in source
```

### Style Control
```markdown
\color{name}{text}
    Applies color to text
    Args:
        name: Color name/code
        text: Text to color
    Behavior:
        - HTML: CSS color
        - LaTeX: LaTeX color
        - Slides: Theme-aware color
```

## Content Adaptation

### Format Detection
Content can detect and adapt to its context:

```markdown
\ifdef{SLIDES}
    \slides{Concise version}
\else
    \notes{Detailed version}
\endif
```

### Media Handling
Images and figures adapt to context:

```markdown
\figure{contents}{caption}{label}
Behavior:
    - Slides: Full-width, minimal caption
    - Notes: Formatted figure with caption
    - PDF: Float placement
```

## Example of Cross-Context Usage

```markdown
\ifndef{adaptiveContent}
\define{adaptiveContent}

\section{Adaptive Example}

% Content adapts to format
\ifdef{SLIDES}
    \slides{
        * Key Point 1
        * Key Point 2
    }
\else
    \notes{
        This detailed explanation provides in-depth understanding...
    }
\endif

% Link works everywhere
\href{https://example.com}{More Information}

% Figure adapts to context
\figure{\includediagram{example}{80%}}
{This caption adapts to format}{fig:example}

\endif
```

## Best Practices

1. Format Awareness
   - Consider all output formats
   - Test in each context
   - Provide appropriate fallbacks

2. Consistent Usage
   - Use consistent macro patterns
   - Maintain style across contexts
   - Document format-specific behavior

3. Progressive Enhancement
   - Start with basic content
   - Add format-specific enhancements
   - Ensure graceful fallbacks

4. Testing
   - Verify behavior in each context
   - Check format-specific features
   - Validate cross-format compatibility
