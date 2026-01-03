---
id: "0004"
title: "Animations Work Consistently and Accessibly Across Formats"
status: "Proposed"
priority: "Medium"
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: ["single-source-multiple-contexts", "academic-rigor-through-tooling"]
stakeholders: ["presentation authors", "accessibility users", "students", "educators"]
tags: ["animations", "accessibility", "cross-format", "presentations"]
---

# REQ-0004: Animations Work Consistently and Accessibly Across Formats

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

When authors create animated content, it should work reliably across all output formats with predictable behavior. Interactive animations in HTML slides should be accessible to users with disabilities, with proper keyboard navigation and screen reader support. In formats that don't support interactivity (notes, PDFs), animations should degrade gracefully to show all frames or provide alternative navigation.

Academic presentations often include animated visualizations, progressive reveals, and step-by-step explanations. These animations must work consistently whether presenting live, sharing slides online, or distributing as notes. Accessibility is particularly important in educational contexts where content must be available to all students regardless of ability.

**Why this matters**: This requirement implements **"Single Source, Multiple Contexts"** by ensuring animated content works appropriately in each output format. It supports **"Academic Rigor Through Tooling"** by ensuring accessibility standards are met automatically rather than requiring authors to create format-specific content.

**Who benefits**: Presentation authors using animations, students and educators requiring accessible content, users of assistive technologies, and anyone viewing content in different formats.

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] Animation macros produce correct output in all supported formats (HTML, notes, PDF, IPynb)
- [ ] Interactive animation controls in HTML have keyboard navigation support
- [ ] Animation controls include proper ARIA labels for screen readers
- [ ] Non-interactive formats show all animation frames or provide alternatives
- [ ] Animation syntax produces consistent, predictable behavior without duplicate definitions
- [ ] Missing JavaScript dependencies degrade gracefully with fallback behavior

## Notes (Optional)

This requirement addresses issues documented in CIP-0007. Current animation macros have bugs (duplicate definitions, missing endanimation) and accessibility problems. Format support is inconsistent.

## References

- **Related Tenets**: single-source-multiple-contexts, academic-rigor-through-tooling
- **Related CIPs**: CIP-0007 (Animation System Improvements)
- **Standards**: WCAG accessibility guidelines for interactive controls

## Progress Updates

### 2026-01-03
Requirement extracted from CIP-0007. Current status: Proposed. Animation system has known bugs and accessibility issues that need addressing.

