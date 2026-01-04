---
id: "2026-01-04_deploy-shell-mdfield-client"
title: "Deploy Shell-based mdfield Client for 8x Speedup"
status: "Proposed"
priority: "High"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "feature"
related_cips: ["0008"]
owner: ""
dependencies: []
---

# Task: Deploy Shell-based mdfield Client for 8x Speedup

## Description

Deploy the shell-based `mdfield-server` client (developed in CIP-0008 Phase 2.5) as a drop-in replacement for Python `mdfield` in lamd Makefiles. This provides **8-14x speedup** for field extraction operations by eliminating Python subprocess startup overhead.

**Context**: CIP-0008 performance testing revealed that Python interpreter startup (~1.3s per call) dominates execution time. A shell-based client using `curl` + `jq` + lynguine server reduces per-call overhead from 1.25s to 0.09s (**13.9x faster per call**).

**Performance improvement**: 
- Current: 24-26s for 21 field extractions (Python subprocess)
- With shell client: ~3.0s for 21 field extractions
- **Speedup: 8x faster**

## Acceptance Criteria

- [ ] Shell client (`mdfield-server.sh`) is packaged in lamd repository
- [ ] Installation script or setup.py updated to install the shell client
- [ ] Makefile templates updated to use shell client by default (or via opt-in)
- [ ] Dependencies documented (`curl`, `jq`)
- [ ] Integration tested with:
  - [ ] Talk builds (`~/lawrennd/talks/_ai/`)
  - [ ] CV builds (if applicable)
  - [ ] Different markdown file formats
- [ ] Performance verified (≥5x speedup vs current Python subprocess approach)
- [ ] Documentation updated:
  - [ ] Installation instructions
  - [ ] Usage examples
  - [ ] Environment variables (`LAMD_PYTHON`, `LAMD_SERVER_URL`)
- [ ] Fallback behavior tested (what happens if `jq` not installed, server fails, etc.)

## Implementation Notes

### Current State

Shell client (`mdfield-server.sh`) exists as test artifact in `~/lawrennd/talks/_ai/`:
- ✅ Fully functional
- ✅ Auto-starts lynguine server
- ✅ Handles errors gracefully
- ✅ Benchmarked: 8x speedup confirmed

### Tasks

**1. Package in lamd**:
```bash
# Move from test location to lamd
cp ~/lawrennd/talks/_ai/mdfield-server.sh lamd/scripts/mdfield-server
chmod +x lamd/scripts/mdfield-server

# Update setup.py
# Add to scripts=['lamd/scripts/mdfield-server'] or similar
```

**2. Makefile Integration** (choose approach):

**Option A** (Easiest - Alias):
```make
# Add at top of Makefile:
MDFIELD = mdfield-server

# Existing calls work unchanged:
TITLE = $(shell $(MDFIELD) title talk.md)
```

**Option B** (Explicit):
```make
# Replace each call:
TITLE = $(shell mdfield-server title talk.md)
```

**Option C** (Conditional - for testing):
```make
# Allow opt-in/opt-out:
USE_SERVER_CLIENT ?= 1
ifeq ($(USE_SERVER_CLIENT),1)
  MDFIELD = mdfield-server
else
  MDFIELD = mdfield
endif
```

**3. Dependencies**:
- `curl`: Standard on macOS/Linux
- `jq`: Needs installation
  - macOS: `brew install jq`
  - Linux: `apt-get install jq` or `yum install jq`
- Check at runtime and provide helpful error if missing

**4. Environment Setup**:
Document optional environment variables:
- `LAMD_PYTHON`: Python interpreter for server startup (default: `/opt/anaconda3/envs/py311/bin/python`)
- `LAMD_SERVER_URL`: Server URL (default: `http://127.0.0.1:8765`)

**5. Testing**:
- Test with various markdown files (talks, CVs, papers)
- Test error cases (missing file, invalid field, server failure)
- Verify fallback behavior
- Benchmark to confirm ≥5x speedup

### Rollback Plan

If issues arise:
1. Set `MDFIELD = mdfield` (revert to Python client)
2. No data loss or workflow disruption
3. Shell client remains available for opt-in use

### Dependencies on Other Work

- ✅ CIP-0008 Phase 1: lamd infrastructure (complete)
- ✅ CIP-0008 Phase 1b: lynguine server endpoints (complete)
- ✅ CIP-0008 Phase 2: Python mdfield server mode (complete)
- ✅ CIP-0008 Phase 2.5: Shell client implementation (complete)
- ⏳ This task: Deployment and integration

## Related

- **CIP**: CIP-0008 (Integrate Lynguine Server Mode for Fast Builds)
- **Requirement**: REQ-0005 (Build Operations Complete in Reasonable Time)

## Progress Updates

### 2026-01-04

Task created. Shell client fully implemented and tested as part of CIP-0008 Phase 2.5. Ready for deployment.

**Benchmark results** (from CIP-0008):
- Per-call: 0.09s (vs 1.25s Python subprocess)
- For 21 calls: 3.0s (vs 24-26s Python subprocess)
- **13.9x faster per call, 8x faster overall**

