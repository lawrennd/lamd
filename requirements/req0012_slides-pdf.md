---
id: "0012"
title: "Authors can produce PDF slides from the same LaMD source as Reveal HTML"
status: "Implemented"
priority: "High"
created: "2026-10-28"
last_updated: "2026-10-28"
related_tenets: []
stakeholders:
  - "Module conveners who need printable or archival slide decks"
  - "Courses reconstructing legacy lecture PDFs from LaMD sources"
tags:
  - slides
  - pdf
  - beamer
  - latex
  - teaching
---

# REQ-0012: Authors can produce PDF slides from the same LaMD source as Reveal HTML

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

A LaMD talk that already builds Reveal HTML slides can also produce a PDF slide deck from that same source. Slide-only content (`\slides{}`, `\newslide{}`) appears in the PDF; notes-only content does not. The PDF is a first-class sibling of the HTML deck, not a print-to-PDF of the browser view.

Notes PDF remains a separate artefact. This requirement does not change how lecture-notes PDFs look, and it does not require a FoilTeX or other legacy slide class.

**Why this matters**: Printable and archival slide PDFs are a primary teaching artefact. Several reconstructed courses need to compare LaMD output against historical lecture PDFs. Reveal HTML cannot serve that comparison.

**Who benefits**: Conveners who ship slide PDFs, and anyone checking that a converted course still contains the original material once printed.

## Acceptance Criteria

- [ ] Authors can request a slides PDF from frontmatter and from `maketalk --format slides --to pdf`.
- [ ] The slides PDF is built from the slides view of the source (`\slides{}` kept, `\notes{}` dropped).
- [ ] Each `\newslide` becomes one PDF frame. Reveal-only attributes (backgrounds, font-size classes, scrollable) do not have to be honoured in v1.
- [ ] Reveal HTML, PPTX, and notes PDF behaviour is unchanged when the new flag is off.
- [ ] A small fixture talk with `\newslide`, slide bullets, a figure, and maths builds a PDF.

## Notes (Optional)

Legacy FoilTeX chrome (20pt foils, Sheffield headers) is out of scope. Student-blank answer space in notes PDFs is also out of scope here; see [REQ-0013](req0013_answer-slot.md).

The existing `pdf:` frontmatter field is Jekyll metadata for a generic PDF link. It must not be overloaded as the slides-PDF build switch; use a dedicated `slidespdf` flag analogous to `notespdf`.

## References

- **Related CIPs**: CIP-0017 (Beamer slides PDF pipeline), CIP-0019 (answer slot)
- **Related requirements**: [REQ-0011](req0011_exercise-sheet-pdf.md) (notes/exercise PDFs), [REQ-0013](req0013_answer-slot.md) (lecturer/student answer slot)

## Progress Updates

### 2026-10-28
Requirement drafted alongside CIP-0017 for NPA PDF reconstruction.
