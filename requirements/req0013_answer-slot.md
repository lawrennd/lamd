---
id: "0013"
title: "Authors can reserve lecturer answers and student blank space from one LaMD source"
status: "Proposed"
priority: "High"
created: "2026-10-31"
last_updated: "2026-10-31"
related_tenets:
  - "single-source-multiple-contexts"
  - "academic-rigor-through-tooling"
stakeholders:
  - "Module conveners reconstructing lecture notes with worked answers"
  - "Students receiving the same notes with answer space left blank"
tags:
  - notes
  - slides
  - teaching
  - answers
---

# REQ-0013: Authors can reserve lecturer answers and student blank space from one LaMD source

> **Remember**: Requirements describe **WHAT** should be true (outcomes), not HOW to achieve it.

## Description

A LaMD source can mark a worked answer in place, with a height for the blank that students write into. Lecturer notes and slides show the answer. Student notes keep that vertical space empty. The source is not rewritten between the two builds.

This is not an exercise wrapper. The surrounding question, heading, and marks stay in the authoring. The slot only chooses between printing the answer and leaving space.

**Why this matters**: Lecture notes that derive a result on the page need the derivation in the lecturer copy and a writing gap in the student copy. Maintaining two sources, or stuffing the answer into an assignment question, breaks the single-source model.

**Who benefits**: Conveners who ship lecturer and student PDFs of the same talk, and courses converting archives that already used this pattern.

## Acceptance Criteria

- [ ] Authors can mark an in-place answer together with a blank height, without wrapping the surrounding question as an exercise.
- [ ] Lecturer notes include the answer text.
- [ ] Student notes omit the answer text and leave vertical space of the requested height.
- [ ] Slides include the answer text in both lecturer and student builds.
- [ ] Existing assignment and exercise macros keep their current behaviour.

## Notes (Optional)

CIP-0017 and REQ-0012 left student/lecturer answer variants out of the Beamer slides-PDF work. This requirement covers that gap for notes and for the slides view of the same source.

Speaker notes remain a separate channel: they are presenter asides, not student blanks and not course-note body.

## References

- **Related Tenets**: [Single Source, Multiple Contexts](../tenets/single-source-multiple-contexts.md), [Academic Rigor Through Tooling](../tenets/academic-rigor-through-tooling.md)
- **Related CIPs**: CIP-0017 (out of scope for answer variants), CIP-0019 (answer slot)

## Progress Updates

### 2026-10-31
Requirement drafted for the NPA notes.cls `\answer{body}{vspace}` reconstruction, alongside CIP-0019.
