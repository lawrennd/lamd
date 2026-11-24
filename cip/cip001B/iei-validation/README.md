# CIP-001B validation: IEI time-plan forks

Forked excerpts from recent IEI `_lamd/` lectures. Hand-written Clock|Block
tables and stray `\classtimertitled` overlays are reconstructed with
`\sessionstart` / `\sessionlength` / `\timeplan` / `\blocktime`.

| Fork | Source | Pattern |
|------|--------|---------|
| `limits-on-intelligence.fork.md` | Week 8 forward plan | Quiz keeps `{timer}`; other blocks plan-only |
| `good-regulator-goals-channels.fork.md` | Week 7 forward plan | No class test; all plan-only (stray timers removed) |
| `exponential-family-fisher-overviews.fork.md` | Week 6 as-delivered | Irregular durations from SRT; Quiz `{timer}` only |

Run:

```bash
cd /Users/neil/lawrennd/lamd-cip001B
PYTHONPATH=. python3 cip/cip001B/iei-validation/validate_forks.py
```

These forks are CIP research notes, not live IEI curriculum.
