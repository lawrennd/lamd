---
author: Neil Lawrence
created: '2026-08-08'
id: '000E'
last_updated: '2026-08-08'
status: Proposed
related_requirements: ["0002"]
tags:
- cip
- robustness
- installation
- course-deployment
- graceful-degradation
title: Robust First-Use and Course Deployment
---

# CIP-000E: Robust First-Use and Course Deployment

## Status

- [x] Proposed
- [ ] Accepted
- [ ] In Progress
- [ ] Implemented
- [ ] Closed

## Summary

lamd currently fails ungracefully in first-use and course deployment scenarios — situations where the environment is real but imperfect: missing output directories, incomplete `people.yml` entries, absent image files, or partially-configured talk frontmatter. This CIP establishes a programme of structured experimentation to **scope the full set of failures**, then derives a prioritised backlog of fixes to make lamd reliable as a course tool.

This addresses REQ-0002 (Processing Errors Are Clear and Actionable): errors should tell the user what went wrong and how to fix it, not terminate silently or with a Python traceback.

## Motivation

The immediate triggers are two bugs found during vibecourse deployment:

1. `maketalk` fails if output directories (`_lectures`, `slides`, etc.) do not exist
2. `mdpeople` crashes when a `people.yml` entry is missing the `image` field

But these are almost certainly the visible tip of a larger iceberg. Course deployments differ from developer environments in predictable ways:

- Directories may not be pre-created
- Configuration files (`people.yml`, bibliography files, include paths) may be partial or missing optional fields
- Snippets repositories may not be cloned
- System tools (`gpp`, `pandoc`, `inkscape`) may be missing or wrong versions
- Talk frontmatter may omit optional-but-assumed fields

Without a systematic survey, individual bug fixes will keep arriving as surprises. A scoping experiment run against a realistic course environment will reveal the full picture before committing to an implementation plan.

## Detailed Description

### Design Principles

Every lamd utility should apply a consistent policy when encountering missing or malformed configuration:

| Situation | Current behaviour | Target behaviour |
|---|---|---|
| Missing output directory | Fatal error / silent fail | Create directory with a warning |
| Missing optional field in YAML | `KeyError` traceback | Skip with a clear warning message |
| Missing optional file (image, bib) | Crash or broken output | Warn and continue without that element |
| Missing system tool | Cryptic error from subprocess | Clear "tool X not found — install with Y" message |
| Missing snippets repo | Silent broken include | Warning with suggested `git clone` command |

This is not about ignoring errors — hard configuration mistakes (wrong file format, missing mandatory fields) should still fail clearly. The goal is to distinguish **recoverable absences** from **genuine errors**.

### Scope of Experimentation

Phase 0 (see below) will test lamd in a clean course environment and document every failure point, categorised as:

- **Crash** — unhandled exception, non-zero exit with no useful message
- **Silent failure** — command exits 0 but produces wrong/empty output
- **Confusing error** — error message that does not tell the user what to do
- **Dependency gap** — requires a tool or file not mentioned in the docs

## Implementation Plan

### Phase 0: Scoping Experiment (Before Accepting This CIP)

**Goal**: Enumerate all failure modes in a realistic course deployment.

**Method**:
1. Start from a fresh clone of vibecourse (or equivalent course repo)
2. Follow the documented installation steps as a student would
3. Run `maketalk`, `mdpeople`, `mdlist`, `mdfield`, `mdpp` on representative course content
4. Record every failure with: command, error message, root cause, proposed fix category
5. Document the results in `cip/cip000E/scoping-results.md`

**Output**: A prioritised list of failure modes that becomes the backlog for Phases 1–3.

**Acceptance gate**: CIP moves to Accepted only after the scoping results are written up and reviewed.

### Phase 1: Critical Crashes (Known)

Fix failures that cause unhandled exceptions or silent bad output. At minimum:

- `maketalk`: create missing output directories rather than failing
- `mdpeople`: handle missing `image`, `url`, and other optional fields gracefully

Additional items will be added from Phase 0 results.

### Phase 2: Graceful Degradation Across All Utilities

Apply the design principles table above consistently across all lamd entry points:

- `mdpp` — missing include files, missing macros directory
- `mdlist` — missing or malformed frontmatter fields
- `mdfield` — missing fields (return empty/default rather than crash)
- `maketalk` — missing bibliography, missing snippets repo, missing system tools

### Phase 3: First-Use Documentation and Diagnostics

- Add a `lamd check` or `lamd doctor` command that validates the environment and reports what is missing
- Update the installation guide to document prerequisites and common first-use failures
- Add a course-deployment checklist to the docs

## Backward Compatibility

- All changes are additive: graceful handling replaces crashes, not functionality
- No changes to the public API or macro syntax
- Existing well-configured environments are unaffected

## Testing Strategy

- Each Phase 1/2 fix accompanied by a test covering the previously-crashing scenario
- Phase 0 scoping document serves as the test specification
- Integration tests run against a minimal "sparse" course environment fixture

## Related Requirements

- **REQ-0002**: Processing Errors Are Clear and Actionable — the primary requirement this implements

A new requirement may be warranted after Phase 0 scoping: *"lamd installs and runs correctly in a first-use course environment"*. This will be assessed once the failure inventory is complete.

## Scoping Results

*To be populated during Phase 0. Add rows as failures are discovered.*

| Command | Error / Symptom | Category | Root Cause | Proposed Fix |
|---|---|---|---|---|
| `maketalk` | Fails if `_lectures/`, `slides/` etc. don't exist | Crash | No `mkdir -p` before writing output | Auto-create directories |
| `mdpeople` | `KeyError: 'image'` on sparse `people.yml` entries | Crash | No `.get()` / default for optional fields | Use `.get()` with sensible defaults |

**Categories**: Crash · Silent failure · Confusing error · Dependency gap

## Implementation Status

- [ ] Phase 0: Scoping experiment complete (results in table above)
- [ ] Phase 1: Critical crash fixes
- [ ] Phase 2: Graceful degradation across all utilities
- [ ] Phase 3: First-use documentation and diagnostics

## References

- Backlog: `2026-08-08_maketalk-create-output-dirs`
- Backlog: `2026-08-08_mdpeople-missing-image-field`
- CIP-0005: Improve mdpp Error Handling and Validation (overlapping scope — coordinate)
- vibecourse deployment experience (trigger for this CIP)
