---
id: "single-source-multiple-contexts"
title: "Single Source, Multiple Contexts"
status: "Active"
created: "2026-01-03"
last_reviewed: "2026-01-03"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- content
- reuse
- formats
---

# Tenet: Single Source, Multiple Contexts

## Tenet

**Description**: Content should be authored once and rendered appropriately for different contexts (slides, notes, papers, web). The lamd system prioritizes content reuse while respecting the unique requirements of each output format. This principle recognizes that academic content often needs to be presented in multiple ways - as conference talks, detailed notes, journal papers, or web content - without requiring authors to maintain separate versions of the same material. By enabling selective rendering through context-aware macros, we reduce duplication, maintain consistency, and allow authors to focus on content rather than format management.

**Quote**: *"Write once, present everywhere"*

**Examples**:
- Using `\slides{}` and `\notes{}` macros to render content selectively based on output format
- Generating HTML slides, PDF notes, and PPTX presentations from the same markdown source
- Macro system allows conditional content inclusion based on context (e.g., detailed explanations in notes, concise bullets in slides)
- A single talk file can produce both a quick presentation and comprehensive documentation

**Counter-examples**:
- Maintaining separate markdown files for slides and notes versions of the same content
- Copy-pasting content between different format files
- Hard-coding format-specific content without using context macros
- Creating format-specific files that duplicate shared content

**Conflicts**:
- **Format-Specific Optimization**: Sometimes a format requires unique content that doesn't fit the single-source model
- Resolution: Use context macros to include format-specific content when necessary, but default to shared content
- **Complexity vs. Simplicity**: Context-aware macros add complexity to the authoring experience
- Resolution: Provide simple defaults that work well without context awareness, but enable power users to leverage full context features

