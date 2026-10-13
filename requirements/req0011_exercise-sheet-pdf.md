---
id: "0011"
title: "Authors can produce lean exercise-sheet PDFs from LaMD sources"
status: "Validated"
priority: "Medium"
created: "2026-10-11"
last_updated: "2026-10-11"
related_tenets: []
stakeholders:
  - "Module conveners writing worksheets and assignments"
  - "Students receiving printable handouts"
tags:
  - notes
  - pdf
  - latex
  - teaching
---

# REQ-0011: Authors can produce lean exercise-sheet PDFs from LaMD sources

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

When a LaMD source is a worksheet or assignment, the notes PDF should read as an exercise sheet — compact header with due date and candidate line, short brief instead of a journal-style abstract, and no unused bibliography machinery — rather than as a general lecture-notes article.

Lecture notes PDFs that are not worksheets must keep their existing appearance unless the author opts into the exercise layout.

**Why this matters**: Printable handouts are a primary teaching artefact. A template aimed at papers and lecture notes produces cluttered, misleading sheets and brittle builds (for example bibtex with no citations).

**Who benefits**: Conveners who ship worksheets via `notespdf`, and students who print them.

## Acceptance Criteria

- [x] Authors can select an exercise-sheet LaTeX layout for notes PDF from frontmatter (explicitly, or by a documented convenience when the source is an assignment).
- [x] Exercise-sheet PDFs omit unused bibliography steps when the document has no citations.
- [x] Default notes PDF behaviour for non-exercise sources is unchanged.
- [x] At least one real worksheet (e.g. IEI Worksheet 1) builds cleanly with the exercise layout.

## Notes (Optional)

Related bug: empty bibtex failure on citation-free notes PDFs. Related design lives in CIP-0013.

## References

- **Related CIPs**: CIP-0013 (proposed)

## Progress Updates

### 2026-10-11
Requirement drafted alongside CIP-0013.

### 2026-10-11 (later)
CIP-0013 accepted; implementation started.

### 2026-10-11 (impl)
CIP-0013 implemented; Worksheet 1 builds with exercise template (2 pages).
