---
id: "2026-10-26_cip0014-hosted-font-css"
title: "CIP-0014: Publish slide font CSS with relative hrefs"
status: "In Progress"
priority: "High"
created: "2026-10-26"
last_updated: "2026-10-26"
category: "bugs"
related_cips: ["0014"]
owner: "Neil Lawrence"
dependencies:
- "2026-10-13_cip0014-talkfontsize-flags"
tags:
- backlog
- bug
- cip0014
- revealjs
- slides
- css
- github-pages
---

# Task: CIP-0014 — publish slide font CSS with relative hrefs

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

`talkfontsize_css_args` passes absolute package paths to pandoc `--css`. Pandoc copies those strings into `<link href>`. On GitHub Pages the browser resolves them as site-root URLs such as `https://mlatcl.github.io/Users/neil/lawrennd/lamd/lamd/includes/slide-fontsize-xs.css`, which 404. Hosted decks then keep Reveal's default size (~42px) even when frontmatter sets `talkfontsize: xs`.

GPSS showed this live on 2026-10-26: `--lamd-fs-scale` unset, title `h1` 88px. After serving the CSS from `slides/` with relative hrefs, scale was 0.70 and body type 28px.

This is distinct from the optional jekyll-theme `talks.css` sync (`2026-10-13_cip0014-jekyll-theme-talks-css`). Package CSS remains the source of truth; it must ship next to the published HTML.

## Acceptance Criteria

- [x] `talkfontsize_css_args` emits basenames (`slide-fonts.css`, `slide-fontsize-{token}.css`), not package paths
- [x] `make-slides.mk` copies those files into the pandoc working directory and into `SLIDESDIR`
- [x] `tests/unit/test_flags.py` asserts the `--css` arguments contain no absolute path separators
- [ ] A rebuilt talk's HTML `href` loads on GitHub Pages (relative to the slides directory)

## Implementation Notes

Copy `slide-fonts.css` and `slide-fontsize-*.css` into the compile directory before pandoc so relative `--css` flags resolve locally, then copy the same files into `SLIDESDIR` next to `${OUT}.slides.html`.

Do not put absolute `/Users/...` paths in published HTML. Site-specific copies (GPSS `gh-pages` `a8dc818`) are a workaround until this lands in lamd.

## Related

- CIP: 0014
- Related task: `2026-10-13_cip0014-jekyll-theme-talks-css` (optional theme sync; not a substitute)
- GPSS workaround: `mlatcl/gpss` `a8dc818`

## Progress Updates

### 2026-10-26

Confirmed on https://mlatcl.github.io/gpss/slides/01-uncertainty-and-modelling.slides.html: font CSS 404, Reveal default size. Task created; generator fix on `fix/cip0014-hosted-font-css`.
