---
id: "0010"
title: "File Access Is Confined To Allowed Roots"
status: "Proposed"
priority: "High"
created: "2026-10-08"
last_updated: "2026-10-08"
related_tenets: ["explicit-over-implicit", "configuration-lives-with-content"]
stakeholders: ["security team", "developers", "system administrators"]
tags: ["security", "filesystem", "path-traversal"]
---

# REQ-0010: File Access Is Confined To Allowed Roots

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

File I/O must stay within configured root directories. Paths must not escape those boundaries via path traversal or symlink abuse. The application must not be tricked into reading or writing outside its designated workspace.

**Why this matters**: Prevents unauthorized filesystem access. Aligns with **"Configuration Lives With Content"** by respecting workspace boundaries, and with **"Explicit Over Implicit"** by making allowed roots an explicit constraint.

**Who benefits**: Security teams, system administrators, all users.

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] File operations resolve paths to a definitive location before use
- [ ] Path traversal attempts (e.g. `../`) that leave allowed roots are rejected
- [ ] Symlinks that would escape allowed directories are rejected
- [ ] Environment-influenced path values cannot escape configured boundaries
- [ ] File operations fail safely when a path would leave allowed roots

## Notes (Optional)

Imported from Trent.AI security assessment (SR-5). Addresses vulnerability TA-5 (Path Traversal via Symlinks); related mitigation task MT-005.

## References

- **Related Tenets**: explicit-over-implicit, configuration-lives-with-content
- **External Links**: Trent.AI SR-5; TA-5; MT-005

## Progress Updates

### 2026-10-08
Imported from Trent.AI. Dates corrected; status set to Proposed pending CIP (HOW). Acceptance criteria kept outcome-focused.
