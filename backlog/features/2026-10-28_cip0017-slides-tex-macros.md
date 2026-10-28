---
id: "2026-10-28_cip0017-slides-tex-macros"
title: "Slides-tex macros for Beamer frames and non-float figures"
status: "Completed"
priority: "High"
created: "2026-10-28"
last_updated: "2026-10-28"
category: "features"
related_cips: ["0017"]
owner: "Neil D. Lawrence"
dependencies: []
tags:
- backlog
- cip0017
- gpp
- beamer
- slides
---

# Task: Slides-tex macros for Beamer

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Override `\newslide` / `\section` in `talk-macros-slides-tex.gpp` so they emit markdown `## title` without Reveal attributes. Redefine `\figure` as a centred non-float for Beamer frames.

## Acceptance Criteria

- [ ] `\newslide{Title}{.scrollable}` does not keep `.scrollable` in the heading
- [ ] `\figure` in slides-tex does not emit a floating `figure` environment
- [ ] Animation stubs (`\startanimation`, `\newframe`, `\endanimation`) remain no-ops / content-only

## Implementation Notes

See CIP-0017 Detailed Description. Keep the existing `\newslide` one-argument form working via GPP's optional second argument.

## Related

- CIP: 0017

## Progress Updates

### 2026-10-28

Task created after CIP-0017 was accepted.
