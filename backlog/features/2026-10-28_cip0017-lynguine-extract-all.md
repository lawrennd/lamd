---
id: "2026-10-28_cip0017-lynguine-extract-all"
title: "Include slides.pdf in lynguine extract_all when slidespdf is set"
status: "Completed"
priority: "Medium"
created: "2026-10-28"
last_updated: "2026-10-28"
category: "features"
related_cips: ["0017"]
owner: "Neil D. Lawrence"
dependencies: ["2026-10-28_cip0017-flags-cli"]
tags:
- backlog
- cip0017
- lynguine
- dependencies
---

# Task: lynguine extract_all for slidespdf

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).

## Description

When frontmatter `slidespdf` is true, `lynguine.util.talk.extract_all` must list `{base}.slides.pdf` so `make all` builds the Beamer deck. Until this is installed, `maketalk --format slides --to pdf` is enough.

## Acceptance Criteria

- [ ] `extract_all` appends `base.slides.pdf` when `slidespdf` is true
- [ ] Existing flags (`notespdf`, `reveal`, …) still produce the same list
- [ ] Unit test in lynguine covers the new field

## Implementation Notes

Patch `/Users/neil/lawrennd/lynguine/lynguine/util/talk.py` and `lynguine/tests/test_util_talk.py`.

## Related

- CIP: 0017

## Progress Updates

### 2026-10-28

Task created after CIP-0017 was accepted.
