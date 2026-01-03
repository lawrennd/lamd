---
id: "0001"
title: "CLI Utilities Are Discoverable and Self-Documenting"
status: "In Progress"
priority: "High"
created: "2026-01-03"
last_updated: "2026-01-03"
related_tenets: ["explicit-over-implicit", "academic-rigor-through-tooling"]
stakeholders: ["new users", "documentation writers", "CLI users"]
tags: ["usability", "documentation", "cli"]
---

# REQ-0001: CLI Utilities Are Discoverable and Self-Documenting

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

Users should be able to discover and understand lamd's command-line utilities without needing to consult external documentation. Each utility should clearly explain its purpose, options, and common usage patterns through built-in help text. When users encounter errors or uncertainty, the tools themselves should provide sufficient guidance to resolve issues.

This requirement supports academic workflows where users may be working on different machines, offline, or in environments where web documentation isn't readily accessible. Self-documenting tools reduce friction and allow users to focus on content creation rather than tool configuration.

**Why this matters**: This requirement is informed by the **"Explicit Over Implicit"** tenet - users should understand how to use tools without hidden knowledge. It also supports **"Academic Rigor Through Tooling"** by making proper tool usage accessible to all users, not just experts.

**Who benefits**: New users discovering lamd, experienced users working with unfamiliar utilities, documentation writers creating tutorials, and anyone troubleshooting issues.

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] Running any lamd utility with `--help` provides clear, comprehensive usage information
- [ ] Help text includes practical examples for common use cases
- [ ] Error messages explain what went wrong and suggest potential fixes
- [ ] Users can discover how utilities integrate with each other through help text
- [ ] Command-line options are documented with clear descriptions of their effects
- [ ] Troubleshooting guidance is available through the command-line interface

## Notes (Optional)

This requirement currently has partial implementation through CIP-0001. Some utilities have good help text while others need improvement. The requirement will be considered "Implemented" when all utilities meet the acceptance criteria.

## References

- **Related Tenets**: explicit-over-implicit, academic-rigor-through-tooling
- **Related CIPs**: CIP-0001 (lamd Command Line Utilities Documentation Improvements)
- **Backlog**: 2025-05-16_improve-cli-help

## Progress Updates

### 2026-01-03
Requirement extracted from CIP-0001. Current status: In Progress. Some utilities (makecv, mdpeople) have improved help text and documentation. Remaining utilities need similar improvements.

