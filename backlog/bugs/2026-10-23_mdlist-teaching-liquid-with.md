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

`with` is a Liquid tag. python-liquid therefore refuses `{% if with %}`. `data/teaching.yaml` uses `with:` for co-teachers (5 of 18 rows). The ACP teaching statement and `includes/current-teaching.md` omit or cannot use the generated list because of this.

## Acceptance Criteria

- [ ] `listteaching.md` does not use the identifier `with`
- [ ] `mdlist teaching $HOME/lawrennd/data/teaching.yaml` exits 0 and lists Cambridge modules
- [ ] Co-teachers still render (Carl Henrik Ek, Ferenc Huszár, Nic Lane)
- [ ] Matching YAML key in `lawrennd/data` teaching.yaml is updated in the same window (cv CIP-0006)

## Implementation Notes

Rename the template field to `collaborators` (already used in `grants.yaml`). Do not try to quote `with` as a Liquid identifier.

Data PR is not this repo: `teaching.yaml` `with:` → `collaborators:`.

## Related

- CIP: 0015
- PRs: (lamd templates; data teaching.yaml)
- Documentation: cv `cambridge/includes/acp12-teaching-statement.md` (workaround note)

## Progress Updates

### 2026-10-23

Probed against live `teaching.yaml`. Crash confirmed. Task created.
