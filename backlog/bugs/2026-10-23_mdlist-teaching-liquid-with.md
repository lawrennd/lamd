---
category: bugs
created: "2026-10-23"
dependencies: []
github_issue: ""
id: 2026-10-23_mdlist-teaching-liquid-with
last_updated: "2026-10-23"
owner: Neil Lawrence
priority: High
related_cips: ["0015"]
status: Proposed
tags:
- backlog
- bug
- mdlist
- liquid
- teaching
title: mdlist teaching crashes on Liquid reserved word with
---

# Task: mdlist teaching crashes on Liquid reserved word `with`

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

`mdlist teaching` and `mdlist exteaching` die before writing a list:

```
liquid.exceptions.LiquidSyntaxError: expected a primitive expression, found with
  -> lamd/templates/listteaching.md:1:101
{%if with %}(with {%for name in with%}...
```

`with` is a Liquid tag. python-liquid therefore refuses `{% if with %}`. Teaching YAML uses `with:` for co-teachers. Current-teaching includes omit or cannot use the generated list because of this.

## Acceptance Criteria

- [ ] `listteaching.md` does not use the identifier `with`
- [ ] `mdlist teaching` against the teaching YAML exits 0 and lists current modules
- [ ] Co-teachers still render from the `collaborators` field
- [ ] Matching YAML key in the teaching data file is updated in the same window (cv reintegration CIP)

## Implementation Notes

Rename the template field to `collaborators` (already used in `grants.yaml`). Do not try to quote `with` as a Liquid identifier.

Data PR is not this repo: `teaching.yaml` `with:` → `collaborators:`.

## Related

- CIP: 0015
- PRs: (lamd templates; data teaching.yaml)
- Documentation: CV teaching includes that currently omit the generated list

## Progress Updates

### 2026-10-23

Probed against live `teaching.yaml`. Crash confirmed. Task created.
