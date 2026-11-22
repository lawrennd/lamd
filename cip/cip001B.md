---
author: "Neil D. Lawrence"
created: "2026-11-22"
id: "001B"
last_updated: "2026-11-22"
status: "Closed"
compressed: false
effort: medium
priority: medium
related_requirements: []
related_cips: ["0012"]
tags:
  - cip
  - lectures
  - timing
  - planning
  - notes
  - slides
  - macros
title: "Lecture time allocation and compiled time plans"
---

# CIP-001B: Lecture time allocation and compiled time plans

> CIPs describe HOW to achieve requirements (WHAT).  
> Related to [CIP-0012](cip0012.md) only insofar as live `\classtimer` / `\classtimertitled` overlays already exist; this CIP is about **planning and compiling allocated block times**, not countdown chrome.

## Status

- [x] Proposed - Initial idea documented
- [x] Accepted - Approved, ready to start work
- [x] In Progress - Actively being implemented
- [x] Implemented - Work complete, awaiting verification
- [x] Closed - Verified and complete
- [ ] Rejected - Will not be implemented
- [ ] Deferred - Postponed

## Summary

Add a LaMD authoring surface for **within-lecture time allocation**: authors mark blocks with a duration (or wall-clock end), and the build **compiles** those marks into a single time-plan table for notes (and optionally a light check that allocations fit the session). Live Reveal countdown timers remain a separate concern; this CIP may optionally *emit* a quiz `\classtimertitled` from a plan entry, but must not conflate pacing plans with interactive timers.

## Motivation

IEI and similar modules already keep a **Clock | Block** table in `\notes{}` and scatter `\classtimertitled{HH:MM}{Label}` for quizzes (and sometimes for every section). That pattern has three problems:

1. **Duplication.** The plan table and the in-body timers drift apart; removing “stray” timers during delivery cleanup also risks deleting the one quiz timer that should stay.
2. **No compile-time check.** Nothing warns when blocks sum past the 110-minute Tuesday slot, or when a “Break” and “Shannon” clock contradict the table.
3. **Wrong tool for the job.** `\classtimer` / `\classtimertitled` are **live countdown overlays** (CIP-0012 Track B chrome). Using them as a substitute for a time plan fills the deck with full-bleed timer slides that were never meant as agenda chrome.

A first-class allocation macro plus a compiled plan keeps speaker notes honest, leaves quiz timers intentional, and gives conveners a single source of truth for “what gets how long.”

## Detailed Description

### Decisions (frozen on accept)

| Decision | Choice |
|----------|--------|
| Macro names | `\sessionstart`, `\sessionlength`, `\blocktime`, `\timeplan` |
| Plan emission | Explicit `\timeplan` anchor only (no auto-insert) |
| Authoring model | Duration-first; wall clocks derived when `\sessionstart` is set |
| Live timers | Opt-in via optional third argument `timer` on `\blocktime` |

### Two concerns (do not merge)

| Concern | Existing today | This CIP |
|---------|----------------|----------|
| **Live countdown** | `\classtimer{10:00}`, `\classtimertitled{10:05}{Quiz 3}` → Reveal iframe | Unchanged; optional generation from a plan row marked `timer` |
| **Allocated plan** | Hand-written markdown tables in `\notes{}` | New macros + compile step → one plan table at `\timeplan` |

### Authoring sketch (v1)

Prefer **duration-first** allocation (portable across term start times), with optional absolute clocks derived from session start:

```markdown
\sessionstart{10:05}
\sessionlength{110}   % minutes; optional if frontmatter / _lamd.yml supplies it

\timeplan

###{Quiz 3}
\blocktime{10}{Quiz 3}{timer}

###{Exponential Family}
\blocktime{20}{Exponential family: θ=-λ; three members; ψ as CGF}

###{Fisher Metric …}
\blocktime{20}{Fisher from score; I≠H; dual charts}

\blocktime{10}{Break}

\blocktime{15}{Shannon capacity}
\blocktime{10}{DPI statement}
\blocktime{20}{Good Regulator overview}
```

Semantics:

- `\blocktime{minutes}{label}` records an allocation; does **not** insert a Reveal timer slide.
- Optional third argument `timer` means: also emit the existing `\classtimertitled` at that point for a live countdown (quiz use-case).
- `\sessionstart` / `\sessionlength` (or YAML equivalents) let the compile step print **Clock | Mins | Block** columns as wall times when wanted.
- `\timeplan` is the sole emission anchor: the compiled table replaces that macro (notes default; slides may emit a short summary or no-op).

Contract: **allocations are data; the plan is compiled at `\timeplan`; live timers are opt-in.**

### Compile behaviour

On `maketalk` / `mdpp` for notes (and optionally slides):

1. Collect `\blocktime` entries in document order (after includes expand).
2. Emit a **Time plan** table at each `\timeplan` (normally one).
3. Warn (non-fatal by default) if `sum(minutes) > sessionlength` or if any block is missing a label.
4. Do **not** require authors to maintain a parallel markdown table.

Derived wall-clock column (when `\sessionstart` is set):

| Clock | Mins | Block |
|------:|-----:|-------|
| 10:05–10:15 | 10 | Quiz 3 |
| … | … | … |

### What this is not

- Not a replacement for VibeCourse `duration_hours` (module contact-hour totals).
- Not automatic speech-to-text “as delivered” reconstruction (IEI’s post-hoc SRT notes stay human).
- Not a requirement that every subsection carry a `\blocktime` — voluntary, but when used, the plan is authoritative.

### Design alternatives (resolved)

1. **YAML frontmatter only** — clean for tooling, awkward next to LaMD section flow.
2. **Duration-only macros in body** — **chosen**; stays beside the material; compile fills the table at `\timeplan`.
3. **Absolute clocks only** — brittle when the slot moves; derived view of (2) is enough for v1.

## Implementation Plan

1. **Macros**
   - Define `\blocktime` / `\sessionstart` / `\sessionlength` / `\timeplan` across notes / slides / null gpp sets.
   - Ensure non-notes formats either no-op or emit a short placeholder (same pattern as classtimer outside slides HTML).

2. **Collection + emission**
   - Implement collection in `mdpp` (or a small post-pass) so includes contribute blocks in order.
   - Emit one markdown/HTML table at `\timeplan`.

3. **Optional timer bridge**
   - `timer` flag → expand to existing `\classtimertitled{HH:MM}{label}` using derived start clock when `\sessionstart` is known; otherwise require an explicit clock argument.

4. **Validation**
   - Advisory overrun warning; optional strict mode later.

5. **Docs + fixtures**
   - Document in `docs/contexts/slides.md` and/or a short lectures/planning note; distinguish clearly from `\classtimer`.
   - Fixture lecture with a few `\blocktime` rows; assert compiled table and “no stray timer slides” unless flagged.

6. **Migration note for IEI**
   - Show how to replace hand tables + quiz-only `\classtimertitled` with `\blocktime{10}{Quiz 3}{timer}` plus unmarked content blocks.

## Backward Compatibility

- Existing `\classtimer` / `\classtimertitled` keep current behaviour.
- Lectures without `\blocktime` are unchanged.
- Hand-written time-plan tables remain valid; authors migrate when ready.
- No change to VibeCourse `duration_hours` semantics.

## Testing Strategy

- Unit/fixture: expand a small markdown fixture through notes HTML and slides HTML; check table content and that unflagged blocks do not create timer iframes.
- Overrun: fixture with sum > `\sessionlength` produces a warning.
- Include order: `\blocktime` inside an `\include` appears in plan order.
- Regression: existing CIP-0012 classtimer fixtures still pass.

## Related Requirements

None linked yet. If a requirements entry is added (e.g. “authors can declare and compile within-lecture time budgets”), set `related_requirements` and link here.

## Implementation Status

- [x] Agree macro names and emission anchor (`\timeplan` explicit)
- [x] Implement gpp macros (notes / slides / null) — `2026-11-22_cip001B-macros`
- [x] Implement collection + table emission in the build path — `2026-11-22_cip001B-collect-emit`
- [x] Advisory sum check — `2026-11-22_cip001B-overrun-warn`
- [x] Optional `timer` → `\classtimertitled` bridge — `2026-11-22_cip001B-timer-bridge`
- [x] Docs + fixtures — `2026-11-22_cip001B-docs-fixtures`
- [x] IEI migration example (optional follow-on in the module repo) — `2026-11-22_cip001B-iei-migration`

## References

- Live timers today: `lamd/macros/talk-macros-slides-html.gpp` (`\classtimer`, `\classtimertitled`); `docs/contexts/slides.md`
- CIP-0012: Reveal backgrounds / content scripts (timers are existing chrome under that testing umbrella)
- Motivating module practice: IEI `_lamd/*.md` “Time plan” notes tables + quiz `\classtimertitled{10:05}{Quiz N}`
- Validation forks: [`cip/cip001B/iei-validation/`](cip001B/iei-validation/) (Weeks 6–8 time plans reconstructed; `validate_forks.py`)

## Progress Updates

### 2026-11-22

Accepted. Frozen: `\sessionstart` / `\sessionlength` / `\blocktime` / `\timeplan`; emission at explicit `\timeplan` only. Backlog tasks created; status → In Progress.

Macros task completed: gpp markers in null / notes / slides-html; fixture tests pass; no timer chrome until the bridge task.

Collect/emit + overrun advisory: `lamd/timeplan.py` post-gpp pass replaces `<!--lamd-timeplan-->` with a Clock|Mins|Block table and warns on overrun / missing labels.

Timer bridge: `timer` flag on `\blocktime` emits CIP-0012 classtimertitled chrome (slides iframe / notes placeholder) at the derived block-start clock; without `\sessionstart`, warns and skips.

Docs + fixtures: slides/notes contexts document allocation vs countdown; fixtures cover include order, overrun warning, and timer opt-in. Status → Implemented (IEI migration remains optional follow-on).

Validated against IEI forks (Weeks 6–8): compiled clocks match original tables; quiz-only `{timer}` emits one iframe; Week 6 as-delivered sum 113>110 triggers overrun advisory. Status → Closed. Live IEI `_lamd/` apply still a teaching edit, not done here.
