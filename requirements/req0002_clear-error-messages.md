---
id: "0002"
title: "Processing Errors Are Clear and Actionable"
status: "In Progress"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: ["explicit-over-implicit", "academic-rigor-through-tooling"]
stakeholders: ["all users", "content authors", "debugging users"]
tags: ["error-handling", "validation", "usability"]
---

# REQ-0002: Processing Errors Are Clear and Actionable

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

When markdown processing fails, users should receive clear, actionable error messages that explain what went wrong and how to fix it. Errors should be caught early with meaningful context rather than propagating cryptic failures from underlying tools like gpp or pandoc. Users should be able to validate their content before processing to catch common mistakes.

Academic content creation involves complex pipelines with many dependencies (includes, diagrams, bibliographies, templates). When something breaks, users need to quickly identify and fix the problem without deep technical knowledge of the preprocessing system. Pre-processing validation should catch common mistakes before expensive processing steps.

**Why this matters**: This requirement implements **"Explicit Over Implicit"** by making processing pipelines transparent and debuggable. It supports **"Academic Rigor Through Tooling"** by ensuring users catch errors before they become publication problems.

**Who benefits**: All users processing markdown content, especially those debugging build failures, missing dependencies, or configuration errors.

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] File path errors identify which file is missing and where it was referenced
- [ ] Missing dependencies are detected before processing begins
- [ ] Error messages suggest specific fixes for common problems
- [ ] Invalid configuration is caught with clear explanations of what's wrong
- [ ] Processing failures include context about where in the pipeline they occurred
- [ ] Users can validate content without triggering full processing

## Notes (Optional)

This requirement currently has significant implementation through CIP-0005 Phases 1-3. Validation utilities exist and are being used. Additional work needed for dependency management (Phase 4) and comprehensive testing (Phase 5).

## References

- **Related Tenets**: explicit-over-implicit, academic-rigor-through-tooling
- **Related CIPs**: CIP-0005 (Improve mdpp Error Handling and Validation)
- **Related Files**: lamd/validation.py

## Progress Updates

### 2026-01-03
Requirement extracted from CIP-0005. Current status: In Progress. Phases 1-3 complete (basic validation, enhanced error handling, directory argument handling). Phases 4-5 (dependency management, testing) remain.

