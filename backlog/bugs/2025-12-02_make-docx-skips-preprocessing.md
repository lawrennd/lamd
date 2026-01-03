---
category: bugs
completed: '2025-12-02'
created: '2025-12-02'
id: 2025-12-02_make-docx-skips-preprocessing
last_updated: '2025-12-02'
priority: High
related_cips: []
status: Completed
title: make-docx.mk CV rule bypasses macro preprocessing
---

# Task: make-docx.mk CV rule bypasses macro preprocessing

## Description

The `make-docx.mk` makefile has a "Direct rule for CV generation" that runs pandoc directly on the source `.md` file **without preprocessing macros**. This means:

- `\include{}` macros are not expanded
- `\define{}` / `\ifdef{}` conditionals don't work  
- `\section{}` and other lamd macros are not processed
- The resulting DOCX contains raw macro text or empty content

### Current Broken Rule (lines 5-10)

```makefile
# Direct rule for CV generation
${BASE}.docx: ${BASE}.md
	pandoc -s \
		${CITEFLAGS} \
		${DOCXFLAGS} \
		-o ${BASE}.docx \
		${BASE}.md
```

### Correct Approach

The build should:
1. First preprocess the `.md` file with `${PP}` (gpp/macro processor) to expand all macros
2. Then run pandoc on the preprocessed output

Compare to the "original rule" (lines 13-19) which uses a preprocessed intermediate file:

```makefile
original-${BASE}.docx: ${BASE}.notes.docx.markdown ${DOCXDEPS}
	pandoc -s \
		${CITEFLAGS} \
		${DOCXFLAGS} \
		-B ${INCLUDESDIR}/${NOTATION} \
		-o ${BASE}.docx \
		${BASE}.notes.docx.markdown
```

## Impact

All CV generation using `makecv` produces empty/broken output with:
- No include content
- No macro expansions
- Just YAML header and blank lines

## Proposed Fix

Option A: Add preprocessing step to the direct rule:

```makefile
${BASE}.preprocessed.md: ${BASE}.md ${DEPS}
	${PP} $< -o $@ --format notes --to docx --code sparse --snippets-path ${SNIPPETSDIR} --macros-path=$(MACROSDIR) --diagrams-dir ${DIAGRAMSDIR} ${PPFLAGS}

${BASE}.docx: ${BASE}.preprocessed.md
	pandoc -s \
		${CITEFLAGS} \
		${DOCXFLAGS} \
		-o ${BASE}.docx \
		${BASE}.preprocessed.md
```

Option B: Remove the direct rule and use the original preprocessing pipeline.

## Acceptance Criteria

- [x] `\include{}` macros expand correctly in CV output
- [x] `\define{}` / `\ifdef{}` conditionals work
- [x] CV DOCX output contains all expected content
- [x] Sheffield CV includes policy, public understanding, publications, etc.

## Related

- File: `lamd/lamd/makefiles/make-docx.mk`
- Discovered when building Sheffield visiting professor CV
- Part of CV build chain bugs discovered 2025-12-02

## Progress Updates

### 2025-12-02
Task created. Issue discovered when Sheffield CV `.docx` output was nearly empty - just YAML header and blank lines. The `make-docx.mk` direct rule was identified as bypassing the macro preprocessing step entirely.

### 2025-12-02 (Fixed)
**Fix implemented**: Modified `make-docx.mk` to add preprocessing step before pandoc conversion:
- Added `${BASE}.preprocessed.md` rule that runs `${PP}` to expand all macros
- Updated `${BASE}.docx` rule to depend on `${BASE}.preprocessed.md` instead of `${BASE}.md`
- Pandoc now runs on the preprocessed file, ensuring all `\include{}`, `\define{}`, and other macros are expanded
- Added integration test `test_docx_rule_includes_preprocessing` to verify preprocessing is included

The fix follows Option A from the proposed solutions and matches the pattern used in the existing `.notes.docx.markdown` rule.