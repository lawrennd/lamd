---
id: "2026-02-03_lamd-cli-tests"
title: "Phase 1: Tests for two-stage `lamd` CLI (talk/cv)"
status: "Proposed"
priority: "Medium"
created: "2026-02-03"
last_updated: "2026-02-03"
category: "features"
related_cips: ["0006"]
owner: "Neil Lawrence"
dependencies:
- "2026-02-03_lamd-talk-subcommand"
- "2026-02-03_lamd-cv-subcommand"
tags:
- tests
- cli
- interface
- compatibility
---

# Task: Tests for two-stage `lamd` CLI (talk/cv)

## Description

Add unit and integration tests for:

- interface generation (schema + determinism)
- interface execution (smoke tests)
- backward compatibility (legacy commands remain functional)

## Acceptance Criteria

- [ ] Unit tests cover interface schema generation and parsing
- [ ] Integration tests cover generate → execute for talk and cv flows
- [ ] Backward compatibility tests ensure `maketalk` and `makecv` remain unchanged
- [ ] Tests run in CI/local without relying on external network resources

## Related

- CIP: 0006

## Progress Updates

### 2026-02-03

Task created to decompose CIP-0006 Phase 1 into concrete DO-work.

