---
category: bugs
created: '2026-08-24'
dependencies: []
id: 2026-08-24_figure-magnify-notes-html
last_updated: '2026-08-24'
owner: Neil Lawrence
priority: High
related_cips: []
status: In Progress
title: Figure magnify pop-out flaky in lecture notes HTML
---

# Task: Make figure zoom reliable in notes/posts HTML (including mobile)

## Description

Lecture notes built via LaMD `posts` output (e.g. IEI `_lectures/*.html`) include magnify controls on figures and tables. Clicking the magnify icon should open a modal overlay with an enlarged figure and caption. Behaviour feels flaky, especially on tablet/mobile, and the affordance is easy to miss.

Zoom is **not implemented in lamd** alone: it requires the Jekyll theme layout, modal DOM, CSS, and JavaScript.

## Current architecture

| Layer | Location | Role |
|-------|----------|------|
| HTML markup | `lamd/macros/talk-macros-html.gpp` | `\figure`, `\table` wrap content; `.magnify` div calls `magnifyFigure(label)` |
| Notes HTML macros | `lamd/macros/talk-macros-notes-html.gpp` | Columns only; figures inherit from `talk-macros-html.gpp` |
| Modal + scripts | `jekyll-theme/_layouts/lecture.html` | `#modal-frame`, loads `figure-magnify.js` |
| JavaScript | `jekyll-theme/assets/js/figure-magnify.js` | Copies `#label-figure` innerHTML into modal |
| Styles | `jekyll-theme/_sass/_figure-box.scss` | Modal overlay, magnify button, mobile width rules |

Notes pages use `layout: lecture` in frontmatter; Jekyll wraps post content with the modal shell at build time. Raw `.posts.html.markdown` fragments alone will not zoom (no modal DOM).

## Issues found (2026-08-24)

### 1. Missing figure labels in source content

`\figure` requires three arguments (content, caption, label). A call with only two arguments produces `id="-figure"` and `magnifyFigure('')`, which cannot work.

Example: `snippets/_physics/includes/daniel-bernoulli-hydrodynamica.md` line 20 — second `\includegooglebook` figure has no label.

### 2. Table magnify ID mismatch

`\table` in `talk-macros-html.gpp` sets `id="label-table"`, but `magnifyFigure()` always reads `idstub + "-figure"`. **Table zoom is broken** even when labels are correct.

### 3. Tiny touch target

Magnify icon is `width:1.5ex` — difficult to tap on iPad/iPhone.

### 4. Modal stacking

`.modal { z-index: 1 }` may sit under fixed site navigation or other chrome.

### 5. JavaScript fragility

`figure-magnify.js` has no null checks; missing DOM nodes throw and break subsequent clicks. Cloning `innerHTML` from `<object>` SVG embeds may behave inconsistently in mobile Safari.

### 6. Jekyll Liquid in icon URL

Magnify button uses `{{ '/assets/images/Magnify_Large.svg' | relative_url }}`. This is correct for Jekyll-rendered lecture pages but appears literally in unprocessed build artefacts; authors previewing raw posts output may think zoom is broken.

## Acceptance Criteria

- [ ] Every `\figure` and `\table` in published lecture notes has a non-empty label (content audit + macro guard or auto-label)
- [ ] Table magnify opens the table frame (fix JS or align ID suffixes)
- [ ] Magnify control has a minimum 44×44px touch target on mobile
- [ ] Modal appears above site chrome (`z-index` sufficient)
- [ ] `magnifyFigure` fails gracefully when modal or target is missing (console warning, no uncaught exception)
- [ ] Manual verification on iPad Safari and desktop Chrome for IEI lecture pages
- [ ] Document in lamd docs: zoom requires Jekyll `lecture` layout + theme assets

## Implementation Notes

**lamd (this repo)**

- Consider validating non-empty `\figure`/`\table` labels at macro expansion time
- Improve magnify markup: `<button type="button">` with `aria-label="Enlarge figure"`, larger hit area
- Optional: embed a theme-independent icon path fallback for non-Jekyll previews

**jekyll-theme (separate repo)**

- Update `figure-magnify.js` to try `-figure` then `-table`; add null checks
- Raise modal `z-index`; add `@media` touch-target rules for `.magnify`
- Consider moving cloned content with `cloneNode(true)` instead of `innerHTML` for SVG objects

**snippets / content**

- Fix `daniel-bernoulli-hydrodynamica.md` missing third `\figure` argument
- Grep for other two-argument `\figure` calls

## Related

- Macro: `lamd/macros/talk-macros-html.gpp`
- Theme layout: `mlatcl/jekyll-theme/_layouts/lecture.html`
- IEI output: `iei/_lectures/*.html`, `iei/_lamd/*.posts.html.markdown`

## Progress Updates

### 2026-08-24

Investigation complete; root causes documented.

**Partial fixes applied:**

- lamd: table frames use `-figure` id for magnify lookup; larger touch-target magnify buttons (`talk-macros-html.gpp`)
- snippets: missing label on Bernoulli kinetic-theory `\figure` call
- jekyll-theme (separate repo): null checks in `figure-magnify.js`; modal `z-index: 1000`; button styling

**Still open:** content audit for other unlabelled figures; rebuild IEI lectures; manual iPad verification; formal docs.
