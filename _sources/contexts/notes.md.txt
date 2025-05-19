# Documentation Context

The notes context is used for creating detailed documentation, lecture notes, or papers.

## Key Macros

### Content Structure
```markdown
\section{title}
    Creates a major section
    Args:
        title: Section heading

\subsection{title}
    Creates a subsection
    Args:
        title: Subsection heading

\notes{content}
    Specifies content that only appears in documentation
    Args:
        content: Detailed explanatory text
```

### Special Elements
```markdown
\recommendation{text}
    Creates a highlighted recommendation box
    Args:
        text: Recommendation content

\notesfigure{block}
    Includes a figure formatted for documentation
    Args:
        block: Figure content and caption
```

## Example Usage

```markdown
\section{Neural Networks}

\notes{
Neural networks are computational models inspired by biological neural systems. 
They consist of:
1. Input layers
2. Hidden layers
3. Output layers
}

\recommendation{
Start with simple architectures and gradually increase complexity as needed.
}

\notesfigure{\includediagram{neural-net}{80%}}
```

## Output Formats

- HTML documentation
- PDF documents
- LaTeX papers
- Word documents

## Best Practices

1. Use clear section hierarchy
2. Include detailed explanations
3. Add examples and figures
4. Cross-reference other sections
