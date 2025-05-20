# Definition Context

The definition context handles content organization, reuse, and inclusion. It's fundamental to LAMD's modular approach to content creation.

## Key Macros

### Content Definition
```markdown
\ifndef{name}
    Prevents multiple inclusion of content
    Args:
        name: Unique identifier for content block

\define{name}
    Defines a named content block
    Args:
        name: Must match corresponding ifndef

\endif
    Ends a definition block
    No arguments
```

### Content Inclusion
```markdown
\include{filepath}
    Includes content from another file
    Args:
        filepath: Path to file to include

\input{filename}
    Direct content inclusion
    Args:
        filename: File to input directly
```

### Source Management
```markdown
\editme
    Adds source file edit link
    No arguments but requires repository configuration

\jekyllinclude{filename}
    Jekyll-specific inclusion
    Args:
        filename: Jekyll include file
```

## Example Usage

```markdown
% In _ml/includes/neural-networks.md
\ifndef{neuralNetworks}
\define{neuralNetworks}

\editme

\section{Neural Networks}
... content ...

\endif

% In main lecture file
\include{_ml/includes/neural-networks.md}
\include{_ml/includes/backpropagation.md}
```

## Directory Structure
```
lectures/
  ├── _ml/
  │   └── includes/
  │       ├── neural-networks.md
  │       └── backpropagation.md
  ├── _physics/
  │   └── includes/
  └── _math/
      └── includes/
```

## Best Practices

1. Use Clear Naming
   - Choose descriptive snippet names
   - Use consistent naming conventions
   - Avoid name collisions

2. Organization
   - Group related content
   - Maintain clear directory structure
   - Document dependencies

3. Reusability
   - Keep snippets focused
   - Minimize dependencies
   - Document requirements

4. Version Control
   - Track all snippet files
   - Maintain change history
   - Document major changes

5. Documentation
   - Comment complex snippets
   - Provide usage examples
   - Document prerequisites
