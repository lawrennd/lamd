---
id: "0006"
title: "Secrets Are Confidential At Rest"
status: "Proposed"
priority: "High"
created: "2026-10-08"
last_updated: "2026-10-08"
related_tenets: ["explicit-over-implicit", "academic-rigor-through-tooling"]
stakeholders: ["security team", "developers", "system administrators"]
tags: ["security", "cryptography", "credentials"]
---

# REQ-0006: Secrets Are Confidential At Rest

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

API keys, OAuth tokens, database passwords, and similar credentials must remain confidential when stored. An attacker who obtains the credential store files must not be able to recover plaintext secrets without the master key. Master key derivation must resist offline dictionary attacks.

This requirement makes the confidentiality boundary explicit: secrets are protected at rest, and plaintext exists only transiently in memory during authorized retrieval.

**Why this matters**: Protects sensitive credentials if storage is breached. Aligns with **"Explicit Over Implicit"** by making security boundaries clear, and with **"Academic Rigor Through Tooling"** by ensuring credential handling meets scholarly and operational trust expectations.

**Who benefits**: All users storing credentials, system administrators, security auditors.

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] Credentials in the store are unreadable without the master key
- [ ] Master key derivation resists offline dictionary attacks (sufficient entropy and work factor)
- [ ] Salt values are unique per credential and cryptographically random
- [ ] Credentials are only available in plaintext in memory during authorized retrieval
- [ ] No plaintext credentials are written to disk outside the protected store

## Notes (Optional)

Imported from Trent.AI security assessment (SR-1). Addresses vulnerability TA-1 (Weak Credential Encryption); related mitigation task MT-003.

Hard constraints from the assessment (implementation guidance for a future CIP, not acceptance criteria themselves): industry-standard encryption at rest (e.g. AES-256 or equivalent); key derivation via PBKDF2, Argon2, or equivalent with sufficient iterations (e.g. ≥100,000 for PBKDF2).

## References

- **Related Tenets**: explicit-over-implicit, academic-rigor-through-tooling
- **External Links**: Trent.AI SR-1; TA-1; MT-003

## Progress Updates

### 2026-10-08
Imported from Trent.AI. Dates corrected; status set to Proposed pending CIP (HOW). Acceptance criteria revised toward outcomes; algorithm specifics moved to Notes.
