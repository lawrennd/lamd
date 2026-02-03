# Governance and Project Structure (VibeSafe)

LaMD uses the VibeSafe governance structure to keep **principles**, **outcomes**, **design**, and **execution** separated and traceable.

## The layers: WHY → WHAT → HOW → DO

- **WHY (Tenets)**: principles that guide decisions (`tenets/`)
- **WHAT (Requirements)**: desired outcomes (`requirements/`)
- **HOW (CIPs)**: design decisions and plans (`cip/`)
- **DO (Backlog)**: concrete tasks (`backlog/`)

Intended linkage direction:

```
Tenets (WHY) ──informs──> Requirements (WHAT) ──guides──> CIPs (HOW) ──breaks into──> Backlog (DO)
```

## Tenets (current)

Tenets live in `tenets/`:

- `explicit-over-implicit`
- `single-source-multiple-contexts`
- `configuration-lives-with-content`
- `compose-dont-monolith`
- `academic-rigor-through-tooling`
- `documentation-lifecycle` (documentation lifecycle and compression)

## Compression (Closed CIPs → docs)

After a CIP is **Closed**, its stable outcomes should be distilled into these Sphinx/MyST docs, then the CIP should be marked:

- `compressed: true`

The CIP remains the full design/history record.

### Compressed CIPs (governance)

This page compresses the stable outcomes from:

- **CIP-0002**: Systematic Requirements Gathering for LaMD  
  `https://github.com/lawrennd/lamd/blob/main/cip/cip0002.md`
- **CIP-0003**: Establishing Project Tenets for LaMD  
  `https://github.com/lawrennd/lamd/blob/main/cip/cip0003.md`

