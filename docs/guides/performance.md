# Build Performance (Server Mode, Batching, Git Cache)

LaMD build performance is driven primarily by minimizing repeated subprocess startup and repeated scanning work in Makefile-driven pipelines.

## Quick start

- **Default builds** use the standard toolchain (`maketalk`, `makecv`, Makefiles, `pandoc`, `gpp`).
- **Fast paths** are available via server mode and batching optimizations where appropriate.

## Server mode

Some LaMD workflows can use a long-running backend service (via `lynguine`) to avoid repeated initialization costs.

### `mdfield` server-mode integration

`mdfield` supports server mode via flags/environment variables (see tool help and repo notes). This reduces repeated in-process initialization work, but the biggest speedup comes from reducing repeated Python subprocess startup costs (see next section).

### Shell client for fast metadata extraction

For Makefile-heavy workflows that call `mdfield` many times, a lightweight shell client can be used (via generated Makefile configuration) to avoid paying Python interpreter startup repeatedly.

If you encounter `curl`/`jq` dependency errors, install those OS tools and retry.

## Batching

Two major batching optimizations exist in the build pipeline:

- **`dependencies batch`**: extracts multiple dependency types in one pass (instead of repeated scans)
- **`mdfield batch`**: extracts many fields in one call (instead of many sequential calls)

These reduce redundant parsing/scanning and can significantly improve build times for talks/CVs with many includes.

## Git update caching

Builds sometimes consult git repositories for dependency updates (snippets, bibliographies, etc.). To avoid contacting remotes on every build, LaMD uses a caching strategy so repeated builds don’t repeatedly pay remote-check overhead.

## Compressed CIPs

This page compresses the stable outcomes from:

- **CIP-0008**: Integrate Lynguine Server Mode for Fast Builds  
  (`https://github.com/lawrennd/lamd/blob/main/cip/cip0008.md`)
- **CIP-0009**: Further Performance Optimization: Close the Gap  
  (`https://github.com/lawrennd/lamd/blob/main/cip/cip0009.md`)

The CIPs contain the full chronology, benchmarks, and rationale; this page is the “current user-facing truth”.

