---
id: "2026-08-18_editme-main-file-fallback"
title: "Section edit links on non-snippet content go to a missing snippets file"
status: "Completed"
priority: "High"
created: "2026-08-18"
last_updated: "2026-08-18"
category: "bugs"
related_cips: []
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- bug
- edit-links
- mdpp
- gpp
---

# Task: Fall back to the document edit URL when `\editme` expands in the main file

## Description

Clicking a section-level **edit** control on content that lives in the talk
file, not a snippet, opens a GitHub URL that does not exist.

Reproduced on `talks/_posts/2026-09-07-time-to-reset.html`. The Diane Coyle
quote is inline in `_policy/time-to-reset.md`. The edit control beside
"Sovereignty Means Having Alternatives" goes to:

```
https://github.com/lawrennd/snippets/edit/main/time-to-reset.gpp.markdown
```

The intended target is the talks-repo URL already computed for the page-level
`edit_url`:

```
https://github.com/lawrennd/talks/edit/gh-pages/_policy/time-to-reset.md
```

### Why the wrong URL is built

`\editme` (in `lamd/macros/talk-macros-edit.gpp`) stores a link of
`\githubBaseUrl\file` and defers expansion until the next `\section` /
`\subsection`. Two things then go wrong together:

1. **`githubBaseUrl` is hardcoded** in `mdpp.py` to the snippets repo
   (`https://github.com/lawrennd/snippets/edit/main/`). That is correct for
   snippet includes. It is never the talks repo.

2. **`\file` is GPP's current input file**, expanded lazily. For snippet
   content that is still inside `\include`, that is the snippet path and the
   snippets URL works. For content in the talk file, GPP is reading the
   preprocessor temp file that `mdpp` always names `{stem}.gpp.markdown`
   (HTML/notes path; Manim uses `.gpp.py` and does not load edit macros).

The motivating case is a leftover `\editme`. `_policy/includes/compute-concentration.md`
calls `\editme` but has no heading of its own, so the stored link is emitted by
the *next* heading in the talk — the inline Sovereignty section. At that point
`\file` is `time-to-reset.gpp.markdown`.

The page-level `edit_url` in HTML frontmatter is already correct. It is
produced later by `flags.py` from `ghub` in `_lamd.yml` and passed to pandoc
as metadata. GPP never sees it, so `\editme` cannot use it today.

## Acceptance Criteria

- [x] An `\editme` that expands while GPP is still in the main preprocessor
      input (the talk file, including leftover snippet `\editme`s that fall
      through to a talk heading) links to the same GitHub URL as the page-level
      `edit_url` (`ghub` organization/repository/branch/directory plus the
      source basename with `.md`)
- [x] An `\editme` that expands inside an `\include` still links to
      `githubBaseUrl` plus the snippet path (existing snippet behaviour
      unchanged)
- [x] The fallback does **not** sniff the `.gpp.markdown` suffix in GPP.
      `mdpp` passes the exact temp path it hands to GPP (`gppTempFile`) and
      the talks URL (`localEditUrl`); the edit macro uses `\ifeq{\file}{\gppTempFile}`
- [x] If `ghub` is missing, the macro still produces a snippets-style link
      (current behaviour) rather than a broken empty href
- [x] Unit tests cover: (1) `mdpp` emits `-DgppTempFile` and `-DlocalEditUrl`
      when `ghub` is present; (2) a fixture where `\editme` is followed by a
      heading in the main file resolves to `localEditUrl`; (3) a fixture where
      `\editme` is followed by a heading inside an include still uses the
      snippets URL
- [x] Rebuilding `time-to-reset` posts HTML, the Sovereignty heading edit
      control opens `_policy/time-to-reset.md` on the talks repo, not
      `time-to-reset.gpp.markdown` on snippets

## Implementation Notes

Do **not** capture `\file` at `\editme` call time with `\defeval`. That would
send the Coyle heading to `compute-concentration.md`. The check belongs at
**expansion** time, which is already when `\file` is evaluated.

`mdpp.setup_gpp_arguments` / `main()` should add, using the same `ghub`
fields as `flags.py` (`organization`, `repository`, `branch`, `directory`)
and `os.path.splitext(args.filename)`:

```text
-DgppTempFile=<exact string passed as GPP infile>
-DlocalEditUrl=https://github.com/{org}/{repo}/edit/{branch}/{directory}/{stem}.md
```

`gppTempFile` must be the identical path string later appended to the `gpp`
command. GPP `\file` is "the filename as it appears on the command line", so
exact equality is reliable; `\ifeq` cannot do suffix matching.

In `talk-macros-edit.gpp`, the href target becomes:

```text
\ifeq{\file}{\gppTempFile}\localEditUrl\else\githubBaseUrl\file\endif
```

That predicate means: still in the talk file GPP is preprocessing → document
URL; inside an `\include` → snippets URL.

`compute-concentration.md` will still have no button pointing at itself
(it has `\editme` and no heading). That is pre-existing snippet authoring.
The visible button sits on talk content and should open the talk.

Update `tests/unit/test_mdpp.py`, which currently asserts the hardcoded
snippets `githubBaseUrl`. Keep that assert; add asserts for the new `-D`
flags.

## Related

- Macros: `lamd/macros/talk-macros-edit.gpp`
- Preprocessor: `lamd/mdpp.py` (`githubBaseUrl`, `.gpp.markdown` temp file)
- Page-level URL: `lamd/flags.py` (`edit_url` from `ghub`)
- Tests: `tests/unit/test_mdpp.py`, `tests/unit/test_flags.py`
- Example: `talks/_policy/time-to-reset.md`, snippet
  `snippets/_policy/includes/compute-concentration.md`
- Docs: `docs/contexts/definition.md` (`\editme`), `docs/guides/snippets.md`

## Progress Updates

### 2026-08-18

Task created with Proposed status after diagnosing the time-to-reset
Sovereignty edit link.

Updated to Ready: approach agreed (pass `gppTempFile` and `localEditUrl`
from mdpp; compare at expansion time). Implementation follows.

Updated to In Progress.

Implemented: `mdpp` always passes `-DgppTempFile` and, when `ghub` is
complete, `-DlocalEditUrl`. The edit macro compares `\file` to
`\gppTempFile` at expansion time. Unit and GPP fixture tests in
`tests/unit/test_mdpp.py` pass. Rebuilt `time-to-reset` posts HTML: the
Sovereignty heading now opens
`https://github.com/lawrennd/talks/edit/gh-pages/_policy/time-to-reset.md`.

Updated to Completed.
