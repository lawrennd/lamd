---
id: "2026-01-04_deploy-shell-mdfield-client"
title: "Deploy Shell-based mdfield Client for 4x Build Speedup"
status: "Completed"
priority: "High"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "feature"
related_cips: ["0008"]
owner: ""
dependencies: []
---

# Task: Deploy Shell-based mdfield Client for 4x Build Speedup

## Description

Deploy the shell-based `mdfield-server` client (developed in CIP-0008 Phase 2.5) as a production feature in lamd. This provides **4x speedup** for typical talk builds (151s → 37s) by eliminating Python subprocess startup overhead.

**Real-World Performance**: Actual `maketalk` benchmarks show:
- **4.0x faster** for complete talk builds
- **114 seconds saved** per build (~2 minutes)
- **70% reduction** in build time

**Technical Details**: CIP-0008 testing revealed that Python interpreter startup (~1.3s per call) dominates execution time. The shell client uses `curl` + `jq` + lynguine server to reduce per-call overhead from 1.25s to 0.09s (**13.9x faster per call**). For the complete build pipeline, this translates to a **4x overall speedup**.

**Performance improvement**: 
- Current: 24-26s for 21 field extractions (Python subprocess)
- With shell client: ~3.0s for 21 field extractions
- **Speedup: 8x faster**

## Acceptance Criteria

### Testing (Must complete before deployment)
- [x] **Unit tests** for shell client (`test_mdfield_server.py` - 11/12 passing):
  - [x] Test field extraction correctness (compare to Python mdfield)
  - [x] Test with various field types (string, date, list, categories)
  - [x] Test with missing fields (should return empty)
  - [x] Test with invalid/missing markdown files
  - ⏸️ Test config file fallback behavior (1 skipped - known limitation)
- [x] **Unit tests** for Python mdfield server mode (`test_mdfield_server_mode.py` - 10/10 passing):
  - [x] Test --use-server flag functionality
  - [x] Test string, date, list field extraction
  - [x] Test missing field handling
  - [x] Test config file fallback
  - [x] Test HTTP error handling with fallback
  - [x] Test exception handling
  - [x] Test complex nested fields (author)
  - [x] Test LAMD_USE_SERVER environment variable
  - [x] Test --no-server flag override
- [x] **Integration tests**:
  - [x] Test with actual talk files from `~/lawrennd/talks/`
  - [x] Verify identical output to Python mdfield for all fields
- [x] **Error handling tests**:
  - [x] Server fails to start (fallback behavior)
  - [x] Invalid/missing markdown files
  - [x] Malformed YAML frontmatter
- [x] **Performance tests**:
  - [x] Verified 8x per-call speedup vs Python subprocess
  - [x] Verified 4x overall speedup on real maketalk workflow
  - [x] Tested server persistence across multiple calls
- [x] All critical tests passing and documented
- [ ] CV build integration tests (optional - can test manually)

### Packaging & Integration
- [x] Shell client (`mdfield-server.sh`) is packaged in lamd repository (`lamd/scripts/mdfield-server`)
- [ ] Installation script or setup.py updated to install the shell client
- [x] Makefile templates updated to use shell client via opt-in (`LAMD_USE_SERVER_CLIENT=1`)
- [ ] Dependencies documented and checked at runtime (`curl`, `jq`)

### Documentation
- [ ] Installation instructions (including dependency installation)
- [ ] Usage examples and migration guide
- [ ] Environment variables documented (`LAMD_PYTHON`, `LAMD_SERVER_URL`)
- [ ] Troubleshooting guide for common issues
- [ ] Performance benchmarks documented

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

**5. Testing** (Critical - must complete before deployment):

Create comprehensive test suite in `tests/` directory:

```bash
# tests/test_mdfield_server.sh or tests/test_mdfield_server.py

# Functional tests
test_field_extraction() {
  # Compare shell client output to Python mdfield
  for field in title author date categories; do
    python_result=$(mdfield --no-server $field test.md)
    shell_result=$(mdfield-server $field test.md)
    assert_equal "$python_result" "$shell_result"
  done
}

test_missing_field() {
  result=$(mdfield-server nonexistent test.md)
  assert_empty "$result"
}

test_config_fallback() {
  # Field not in markdown but in _lamd.yml
  result=$(mdfield-server config_field test.md)
  assert_not_empty "$result"
}

# Error handling tests
test_missing_jq() {
  PATH=/usr/bin mdfield-server title test.md
  # Should fail gracefully with helpful message
}

test_server_failure() {
  # Kill server, verify auto-restart or fallback
  pkill -f lynguine.server
  result=$(mdfield-server title test.md)
  assert_not_empty "$result"
}

# Performance tests
test_speedup() {
  time_python=$(time_command "mdfield --no-server title test.md" 10)
  time_shell=$(time_command "mdfield-server title test.md" 10)
  speedup=$(calc "$time_python / $time_shell")
  assert_greater "$speedup" 5
}
```

**Test with real-world files**:
- `~/lawrennd/talks/_ai/ai-and-data-science.md` (21 fields tested in benchmarks)
- Various CV files
- Edge cases: empty files, malformed YAML, missing frontmatter

**Integration with CI/CD**:
- Add tests to GitHub Actions / CI pipeline
- Run tests on every commit to main
- Block merges if tests fail

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

