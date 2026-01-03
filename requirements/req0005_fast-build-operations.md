---
id: "0005"
title: "Build Operations Complete in Reasonable Time"
status: "Proposed"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: ["compose-dont-monolith", "academic-rigor-through-tooling"]
stakeholders: ["content authors", "CI/CD users", "developers"]
tags: ["performance", "user-experience", "workflow"]
---

# REQ-0005: Build Operations Complete in Reasonable Time

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

When users build content (CVs, talks, documents), the build process should complete in reasonable time without unnecessary waiting. Users should not experience significant delays from tool overhead that dominates the actual content processing work. Build times should be proportional to the complexity and size of the content, not dominated by infrastructure startup costs.

Academic content creation involves iterative workflows - make a change, rebuild, review, repeat. When build times are slow due to tool overhead rather than actual work, this feedback loop breaks down. Users lose focus, productivity suffers, and the tools become frustrating rather than helpful. Fast builds enable better workflows and more productive content creation.

**Why this matters**: This requirement is informed by **"Academic Rigor Through Tooling"** - tools should support scholarship without adding unnecessary friction. It's also informed by **"Compose, Don't Monolith"** - the solution should leverage external services and tools efficiently rather than building complex caching into lamd itself.

**Who benefits**: Content authors who build CVs and talks frequently, developers working on content, CI/CD systems that build multiple documents, and anyone in an iterative edit-build-review cycle.

## Current Situation

**CV builds** currently take ~72 seconds, with:
- 38 subprocess calls to lynguine (27 `mdfield` + 11 `mdlist`)
- Each call: ~1.9s startup overhead (Python + pandas + lynguine imports)
- Actual work: ~5 seconds
- **Startup overhead: 93% of total time**

This makes the build process feel sluggish and breaks the iterative workflow. Most of the time is spent waiting for tools to start up rather than doing actual work.

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] CV builds complete in under 10 seconds for typical documents
- [ ] Build time is dominated by actual work (content processing) not tool overhead
- [ ] Repeated builds (common in iterative workflows) are fast
- [ ] Build performance is predictable and consistent
- [ ] Users can iterate quickly through edit-build-review cycles
- [ ] CI/CD systems can build multiple documents efficiently

## Notes (Optional)

This requirement focuses on the outcome (fast builds) without prescribing the implementation. Solutions could include:
- Using persistent services to amortize startup costs
- Caching frequently accessed data
- Optimizing subprocess calls
- Using different communication patterns

The key is that **builds should be fast**, not that they use any specific technical approach.

## References

- **Related Tenets**: 
  - `compose-dont-monolith`: Solution should leverage external services efficiently
  - `academic-rigor-through-tooling`: Tools should enable productivity, not hinder it
- **Related Projects**: 
  - lynguine REQ-0007 (Fast Repeated Access) addresses similar performance needs
  - lynguine CIP-0008 (Server Mode) provides a potential solution approach
- **Current State**:
  - CV builds: ~72s total, ~5s actual work, ~67s overhead
  - Profiling shows 1.9s startup per subprocess call

## Progress Updates

### 2026-01-03
Requirement created based on profiling of lamd CV builds. Current performance makes iterative workflows frustrating. Related work in lynguine (server mode) may provide a solution approach.

