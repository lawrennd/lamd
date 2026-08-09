---
author: Neil Lawrence
created: "2026-08-09"
id: "000F"
last_updated: "2026-08-09"
status: Proposed
compressed: false
related_requirements: ["0002", "0004"]
related_cips: ["0005", "0007", "000E"]
tags:
- cip
- validation
- build-output
- animations
- explicit-over-implicit
title: Build Output Validation
---

# CIP-000F: Build Output Validation

## Status

- [x] Proposed — initial design document; **Phase 0 scoping not yet started**
- [ ] Accepted — **blocked until Phase 0 inventory is complete and reviewed**
- [ ] In Progress
- [ ] Implemented
- [ ] Closed

## Summary

lamd validates much of its **input** pipeline (paths, includes, frontmatter) but does not systematically check **built outputs** for integrity problems that survive a successful `make`. A concrete failure mode — duplicate animation group names across included snippets producing duplicate DOM ids and blank slides — motivated this CIP.

This plan establishes **Phase 0: scoping and inventory** as a mandatory design stage before any implementation is accepted. Phase 0 decides *what* to validate, *when* in the pipeline to validate it, and *how* errors should surface. Implementation follows only after that inventory is agreed.

**Requirements addressed:** REQ-0002 (clear, actionable errors; validate without full re-debugging), REQ-0004 (predictable, accessible animations).

**Related work:** CIP-0005 (input/mdpp validation), CIP-0007 (animation macro behaviour and runtime fallbacks), CIP-000E (first-use robustness — may share a `lamd check`-style surface but different failure domain).

## Motivation

### Triggering incident (August 2026)

The talk `basis-functions-and-generalisation` includes two snippets that both used animation group `olympic_LM_polynomial_number`:

| Slide | Snippet | Frames |
|-------|---------|--------|
| Polynomial Fits to Olympic Data | `olympic-marathon-all-polynomial.md` | 29 |
| Polynomial Fits to Olympics Data | `olympic-marathon-validation-fit.md` | 28 |

The build completed without error. In the generated HTML, both slides emitted `id="animation-olympic_LM_polynomial_number"`, duplicate range inputs, and frame classes with the same name. `figure-animate.js` uses global DOM queries; on the second slide the visible frame belonged to the hidden first slide → **blank animation**.

**Content fix:** rename the validation-fit group to `olympic_LM_polynomial_number_val` in the snippet.

**System gap:** nothing in the build pipeline flagged the collision. The author discovered it only by visual inspection in the browser.

### Related incident: outer fold slider range (August 2026)

The same talk’s leave-one-out and $k$-fold cross-validation slides nest animations: an outer **fold** slider and an inner **num basis** slider per fold. Both snippets declared `\startanimation{...}{0}{1}{fold}` while emitting **six** outer `\newframe` blocks (folds `000`–`005` and `00`–`05` respectively). LaMD maps `{start}{finish}` directly to the HTML range input `min`/`max`, so the fold slider had only two positions and could not reach folds 2–5 even though those frames existed in the DOM. Inner sliders worked because their `{1}{11}` range matched their frame count.

**Content fix:** set outer `\startanimation` finish to `5` in `olympic-marathon-loo-validation.md` and `olympic-marathon-k-fold-validation.md`.

**System gap:** inventory item **OUT-ANIM-FRAME-RANGE** (animation frame count mismatch) — the build succeeded; the defect is only visible when using the slider.

### Why this is not covered by existing CIPs

| Area | What exists | Gap |
|------|-------------|-----|
| CIP-0005 / `lamd/validation.py` | Pre-gpp path and include checks | Does not inspect merged HTML or post-macro DOM |
| CIP-0007 | Macro emission, ARIA, JS fallbacks when elements missing | Does not detect duplicate ids across a document |
| CIP-000E (Proposed) | First-use / deployment failure inventory | Overlaps on “doctor” UX; different primary failure set |

Output validation is a distinct concern: **the pipeline can succeed while the artefact is wrong**.

### Why not rush the architecture

Validation could live at several layers:

1. **Authoring time** — lint snippets/macros for duplicate `\define{animationName}{...}` across a talk’s include graph
2. **GPP/post-gpp** — inspect intermediate markdown before pandoc
3. **Post-pandoc HTML** — parse built slides/notes/pages
4. **Post-build integration** — hook in makefile targets after each output format

Each layer has different visibility, cost, and error-message quality. Choosing prematurely risks either duplicated checks or checks that cannot see the actual failure (e.g. pandoc may rewrite ids). **Phase 0 must resolve this with evidence**, not preference.

## Detailed Description

### Goal (WHAT)

After a lamd build, users should be able to run validation (integrated or standalone) that catches **classes of output defects** with messages that name the offending source (file, macro, slide section) and suggest a fix — without requiring browser inspection or manual HTML diffing.

### Non-goals (for initial scope — confirm in Phase 0)

- Replacing pandoc or gpp
- Validating semantic correctness of content (e.g. “is this polynomial degree appropriate?”)
- Full HTML accessibility audit (axe-core class tooling) — may be a later extension
- Validating remote asset availability at view time (CDN/network)

### Phase 0 deliverable: failure-mode inventory

Before this CIP moves to **Accepted**, complete an inventory document at `cip/cip000F/inventory.md` (create when Phase 0 starts). For each failure mode, record:

| Field | Purpose |
|-------|---------|
| **ID** | Stable reference (e.g. `OUT-ANIM-DUP-GROUP`) |
| **Example** | Real or minimal repro (link to commit/snippet/talk) |
| **Detectable at** | Which pipeline stage can see it (include graph / gpp out / html / pdf) |
| **Severity** | silent-wrong / broken-output / degraded-a11y / warning-only |
| **User impact** | What the author/reader experiences |
| **Fix locus** | content / macro / build config / lamd code |
| **Priority** | P0–P3 for first implementation tranche |

**Seed list** (to validate/extend in Phase 0 — not authoritative):

1. **Duplicate animation group names** in one HTML document (this incident)
2. Duplicate HTML `id` attributes anywhere in slide output
3. Animation frame count mismatch (declared `startanimation` range vs emitted frames)
4. Broken relative image/diagram links in output HTML
5. Missing bibliography keys rendered as `[?]` or empty citations
6. Empty `\include{...}` expansion (silent omission)
7. Slides referencing undefined macros (may already fail at gpp — confirm)
8. Multiple `\startanimation` with same group in one file (intra-file duplicate)

Phase 0 should also **exercise the inventory** against 2–3 real talks (including `basis-functions-and-generalisation`) and note which modes appear in practice.

### Phase 1 deliverable: architecture decision (in this CIP)

After inventory, add a **Validation Architecture** subsection here (or fold into Detailed Description) that records:

- **Primary validation layer(s)** chosen and why
- **CLI surface** — e.g. extend `maketalk`/`make` target, `lamd validate-output`, or part of CIP-000E’s `lamd check`
- **Exit codes and makefile integration** — fail build vs warn-only per check class
- **Message format** — file:line when traceable; slide title/section when not
- **Explicit non-chosen alternatives** and why rejected

Do not start Phase 2 implementation until Phase 1 is written and reviewed.

### Candidate implementation sketch (Phase 2+, subject to Phase 0–1)

Likely first tranche if post-HTML is chosen:

- Parse built `.slides.html` (and optionally `.html` notes)
- Collect `id="animation-*"`, `id="range-*"`, `data-animation-group`, frame class names
- Report duplicates with slide/section context (reveal.js `section` elements)
- Unit tests on minimal HTML fixtures

Other tranches follow inventory priority — not committed here.

### Relationship to CIP-000E

CIP-000E scopes **environment and first-use** failures (missing dirs, people.yml, partial frontmatter). CIP-000F scopes **artefact integrity after a nominally successful build**. A unified `lamd check` command may eventually subsume both; until then, keep CIPs separate and note overlap in Phase 1 CLI design.

## Implementation Plan

### Phase 0 — Scoping and inventory (**required before Accepted**)

1. Create `cip/cip000F/inventory.md` from seed list above
2. Review 2–3 production talks; add observed failure modes
3. For each mode, prototype *detection feasibility* (manual grep/script — no product code yet):
   - Can include graph see it pre-gpp?
   - Does gpp output expose it?
   - Is it only visible in final HTML/PDF?
4. Draft priority ranking (P0 = silent wrong output, like duplicate animation ids)
5. **Pause:** present inventory for review; update this CIP; only then seek **Accepted**

### Phase 1 — Architecture decision (**required before In Progress**)

1. Choose validation layer(s) with rationale tied to inventory
2. Specify CLI/make integration and fail vs warn policy
3. Define message templates and test strategy
4. Identify backlog breakdown for Phase 2+
5. **Pause:** seek **Accepted** if not already; create backlog tasks only after Accepted

### Phase 2 — First tranche implementation

Depends on Phase 1 outcome. Expected shape if post-HTML wins:

1. Module under `lamd/` (e.g. `output_validation.py`) — location confirmed in Phase 1
2. Checks for P0 items from inventory
3. Tests with fixture HTML
4. Optional makefile hook behind explicit target (e.g. `make validate` or `maketalk --validate`)
5. Documentation in Sphinx/docs after validation (documentation lifecycle)

### Phase 3 — Expansion

Implement remaining inventory items by priority; consider snippet-graph lint for animation names if high value.

## Backward Compatibility

- Validation must be **opt-in or explicit target** initially (`make validate`, flag, or separate command) so existing CI/makefiles are unchanged
- Warn-only mode for checks that may false-positive until tuned
- No change to macro syntax required for Phase 2 duplicate-id detection
- Content fixes (like renaming animation groups) remain author responsibility; validator explains collisions

## Testing Strategy

**Phase 0:** manual scripts and grep on real outputs; document findings in inventory

**Phase 2+:**

- Unit tests on minimal HTML/markdown fixtures per check
- Regression fixture from Olympics duplicate case (pre-fix HTML should fail; post-fix should pass)
- Integration test: build a small talk with known defect → validator reports expected message
- No change to existing animation macro unit tests unless CLI integration added

## Related Requirements

- **REQ-0002** — Output defects should produce clear, actionable messages; users should catch problems without browser debugging
- **REQ-0004** — Animation behaviour should be predictable; duplicate groups violate that expectation silently

## Implementation Status

### Phase 0
- [ ] Create `cip/cip000F/inventory.md`
- [ ] Review real talks against seed failure modes
- [ ] Document detectability per pipeline stage
- [ ] Priority ranking agreed
- [ ] Phase 0 review complete (gate for Accepted)

### Phase 1
- [ ] Architecture decision recorded in this CIP
- [ ] CLI/make integration specified
- [ ] Backlog tasks created (after Accepted)

### Phase 2+
- [ ] Not started — blocked on Phase 0–1

## References

- Snippet fix: `snippets/_ml/includes/olympic-marathon-validation-fit.md` — group renamed to `olympic_LM_polynomial_number_val`
- Snippet fix: `snippets/_ml/includes/olympic-marathon-loo-validation.md`, `olympic-marathon-k-fold-validation.md` — outer fold `\startanimation` finish `1` → `5`
- Related snippet: `snippets/_ml/includes/olympic-marathon-all-polynomial.md`
- Talk: `mlfc/_lamd/basis-functions-and-generalisation.gpp.markdown`
- Runtime: `lamd/includes/slides-header.html` (`showDivs`, global class queries)
- Macros: `lamd/macros/talk-macros-slides-html.gpp`
- Input validation: `lamd/lamd/validation.py`, CIP-0005
- Animation improvements: CIP-0007
