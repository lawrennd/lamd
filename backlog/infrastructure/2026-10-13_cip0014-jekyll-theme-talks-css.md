---
id: "2026-10-13_cip0014-jekyll-theme-talks-css"
title: "CIP-0014: Optional sync font-size rules into jekyll-theme talks.css"
status: "Proposed"
priority: "Low"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "infrastructure"
related_cips: ["0014"]
owner: "Neil Lawrence"
dependencies:
- "2026-10-13_cip0014-slide-fonts-css"
tags:
- backlog
- cip0014
- jekyll-theme
- css
- typography
---

# Task: CIP-0014 — sync font-size rules into jekyll-theme `talks.css`

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Optional follow-up: copy or link the same `--lamd-fs-*` / `.font-*` rules into `jekyll-theme/assets/css/talks.css` so site-served slides match local `maketalk` when the default remote `talkcss` is used without the package `--css` path being available.

## Acceptance Criteria

- [ ] jekyll-theme `talks.css` includes equivalent variables and `.font-*` rules (or clearly imports them)
- [ ] No regression to existing heading / `.scrollable` rules
- [ ] Documented that lamd package CSS remains source of truth for `maketalk`

## Implementation Notes

Separate repo (`jekyll-theme`). Only needed if hosted decks omit package CSS. Do not block CIP-0014 Close on this task.

## Related

- CIP: 0014
- Depends on: `2026-10-13_cip0014-slide-fonts-css`

## Progress Updates

### 2026-10-13

Task created (Proposed) when CIP-0014 Accepted; optional cross-repo follow-up.
