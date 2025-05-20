# Creating Effective Snippets

## Snippet Design Principles

1. Single Responsibility
   - Each snippet should cover one concept
   - Clear, focused purpose
   - Minimal dependencies

2. Self-Contained
   - Include necessary setup
   - Document dependencies
   - Handle edge cases

3. Reusable
   - Parameterize where appropriate
   - Avoid hard-coding
   - Consider different contexts

## Example Snippet Template
```markdown
\ifndef{conceptName}
\define{conceptName}

\editme

\section{Concept Title}

\notes{
Detailed explanation of the concept...
}

\slides{
* Key point 1
* Key point 2
* Key point 3
}

\figure{\includediagram{concept-diagram}{80%}}
{Concept visualization}{fig:concept}

\endif
```

## Snippet Organization

1. Directory Structure
```
_topic/
  └── includes/
      ├── concept1.md
      ├── concept2.md
      └── README.md
```

2. Naming Conventions
   - Use kebab-case for files
   - Clear, descriptive names
   - Include version if needed

3. Documentation
   - README for each directory
   - Usage examples
   - Dependency list

## Testing Snippets

1. Isolated Testing
```bash
lamd test snippet.md --format all
```

2. Integration Testing
```bash
lamd build lecture.md --verify-snippets
```
