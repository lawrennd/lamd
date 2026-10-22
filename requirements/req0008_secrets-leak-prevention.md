---
id: "0008"
title: "Secrets Do Not Leak Through Logs Or Errors"
status: "Proposed"
priority: "High"
created: "2026-10-08"
last_updated: "2026-10-08"
related_tenets: ["explicit-over-implicit"]
stakeholders: ["security team", "developers", "operations team"]
tags: ["security", "logging", "error-handling"]
---

# REQ-0008: Secrets Do Not Leak Through Logs Or Errors

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

Exception tracebacks, application logs, and error messages must not expose plaintext credentials or other sensitive parameter values. Sensitive data must not appear in output that logging, monitoring, or debugging systems can capture.

**Why this matters**: Prevents accidental credential exposure through logs and errors. Aligns with **"Explicit Over Implicit"** by keeping sensitivity boundaries clear in every output channel.

**Who benefits**: Security teams, operations teams, developers reviewing logs.

## Acceptance Criteria

What does "done" look like? Be specific about outcomes, not implementation:

- [ ] Exception output does not contain plaintext credentials or sensitive values
- [ ] Application logs do not contain plaintext credentials or API keys
- [ ] User-facing error messages do not contain sensitive data
- [ ] Stack traces written to logs are free of plaintext secrets
- [ ] Debugging output does not expose plaintext secrets

## Notes (Optional)

Imported from Trent.AI security assessment (SR-3). Addresses vulnerability TA-4 (Credential Leakage via Exception Tracebacks); related mitigation task MT-004.

## References

- **Related Tenets**: explicit-over-implicit
- **External Links**: Trent.AI SR-3; TA-4; MT-004

## Progress Updates

### 2026-10-08
Imported from Trent.AI. Dates corrected; status set to Proposed pending CIP (HOW). Wording aligned with outcome-focused acceptance criteria.
