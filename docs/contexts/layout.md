# Layout Context

The layout context manages the visual arrangement of content across different output formats, handling columns, alignment, and spacing.

## Key Macros

### Column Layout
```markdown
\columns{one}{two}{width1}{width2}
    Creates two-column layout
    Args:
        one: Left column content
        two: Right column content
        width1: Left column width
        width2: Right column width

\threeColumns{one}{two}{three}{width1}{width2}{width3}
    Creates three-column layout
    Args:
        one/two/three: Column contents
        width1/2/3: Column widths
```

### Alignment
```markdown
\aligncenter{block}
    Centers content horizontally
    Args:
        block: Content to center

\alignright{block}
    Right-aligns content
    Args:
        block: Content to align

\alignleft{block}
    Left-aligns content
    Args:
        block: Content to align
```

### Containers
```markdown
\div{contents}{class}{style}
    Creates a generic container
    Args:
        contents: Container content
        class: CSS class
        style: CSS styling

\span{contents}{class}{style}
    Creates an inline container
    Args:
        contents: Inline content
        class: CSS class
        style: CSS styling
```

### Text Styling
```markdown
\largetext{block}
    Increases text size
    Args:
        block: Text to enlarge

\smalltext{block}
    Decreases text size
    Args:
        block: Text to reduce
```

### Additional Layout Controls

```markdown
\xrightarrow{block}
    Creates right arrow with text
    Args:
        block: Arrow label text

\small{block}
    Makes text small in all formats
    Args:
        block: Text to reduce

\raw{block}{options}
    Inserts raw content
    Args:
        block: Raw content
        options: Format options
```

Example usage:
```markdown
Model input \xrightarrow{transform} Model output

\small{Note: Results may vary}

\raw{<custom-element>Content</custom-element>}{html}
```

## Example Usage

```markdown
\ifndef{layoutExample}
\define{layoutExample}

\section{Comparison of Methods}

\columns{
    \aligncenter{
        \largetext{Method A}
        \includediagram{method-a}{90%}
    }
}{
    \aligncenter{
        \largetext{Method B}
        \includediagram{method-b}{90%}
    }
}{50%}{50%}

\div{
    \smalltext{* Results based on experimental data}
}{footnote}{padding: 1em;}

\endif
```

## Format-Specific Behavior

### HTML/Slides
- Flexible CSS-based layouts
- Responsive design support
- Dynamic alignment

### PDF/LaTeX
- Fixed column widths
- Precise alignment control
- Consistent spacing

### Word/PPTX
- Table-based layouts
- Native alignment support
- Consistent margins

## Best Practices

1. Use relative widths when possible
2. Consider mobile responsiveness
3. Test layouts in all output formats
4. Maintain consistent spacing
5. Use semantic class names
6. Consider accessibility
