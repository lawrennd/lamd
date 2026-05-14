---
category: features
created: '2026-05-05'
id: 2026-05-05_html-stripping-safety-net
last_updated: '2026-05-05'
priority: Medium
related_cips:
- 000C
status: Abandoned
owner: "Neil Lawrence"
title: HTML-block stripping safety net in mdpp.py Manim post-processor
---

# Task: HTML-block stripping safety net in mdpp.py Manim post-processor

## Description

Raw HTML tags (`<div>`, `<canvas>`, `<script>`, `<button>`, etc.) embedded in
`\figure{}` arguments or other macro content can leak into the generated
`.manim.py` file, causing a `SyntaxError` when Python tries to parse the output.

The correct long-term fix is to wrap all HTML-only content in `\html{}` (which is
already a no-op in all non-HTML formats).  However, because the snippets
repository contains many files that have not yet been audited and updated, a
safety-net post-processor in `mdpp.py` is needed as a backstop.

## Acceptance Criteria

- After the existing first-pass strip (which removes macro-file verbatim output
  before `from manim import`), a second pass scans the generated Python file for
  lines starting with block-level HTML opening tags.
- When a block-level HTML tag is detected, the scanner collects all lines up to the
  matching closing tag (stack-based, handling nesting) and replaces the entire block
  with a single comment: `# [html content suppressed: <tag>]`.
- The output is still valid Python after stripping.
- A test (`TestMdppManim_HtmlStripping`) verifies the behaviour.

## Implementation Notes

- The HTML tag set covers: `div`, `canvas`, `script`, `button`, `span`, `select`,
  `option`, `iframe`, `p`, `table`, `thead`, `tbody`, `tr`, `td`, `th`, `ul`,
  `ol`, `li`, `form`, `input`, `label`, `nav`, `section`, `article`, `aside`,
  `header`, `footer`, `figure`, `figcaption`, `video`, `audio`, `source`.
- The regex for opening tags: `^\s*<(tag)(\s[^>]*)?>` (case-insensitive).
- The scanner only applies to Manim targets (`--to manim` or `--to manim-video`).

## Related

- CIP: 000C
- See also: `backlog/features/2026-05-05_snippets-html-audit.md`
- See also: `backlog/features/2026-05-05_htmlmanim-macro.md`

## Progress Updates

### 2026-05-05
Task created and implemented as part of handling HTML/JS content in Manim output.
Status set to Completed. Implementation is in `lamd/mdpp.py` (second pass block,
lines ~499–557). Tests added to `lamd/tests/test_mdpp_manim.py`.

### 2026-05-05 (later)
Approach abandoned. The safety net silently suppresses HTML content, which
violates the "Explicit over Implicit" tenet — authors would not know their
content was missing. The correct approach is to fix the source: wrap all
HTML-only content in `\html{}`. All known snippets have been updated
(see commit in snippets repo). The safety-net code and its tests have been
removed. If raw HTML leaks into Manim output the resulting `SyntaxError`
from `py_compile` is the desired signal.