---
category: bugs
created: "2026-10-23"
dependencies: []
github_issue: ""
id: 2026-10-23_mdlist-listperson-include
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
- templates
title: mdlist student and PDRA templates cannot include listperson
---

# Task: mdlist student and PDRA templates cannot include listperson

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).

## Description

`mdlist exstudents`, `expdras`, `students`, and `pdras` fail at render:

```
liquid.exceptions.TemplateNotFoundError: listperson
  -> lamd/templates/liststudent.md:1:13
* {% include 'listperson' %}
```

`listperson.md` exists in `lamd/templates/`. `mdlist` calls `get_template(listtemplate + ".md")`, so the outer template loads. Nested `{% include 'listperson' %}` does not add `.md`.

`lynguine.util.liquid.load_template_env` used to pass `FileExtensionLoader(..., ext=".md")`. Current python-liquid has no `liquid.loaders`; the fallback is `FileSystemLoader`, which looks for a file literally named `listperson`.

CVs that need RA/PhD lists therefore omit them.

## Acceptance Criteria

- [ ] `{% include 'listperson.md' %}` (or a loader that adds `.md`) resolves
- [ ] `mdlist exstudents` against the former-students YAML writes given/family names
- [ ] `mdlist expdras` against the former-RA YAML writes names
- [ ] Nested includes `extractperson`, `list_name`, `years`, `semester_term` still resolve

## Implementation Notes

Smallest lamd fix: suffix `.md` on includes in `liststudent.md` and `listpdra.md`. Optional follow-up in lynguine: restore an extension-aware loader so `ext=".md"` means something again.

`students.yaml` rows have top-level `given`/`family`, not a nested `person`. `listperson.md` already handles that when `person` is absent.

## Related

- CIP: 0015
- PRs: (lamd templates; optional lynguine loader)
- Documentation: CV includes that currently omit generated group lists

## Progress Updates

### 2026-10-23

Probed against live `students.yaml` and `ras.yaml`. Crash confirmed. Task created.
