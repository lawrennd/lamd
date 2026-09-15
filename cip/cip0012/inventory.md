# CIP-0012 Stage 0 — JavaScript inventory

Survey date: 2026-09-15  
Corpus: `snippets/`, `talks/`, `lamd/includes/`, `lamd/macros/`

## Classification legend

| Track | Meaning |
|-------|---------|
| **A** | Content scripts (multi-format HTML: slides, notes/posts, notebooks) |
| **B** | Reveal setup / slide backgrounds (slides only) |
| **Other** | Shared chrome unrelated to A/B API (MathJax, Mermaid, CIP-0007 frame controls, third-party widgets) |

## Track A — Content script loaders

Pattern: `_scripts/includes/*-js.md` with `\ifndef{…Js}` + `<script src="\scriptsDir/…">`. Scenario includes under `_physics/`, `_information/` pull these in. Format reach: wherever the parent include is expanded for HTML (slides-html, notes-html, ipynb HTML).

| Path | Scripts loaded | Notes |
|------|----------------|-------|
| `snippets/_scripts/includes/ballworld-js.md` | `ballworld/ballworld.js` | Shared runtime for Maxwell, Szilard, multiball, kappenball |
| `snippets/_scripts/includes/maxwell-js.md` | includes ballworld + `ballworld/maxwell.js` | |
| `snippets/_scripts/includes/szilard-js.md` | ballworld + szilard | |
| `snippets/_scripts/includes/multiball-js.md` | ballworld + multiball | |
| `snippets/_scripts/includes/kappenball-js.md` | ballworld + kappenball | |
| `snippets/_scripts/includes/dasher-js.md` | `dasher/dasher.js?v=22` | Cache-bust query |
| `snippets/_scripts/includes/dieroll-js.md` | `dieroll/dieroll.js` | |
| `snippets/_scripts/includes/jointentropy-js.md` | jointentropy | |
| `snippets/_scripts/includes/multigame-js.md` | multigame | |
| `snippets/_scripts/includes/observer-inside-js.md` / `observer-outside-js.md` | observer canvases | |
| `snippets/_scripts/includes/plotly-js.md` | CDN Plotly | External CDN, not `scriptsDir` |

Consumers (canvas markup + `\include{…-js.md}`): e.g. `_physics/includes/maxwells-demon*.md`, `entropy-billiards.md`, `dieroll.md`, `kappenball.md`, `_information/includes/dasher.md`.

**Other (not Track A API):** `snippets/_ai/includes/hype-about-hype.md` embeds Twitter `widgets.js` (third-party).

## Track B — Reveal backgrounds / setup

| Path | Pattern | Notes |
|------|---------|-------|
| `snippets/_privacy/includes/differential-privacy-with-cloaking.md` | `\newslide{…}{data-background="\writeDiagramsDir/pres_bg.png"}` | Static image BG |
| `snippets/_privacy/includes/differential-privacy-for-gps.md` | same | |
| `talks/_privacy/cloaking-functions.md` | includes privacy snippets | Talk entry |
| `lamd/macros/talk-macros-slides-html.gpp` `\includeplotly` | `data-background-iframe` + `data-background-interactive` | Reveal-only macro |

No inventoried uses of custom `slidesheader` beyond topic `_lamd.yml` → `slides-header.html`. No existing `slide_setup` / `--include-after-body` usage (gap CIP-0012 closes).

## Other — Shared header / animation / Mermaid

| Path | Role |
|------|------|
| `lamd/includes/slides-header.html` | MathJax 2.7.1 + `figure-animate.js` + `lamdSetDivs` / `lamdPlusDivs` (CIP-0007) |
| `lamd/macros/talk-macros-slides-html.gpp` `\startanimation` | Inline `DOMContentLoaded` init for frame groups |
| `lamd/templates/pandoc/pandoc-revealjs-template.revealjs` | Mermaid CDN + `Reveal.addEventListener('ready', …)` in `<head>` **before** Reveal loads (bug); `$include-after$` after `Reveal.initialize` (unwired) |

Topic `_lamd.yml` files set `slidesheader: slides-header.html` (talks `_ai`, `_information`, `_physics`, …).

## Format reach summary

| Mechanism | Slides HTML | Notes HTML | ipynb | TeX/PPTX/DOCX |
|-----------|-------------|------------|-------|---------------|
| Track A `_scripts/includes/*-js.md` | Yes | Yes (when included) | Yes (HTML cells) | No (script tags meaningless / stripped by macros) |
| Track B `data-background*` / `\includeplotly` | Yes | No | No | No |
| `slidesheader` / MathJax / figure-animate | Yes | N/A (postsheader separate) | N/A | N/A |

## Agreed fixture list → `tests/fixtures/cip0012/`

| Fixture | Maps from | Covers |
|---------|-----------|--------|
| `legacy-ballworld-js.md` | `snippets/_scripts/includes/ballworld-js.md` | Track A legacy once-guard + `scriptsDir` |
| `legacy-maxwell-js.md` | `snippets/_scripts/includes/maxwell-js.md` (slim: ballworld + maxwell script only) | Nested Track A loaders |
| `legacy-dasher-js.md` | `snippets/_scripts/includes/dasher-js.md` | Query-string script URL |
| `includescript-ballworld.md` | Migration twin of ballworld | Track A `\includescript` |
| `data-background-slide.md` | Privacy cloaking pattern | Track B `\newslide` + `data-background` |
| `includeplotly-bg.md` | `\includeplotly` macro use | Track B iframe background |
| `slide_setup_ambient.html` | New reference | Track B ambient + §B3 yield |

Header baseline: assert on live `lamd/includes/slides-header.html` (MathJax + figure-animate), not a fixture copy.
