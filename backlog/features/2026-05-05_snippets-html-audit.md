---
id: "2026-05-05_snippets-html-audit"
title: "Audit snippets repo: wrap raw HTML in \\figure{} with \\html{}"
status: "In Progress"
priority: "Medium"
created: "2026-05-05"
last_updated: "2026-05-05"
related_cips: ["000C"]
---

# Task: Audit snippets repo: wrap raw HTML in `\figure{}` with `\html{}`

## Description

Several snippets in the `lawrennd/snippets` repository embed raw HTML/JS directly
as the `contents` argument of `\figure{}` (or other macros).  When these snippets
are included in a talk compiled with `--to manim`, the raw HTML leaks into the
generated Python file and causes a `SyntaxError`.

The correct fix is to wrap the HTML block and any JS `\include{...}` in `\html{}`
so the content is suppressed in all non-HTML formats automatically.

## Acceptance Criteria

- All `\figure{}` calls in the snippets repo that pass raw HTML as the first
  argument have that HTML wrapped in `\html{...}`.
- All `\include{_scripts/...}` calls that pull in JavaScript are similarly
  wrapped or already inside `\html{}`.
- Running `mdpp --to manim` on a talk that includes any audited snippet no longer
  produces HTML-related `SyntaxError`.

## Implementation Notes

Search pattern for candidates:

```bash
rg -n '\\figure\{' --include='*.md' /path/to/snippets \
  | rg -v '\\html\{'   # narrow to figures without \html{} on the same line
```

Also search for `<div`, `<canvas`, `<script` etc. outside `\html{}` blocks.

This is tracked separately from the `lamd` repo because it touches a different
repository (`lawrennd/snippets`).

## Known Fixed Files

- `_physics/includes/multigame-entropy.md` — fixed 2026-05-05 (commit 2aaa9b49)

## Related

- CIP: 000C
- See also: `backlog/features/2026-05-05_html-stripping-safety-net.md`
- See also: `backlog/features/2026-05-05_htmlmanim-macro.md`

## Progress Updates

### 2026-05-05
Task created.  `_physics/includes/multigame-entropy.md` has already been fixed.
Status is In Progress pending a full audit of the snippets repo.
