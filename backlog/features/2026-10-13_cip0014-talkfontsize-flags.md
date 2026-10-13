---
id: "2026-10-13_cip0014-talkfontsize-flags"
title: "CIP-0014: talkfontsize frontmatter in flags.py"
status: "Ready"
priority: "High"
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
- frontmatter
- typography
---

# Task: CIP-0014 — `talkfontsize` in `flags.py`

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Wire frontmatter `talkfontsize` through `flags.py` for reveal output: normalise aliases to short tokens, reject unknown tokens with a clear message, attach package `slide-fonts.css` via `--css`, and inject `--lamd-fs-scale` (header `<style>` or equivalent pandoc variable).

## Acceptance Criteria

- [ ] Unset `talkfontsize` defaults to `medium` (scale `1.00`) — no visual change
- [ ] Aliases resolve: `smaller`/`x-small`→`xs`, `small`→`sm`, `medium`/`normal`→`md`, `large`→`lg`, `larger`/`x-large`→`xl`
- [ ] Unknown token fails with an error listing allowed names
- [ ] Reveal flag line includes package font CSS (repeatable alongside custom `talkcss`)
- [ ] Build injects the correct `--lamd-fs-scale` for the chosen token
- [ ] `tests/unit/test_flags.py` covers default, aliases, custom `talkcss` coexistence, and invalid token

## Implementation Notes

Mirror existing `talktheme` / `talkcss` handling in `lamd/flags.py` (`output == "reveal"`). Custom `talkcss` must still apply; document that overrides should prefer CSS variables.

## Related

- CIP: 0014
- Depends on: `2026-10-13_cip0014-slide-fonts-css`

## Progress Updates

### 2026-10-13

Task created (Ready) when CIP-0014 Accepted.
