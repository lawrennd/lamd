# CIP-000E Scoping Results

**Status**: In progress — to be populated during Phase 0 experimentation

## Method

Fresh clone of vibecourse (or equivalent course repo), following student installation steps, running all lamd utilities against representative course content.

## Failure Inventory

| Command | Error / Symptom | Category | Root Cause | Proposed Fix |
|---|---|---|---|---|
| `maketalk` | Fails if `_lectures/`, `slides/` etc. don't exist | Crash | No `mkdir -p` before writing output | Auto-create directories |
| `mdpeople` | `KeyError: 'image'` on sparse `people.yml` entries | Crash | No `.get()` / default for optional fields | Use `.get()` with sensible defaults |
| *(to be filled in during Phase 0)* | | | | |

## Summary Statistics

- Crashes: 2 (known) + TBD
- Silent failures: TBD
- Confusing errors: TBD
- Dependency gaps: TBD

## Notes

Add observations here as the experiment runs.
