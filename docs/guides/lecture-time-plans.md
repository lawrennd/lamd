# Lecture Time Plans (Compiled Allocations)

Authors declare **how long each block should take**. The build compiles those
marks into one plan table. Live Reveal countdown timers stay a separate,
opt-in concern.

## Two concerns (do not merge)

| Concern | Macros | Behaviour |
|---------|--------|-----------|
| **Allocated plan** | `\sessionstart`, `\sessionlength`, `\blocktime`, `\timeplan` | Compiles a Clock\|Mins\|Block (or Mins\|Block) table at `\timeplan` |
| **Live countdown** | `\classtimer`, `\classtimertitled` | Full-bleed Reveal iframe (slides HTML); short placeholder in notes |

Do **not** use classtimer overlays as an agenda. Put durations next to the
material; emit the plan once at `\timeplan`.

## Authoring

```markdown
\sessionstart{10:05}
\sessionlength{110}

\timeplan

\subsection{Quiz 3}
\blocktime{10}{Quiz 3}{timer}

###{Exponential family}
\blocktime{20}{Exponential family}

\blocktime{10}{Break}
```

| Macro | Role |
|-------|------|
| `\sessionstart{HH:MM}` | Optional wall-clock origin for the Clock column |
| `\sessionlength{minutes}` | Optional budget; advisory warning if allocations overrun |
| `\blocktime{mins}{label}` | Allocation only — no timer slide |
| `\blocktime{mins}{label}{timer}` | Same, plus CIP-0012 `\classtimertitled` at the **block start** clock |
| `\timeplan` | **Only** emission anchor for the compiled table |

Contract: allocations are data; the plan appears only where you put
`\timeplan`; live timers are opt-in via `{timer}`.

## Compile behaviour

After gpp expands includes, `mdpp` collects markers in document order and:

1. Replaces each `\timeplan` with a markdown table (clock ranges when
   `\sessionstart` is set).
2. Warns (non-fatal) if `sum(minutes) > sessionlength` or a block lacks a label.
3. For `{timer}` rows: emits classtimertitled chrome (slides iframe / notes
   placeholder) at the derived start clock. Without `\sessionstart`, warns and
   skips the overlay.

Unflagged `\blocktime` rows never create timer iframes.

## Migration pattern

Replace a hand-written Clock\|Block notes table and scattered
`\classtimertitled{HH:MM}{Label}` overlays with:

- one `\sessionstart` / `\sessionlength` / `\timeplan` near the top
- `\blocktime{…}{…}` beside each section
- `{timer}` only on the quiz (or other intentional countdown)

Worked IEI forks used for validation live under
`cip/cip001B/iei-validation/` (research notes; not live curriculum).

## Macro reference elsewhere

- Slides context: live timers and the allocation sketch — {doc}`../contexts/slides`
- Notes context: plan-first authoring — {doc}`../contexts/notes`

## Compressed CIP

This page compresses the stable outcomes from:

- **CIP-001B**: Lecture time allocation and compiled time plans  
  (`https://github.com/lawrennd/lamd/blob/main/cip/cip001B.md`)

The CIP holds design rationale, implementation chronology, and IEI
validation notes; this page is the current user-facing truth.
