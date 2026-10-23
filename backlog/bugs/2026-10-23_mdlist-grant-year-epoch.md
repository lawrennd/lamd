---
category: bugs
created: "2026-10-23"
dependencies: []
github_issue: ""
id: 2026-10-23_mdlist-grant-year-epoch
last_updated: "2026-10-23"
owner: Neil Lawrence
priority: Medium
related_cips: ["0015"]
status: Proposed
tags:
- backlog
- bug
- mdlist
- grants
title: mdlist grants render integer years as 1970 and a literal newline
---

# Task: mdlist grants render integer years as 1970 and a literal newline

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

`mdlist grants` writes rows such as:

```
* Deep Probabilistic Models ..., from 1970 to 1970 funded by EPSRC ...
```

Those grants in `data/grants.yaml` have `start: 2016` / `end: 2020` (YAML integers). `listgrant.md` uses `{{start | date: "%Y"}}`. Liquid's date filter treats a small integer as seconds since the Unix epoch, hence 1970.

`cvlists.yml` `grants.compute.preprocessor` includes `convert_year_iso`, but preprocess is skipped (`2025-12-02_mdlist-preprocess-filtering`). Recent grants already use ISO dates (`2022-02-07`) and render correctly.

The same template ends with a literal `\n`, so each item shows a backslash-n in the Word CV.

`mdlist grants` and `mdlist exgrants` are currently byte-identical (filter bug, not this template).

## Acceptance Criteria

- [ ] Integer years in YAML do not render as 1970 (preprocess *or* ISO dates in data)
- [ ] `listgrant.md` does not emit a literal `\n`
- [ ] After filtering works, current vs former grant lists differ

## Implementation Notes

lamd: strip `\n` from `listgrant.md` immediately.

Data: convert remaining integer `start`/`end` to ISO (`2016-01-01`). That makes Liquid safe even before referia preprocess is restored. 23 of 28 grants still use ints.

Do not treat 1970 as a missing-date sentinel in the template.

## Related

- CIP: 0015
- Depends on: `2025-12-02_mdlist-preprocess-filtering` for current vs former
- PRs: (lamd template; grants.yaml in the data repo)

## Progress Updates

### 2026-10-23

Live `grants.yaml` counted: 28 rows, 23 integer starts, 5 ISO dates. Output matched. Task created.
