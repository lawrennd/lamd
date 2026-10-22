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

\machinereviewlink
    Notes-only pointer (near the start of a lecture) to the machine-review
    section. HTML notes render it as a short aside; other notes formats use a
    blockquote. Empty on slides.

\machinereview
    Notes-only heading ``Machine Review`` (pandoc id ``machine-review``).
    Place at the end of the lecture, then include the review body under
    ``\ifdef{NOTES}`` so gpp does not dump it into slides. Empty on slides.
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

## Notes PDF templates (CIP-0013)

Frontmatter field `tex_template` selects the pandoc LaTeX template for `notespdf`:

| Value | Template | Use |
|-------|----------|-----|
| `notes` (default) | `pandoc-notes-tex-template.tex` | Lecture notes / long-form |
| `exercise` | `pandoc-exercise-tex-template.tex` | Worksheets / assignments |

Convenience: if `tex_template` is unset and `assignment: true`, the build uses `exercise`. Override with `tex_template: notes` when you need assignment macros but lecture-note chrome.

Exercise PDFs skip forced bibliography / bibtex so citation-free handouts build cleanly.

```yaml
assignment: True
notespdf: True
tex_template: exercise   # optional when assignment is true
```

## Best Practices

1. Use clear section hierarchy
2. Include detailed explanations
3. Add examples and figures
4. Cross-reference other sections
