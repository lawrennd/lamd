# Quick Start Guide

## Creating Your First Document

1. Create a new markdown file `lecture.md`:
```markdown
---
title: "Introduction to Machine Learning"
author: Your Name
date: 2024-01-01
---

\ifndef{introML}
\define{introML}

\section{Machine Learning Basics}

\notes{
Machine learning is a field of computer science that gives computers the ability to learn without being explicitly programmed.
}

\slides{
* ML enables computers to learn
* Learning from data
* Improving with experience
}

\endif
```

2. Build different formats:
```bash
# Create slides
lamd build lecture.md --format slides

# Create notes
lamd build lecture.md --format notes

# Create PDF
lamd build lecture.md --format pdf
```

## Creating Reusable Snippets

1. Create a snippet file `_ml/includes/neural-networks.md`:
```markdown
\ifndef{neuralNetworks}
\define{neuralNetworks}

\section{Neural Networks}

\notes{
Neural networks are computational models inspired by biological neural systems.
}

\slides{
* Inspired by biology
* Multiple layers
* Deep learning foundation
}

\endif
```

2. Include in your lecture:
```markdown
\include{_ml/includes/neural-networks.md}
```

## Adding Media

```markdown
\figure{\includediagram{neural-net}{80%}}
{Basic neural network architecture}{fig:neural-net}

\includeyoutube{video-id}{800}{600}
```

## Next Steps

1. Explore different contexts (slides, notes, etc.)
2. Learn about media handling
3. Understand layout controls
4. Master bibliography management
