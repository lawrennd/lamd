---
id: "academic-rigor-through-tooling"
title: "Academic Rigor Through Tooling"
status: "Active"
created: "2026-01-03"
last_reviewed: "2026-01-03"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- academic
- quality
- reproducibility
---

# Tenet: Academic Rigor Through Tooling

## Tenet

**Description**: The system should enable academic best practices (reproducibility, proper citations, code testing) while remaining flexible enough to support diverse academic workflows. Academic work requires rigor - accurate citations, reproducible code, consistent author attribution, and traceable dependencies. Rather than constraining users with rigid requirements, lamd provides tools that make rigorous practices easy and natural. Code can be extracted and tested to ensure it runs. Bibliography management ensures proper attribution. Dependency tracking makes it clear which diagrams and includes are used. This approach supports scholarship without becoming prescriptive about how scholars work.

**Quote**: *"Support scholarship, don't constrain it"*

**Examples**:
- `--code test` flag enables code extraction and validation to ensure examples actually work
- Bibliography management with CSL support for proper academic citations
- People macros ensure consistent representation of authors and collaborators across documents
- Dependency tracking for diagrams and includes makes content reproducible
- Frontmatter validation catches metadata errors before they become publication problems

**Counter-examples**:
- Forcing all users to follow a single citation style regardless of field conventions
- Allowing broken code examples to be published without validation
- Inconsistent author attribution across related documents
- Missing dependencies that make content non-reproducible
- Ignoring field-specific academic conventions

**Conflicts**:
- **Flexibility vs. Enforcement**: Some users want strict validation, others want freedom
- Resolution: Provide validation tools that can be run on demand but don't block workflow
- **Different Academic Fields**: Citation and formatting conventions vary across disciplines
- Resolution: Support multiple styles and conventions, make switching between them easy

