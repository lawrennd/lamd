# Bibliography Context

The bibliography context handles references, citations, and academic acknowledgments across different output formats.

## Key Macros

### References
```markdown
\references
    Creates references section
    No arguments

\cite{key}
    Cites a reference
    Args:
        key: BibTeX citation key

\citep{key}
    Parenthetical citation
    Args:
        key: BibTeX citation key
```

### Acknowledgments
```markdown
\thanks
    Creates acknowledgments section
    No arguments

\addguardian{title}{link}
    Adds Guardian article reference
    Args:
        title: Article title
        link: Article URL

\addblog{title}{link}
    Adds blog post reference
    Args:
        title: Post title
        link: Post URL
```

### Reading Materials
```markdown
\reading
    Creates further reading section
    No arguments

\addreading{reference}{section}
    Adds reading recommendation
    Args:
        reference: Reference to add
        section: Section identifier
```

## Example Usage

```markdown
\ifndef{deepLearningLecture}
\define{deepLearningLecture}

\section{Deep Learning}

As shown by \cite{Goodfellow-et-al-2016}, deep networks can...

\references

\thanks
\addblog{Neural Networks Explained}{2024/01/neural-networks}
\addguardian{AI Breakthrough}{ai/2024/breakthrough}

\reading
\addreading{Deep Learning Book}{Chapter 1}
\addreading{Neural Networks Review}{Introduction}

\endif
```

## Configuration

### BibTeX Setup
```latex
@book{Goodfellow-et-al-2016,
    title={Deep Learning},
    author={Ian Goodfellow and Yoshua Bengio and Aaron Courville},
    publisher={MIT Press},
    year={2016}
}
```

## Output Format Considerations

### LaTeX/PDF
- Full bibliography support
- Citation numbering
- BibTeX integration

### HTML
- Hyperlinked citations
- DOI integration
- Online reference linking

### Slides
- Simplified citations
- Reference slide generation
- Clickable links

## Best Practices

1. Citation Management
   - Use consistent keys
   - Maintain central BibTeX file
   - Check citation validity

2. Reference Organization
   - Group related references
   - Provide complete metadata
   - Include DOIs when available

3. Acknowledgments
   - Credit all contributors
   - Include funding sources
   - Mention institutional support
