---
id: "configuration-lives-with-content"
title: "Configuration Lives with Content"
status: "Active"
created: "2026-01-03"
last_reviewed: "2026-01-03"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- configuration
- portability
- metadata
---

# Tenet: Configuration Lives with Content

## Tenet

**Description**: Configuration and metadata should reside with the content (via YAML frontmatter) rather than in separate configuration files. This keeps content self-describing and portable. When a markdown file contains its own metadata - author, title, venue, formatting preferences - it can be shared, moved, or archived without losing essential context. This approach treats each document as a complete unit that knows what it needs, reducing dependencies on external configuration and making the system more maintainable. The build system extracts this frontmatter as the source of truth, ensuring consistency between what the author specifies and what gets rendered.

**Quote**: *"The document knows what it needs"*

**Examples**:
- Document frontmatter specifies title, author, venue, geometry, and other metadata
- The `mdfield` utility extracts configuration directly from markdown files
- Makefiles use frontmatter as the source of truth for build settings
- Moving a talk file to a different directory doesn't break its build configuration

**Counter-examples**:
- Storing document metadata in separate configuration files that must be kept in sync
- Hard-coding document properties in makefiles
- Requiring global configuration files that affect all documents
- Separating metadata from content in a way that requires both to be present for the document to work

**Conflicts**:
- **Project-Wide Defaults**: Some settings should apply to all documents in a project
- Resolution: Use `_lamd.yml` for project-wide defaults, but allow frontmatter to override
- **Configuration Complexity**: Putting all configuration in frontmatter can make headers verbose
- Resolution: Provide sensible defaults so most documents need minimal frontmatter

