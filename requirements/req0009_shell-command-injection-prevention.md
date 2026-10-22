---
id: "0009"
title: "Shell Commands Are Safe From Injection"
status: "Proposed"
priority: "High"
created: "2026-10-08"
last_updated: "2026-10-08"
related_tenets: ["explicit-over-implicit", "academic-rigor-through-tooling"]
stakeholders: ["security team", "developers"]
tags: ["security", "input-validation", "command-injection"]
---

# REQ-0009: Shell Commands Are Safe From Injection

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

User-controlled input that influences shell command construction — including markdown metadata and file paths — must not allow arbitrary command execution. External input used when invoking external tools must be safe: rejected, escaped, or otherwise prevented from injecting commands.

**Why this matters**: Prevents arbitrary command execution through malicious input. Supports **"Academic Rigor Through Tooling"** by keeping the build toolchain trustworthy, and **"Explicit Over Implicit"** by treating untrusted input as an explicit boundary.

**Who benefits**: All users, security teams, system administrators.

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] User-controlled input cannot inject arbitrary shell commands
- [ ] Shell metacharacters in untrusted input do not alter command structure
- [ ] File paths used in commands cannot escape intended path semantics
- [ ] Repository and workspace paths cannot inject commands when passed to tools
- [ ] Command construction does not rely on unsanitized string interpolation of untrusted input

## Notes (Optional)

Imported from Trent.AI security assessment (SR-4). Addresses vulnerabilities TA-3 (Shell Injection via Unsanitized GPP Metadata) and TA-8 (Command Injection via Git Paths); related mitigation task MT-002.

Known attack surfaces for a future CIP: gpp metadata, git repository paths, and other shell-invoking build steps.

## References

- **Related Tenets**: explicit-over-implicit, academic-rigor-through-tooling
- **External Links**: Trent.AI SR-4; TA-3, TA-8; MT-002

## Progress Updates

### 2026-10-08
Imported from Trent.AI. Dates corrected; status set to Proposed pending CIP (HOW). Description generalized from gpp-specific wording; attack surfaces retained in Notes.
