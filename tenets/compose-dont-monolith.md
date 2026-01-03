---
id: "compose-dont-monolith"
title: "Compose, Don't Monolith"
status: "Active"
created: "2026-01-03"
last_reviewed: "2026-01-03"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- architecture
- modularity
- composition
---

# Tenet: Compose, Don't Monolith

## Tenet

**Description**: Favor modular, composable components over monolithic solutions. Each utility should do one thing well and integrate cleanly with others. This Unix philosophy approach creates a system that is easier to understand, test, and extend. Rather than building one massive tool that does everything, lamd provides focused utilities that can be combined in different ways. Need to extract a field from markdown? Use `mdfield`. Need to generate lists? Use `mdlist`. Need to build a talk? Use `maketalk`. This modularity allows users to understand and use just the parts they need, and makes it possible to integrate lamd tools into larger workflows.

**Quote**: *"Build systems from parts, not parts from systems"*

**Examples**:
- Separate utilities with focused responsibilities: `mdfield`, `mdlist`, `mdpeople`, `maketalk`, `makecv`
- Modular makefiles for different document types that can be included as needed
- Two-stage CLI design (interface generation + execution) in CIP-0006 separates configuration from computation
- Integration with external workflow systems like lynguine rather than reimplementing workflow logic
- Each utility can be used independently or as part of a larger pipeline

**Counter-examples**:
- Creating a single monolithic command that tries to handle all document types and operations
- Tightly coupling utilities so they can't be used independently
- Reimplementing functionality that already exists in other tools
- Building features that can't be composed with other parts of the system
- Creating utilities with multiple unrelated responsibilities

**Conflicts**:
- **Convenience vs. Modularity**: Sometimes a monolithic tool is more convenient for users
- Resolution: Provide convenience wrappers (like `maketalk`) that compose modular parts but don't prevent direct access to those parts
- **Learning Curve**: More tools means more to learn
- Resolution: Design each tool with clear, consistent interfaces and good documentation

