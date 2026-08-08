---
id: "2026-08-08_maketalk-create-output-dirs"
title: "maketalk fails if output directories (_lectures, slides, etc.) do not exist"
status: "Proposed"
priority: "High"
created: "2026-08-08"
last_updated: "2026-08-08"
category: "bugs"
related_cips: []
owner: ""
dependencies: []
tags:
- backlog
- bug
- maketalk
- makefile
- robustness
---

# Task: Auto-create output directories in maketalk

## Description

On a fresh module, the output directories referenced in `_lamd.yml` (`postsdir`,
`slidesdir`, `notesdir`, `notebooksdir`, `practicalsdir`) do not exist. When
`maketalk` runs it tries to `cp` compiled outputs into these directories and
immediately fails:

```
cp: ../_lectures//02-01-example.html: No such file or directory
make: *** [example.posts.html] Error 1
```

`check-directories` in `make-talk-flags.mk` (line 154) only validates that
`snippetsdir` and `bibdir` exist — it does not create or validate the output
directories, nor does any other make target.

## Acceptance Criteria

- [ ] Running `maketalk` on a fresh module with valid `_lamd.yml` succeeds without
      requiring the user to manually create output directories
- [ ] Output directories are created (`mkdir -p`) before the first `cp` into them
- [ ] Behaviour is unchanged for modules where the directories already exist

## Implementation Notes

Two possible approaches:

**Option A — `check-directories` creates them:**
```makefile
check-directories:
    @echo "Checking required directories..."
    @mkdir -p "$(POSTSDIR)" "$(SLIDESDIR)" "$(NOTESDIR)" "$(NOTEBOOKSDIR)" "$(PRACTICALSDIR)"
    ...
```

**Option B — each `cp` rule uses `mkdir -p` inline:**
```makefile
$(POSTSDIR)/%.html: %.html
    mkdir -p $(POSTSDIR) && cp $< $@
```

Option A is simpler and creates all dirs up front as part of `check-directories`.

## Related

- PRs:
- Discovered via: vibecourse fresh-install testing (2026-08-08)
