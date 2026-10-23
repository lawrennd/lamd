---
category: bugs
created: "2026-10-23"
dependencies: []
github_issue: ""
id: 2026-10-23_mdlist-talks-empty-entries
last_updated: "2026-10-23"
owner: Neil Lawrence
priority: High
related_cips: ["0015"]
status: Proposed
tags:
- backlog
- bug
- mdlist
- talks
title: invited-talk-list.markdown is empty bullets from the whole talks tree
---

# Task: invited-talk-list.markdown is empty bullets from the whole talks tree

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

Cambridge ACP `make invited-talk-list.markdown` writes 1,324 lines of:

```
* , **,
```

`listtalk.md` is `* {{title}}, *{{venue}}*, {{ date | date: "%d %B %Y"}}`. The invited-talk records that belong on a CV live in `talks/_posts/` (250 files, `layout: talk`, `title`, `venue`, `date`). `_lamd.yml` sets `talksdir: $HOME/lawrennd/talks` (repo root). `make-lists.mk` runs `find $(TALKSDIR) -name '*.md'`, so lecture notes (`_accelerate/accelerator-intro.md` has `title` and `abstract` only, no `venue`/`date`) and other trees are mixed in. Combined with skipped preprocess/augmentors, the CV include is unusable.

ACP `includes/acp12-recognition.md` still `\include{../includes/invited-talks.md}`.

## Acceptance Criteria

- [ ] `make-lists.mk` prefers `$(TALKSDIR)/_posts` when that directory exists
- [ ] Generated talk list has venue/date lines, not empty `* , **, `
- [ ] `talksince` / `-s` then drops talks before the cut (depends on filtering backlog)
- [ ] Empty `_posts` does not fall back to scanning `.`

## Implementation Notes

lamd makefile change is sufficient for a default talks clone. cv CIP-0006 can also set `talksdir` to `$HOME/lawrennd/talks/_posts`. Do both.

Do not pass the whole talks repo as invited talks.

## Related

- CIP: 0015
- Depends on: `2025-12-02_mdlist-preprocess-filtering` for the year cut
- PRs: (lamd makefile; cv `_lamd.yml`)

## Progress Updates

### 2026-10-23

Cambridge leftover `invited-talk-list.markdown` (00:06) inspected: 1,324 empty bullets. Talk `_posts` sample has usable frontmatter. Task created.
