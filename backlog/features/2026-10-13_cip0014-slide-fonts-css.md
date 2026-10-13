---
id: "2026-10-13_cip0014-slide-fonts-css"
title: "CIP-0014: Ship slide-fonts.css five-step scale"
status: "Ready"
priority: "High"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "features"
related_cips: ["0014"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- cip0014
- revealjs
- slides
- css
- typography
---

# Task: CIP-0014 — `slide-fonts.css` five-step scale

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Add a lamd-packaged stylesheet that defines the Reveal font-size scale via CSS custom properties and per-slide `.font-*` section classes. Rules must be additive (do not fork full `talks.css`).

## Acceptance Criteria

- [ ] `lamd/includes/slide-fonts.css` (or agreed package path) exists
- [ ] `:root` defines `--lamd-fs-base`, `--lamd-fs-scale`, and `xs`/`sm`/`md`/`lg`/`xl` step variables
- [ ] `.reveal` uses `calc(var(--lamd-fs-base) * var(--lamd-fs-scale))`
- [ ] `.reveal .slides section.font-{xs,sm,md,lg,xl}` scale relative to the deck base
- [ ] Default (no overrides) leaves visual size unchanged vs current Reveal + `talks.css`
- [ ] Unit or snapshot check asserts required variable and class names are present

## Implementation Notes

See CIP-0014 Detailed Description (size scale table and CSS sketch). Prefer package CSS so `maketalk` does not depend on updating external inverseprobability / jekyll-theme `talks.css`.

## Related

- CIP: 0014

## Progress Updates

### 2026-10-13

Task created (Ready) when CIP-0014 Accepted.
