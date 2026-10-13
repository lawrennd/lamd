---
id: "2026-10-13_cip0014-slidefont-macros"
title: "CIP-0014: Optional slidefont helper and subsection attrs"
status: "Ready"
priority: "Medium"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "features"
related_cips: ["0014"]
owner: "Neil Lawrence"
dependencies:
- "2026-10-13_cip0014-slide-fonts-css"
tags:
- backlog
- cip0014
- revealjs
- slides
- macros
- typography
---

# Task: CIP-0014 — `\slidefont` helper + subsection attrs decision

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Confirm that `\newslide{…}{.font-sm}` and `\section{…}{.font-sm}` work via the existing attrs channel. Optionally add `\slidefont{size}` emitting `.font-<size>`. Record the CIP choice for `\subsection`: **A** leave unchanged (v1), or **B** add a second attrs argument like `\newslide` / `\section`.

## Acceptance Criteria

- [ ] Documented / verified: `{.font-sm}` (and siblings) on `\newslide` / `\section` reach Reveal `<section>` classes
- [ ] Optional `\slidefont{size}` defined in `talk-macros-slides.gpp` if kept
- [ ] Subsection attrs decision (A or B) recorded in CIP-0014 Implementation Status
- [ ] If B chosen: `\subsection{text}{commands}` implemented and tested; if A: docs state size classes apply to `\newslide` / `\section` only
- [ ] No new primary constructors such as `\newslidesmall{…}`

## Implementation Notes

CIP-0014 recommends option A for v1 unless authors clearly need subsection attrs. Helpers should emit attrs, not proliferate slide macros.

## Related

- CIP: 0014
- Depends on: `2026-10-13_cip0014-slide-fonts-css`

## Progress Updates

### 2026-10-13

Task created (Ready) when CIP-0014 Accepted.
