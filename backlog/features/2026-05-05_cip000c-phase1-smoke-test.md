---
id: "2026-05-05_cip000c-phase1-smoke-test"
title: "Phase 1 smoke test: mdpp --to manim on minimal talk"
status: "Completed"
priority: "Medium"
created: "2026-05-05"
last_updated: "2026-05-05"
completed: "2026-05-05"
category: "features"
related_cips: ["000C"]
owner: ""
dependencies: ["2026-05-05_cip000c-mdpp-manim-format"]
tags:
- backlog
- manim
- testing
- cip-000c
---

# Task: Phase 1 smoke test

## Description

Create a minimal fixture talk and verify that `mdpp --to manim` produces a syntactically valid Python file. This validates the end-to-end Phase 1 pipeline before moving to Phase 2.

## Acceptance Criteria

- [ ] A fixture talk `lamd/tests/fixtures/minimal-manim-talk.md` exists with at least: YAML frontmatter, `\newslide{Title}`, `\slides{some text}`, `\notes{some notes}`, `\speakernotes{a note}`
- [ ] Running `mdpp --to manim minimal-manim-talk.md -o /tmp/minimal-manim-talk.slides.manim.py` completes without error
- [ ] The generated `.slides.manim.py` passes `python -m py_compile`
- [ ] `_lamd_manim.py` is written to the same output directory
- [ ] The smoke test is captured as an automated test (e.g. in `lamd/tests/test_mdpp_manim.py`) so it runs in CI

## Implementation Notes

The test does not need Manim or manim-slides to be installed — it only checks Python syntax. The `py_compile` check is sufficient to catch macro expansion errors (unclosed brackets, bad indentation, etc.).

## Related

- CIP: 000C
- Depends on: `2026-05-05_cip000c-mdpp-manim-format`

## Progress Updates

### 2026-05-05

Task created as part of CIP-000C Phase 1.
