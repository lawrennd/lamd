---
id: "2026-01-04_optimize-dependency-scanning"
title: "Optimize Dependency Scanning Performance"
status: "Proposed"
priority: "High"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "feature"
related_cips: ["0009"]
owner: ""
dependencies: ["2026-01-04_performance-profiling-infrastructure"]
---

# Task: Optimize Dependency Scanning Performance

## Description

Profiling revealed that dependency scanning is the **#1 bottleneck** in lamd builds, accounting for **61.2% of total build time** (28s out of 45.7s).

**Current Performance**:
- 19 calls to `dependencies` command
- Average: 1.47s per call
- Total: 28.0s (61.2% of build time)

**Problem**: Each call re-reads and recursively processes all files from scratch.

## Root Cause Analysis

### Investigation Findings

The `dependencies` command (`lamd/dependencies.py`) calls lynguine functions that:

1. **Read files multiple times**:
   - `extract_inputs()` recursively reads main file + all includes
   - `extract_diagrams()` calls `extract_inputs()` then reads all files again
   - Each dependency type (inputs, diagrams, texdiagrams, docxdiagrams, etc.) repeats this

2. **No caching**:
   - Every `dependencies` call starts from scratch
   - Files are re-read and re-parsed repeatedly
   - Recursive includes are processed every time

3. **Multiple Makefile calls**:
   ```make
   # make-talk-flags.mk calls dependencies 6 times:
   DEPS=$(shell dependencies inputs ...)           # reads all files
   DIAGDEPS=$(shell dependencies diagrams ...)     # reads all files again
   DOCXDEPS=$(shell dependencies docxdiagrams ...) # reads all files again
   PPTXDEPS=$(shell dependencies docxdiagrams ...) # reads all files again
   TEXDEPS=$(shell dependencies texdiagrams ...)   # reads all files again
   DYNAMIC_DEPS=$(shell dependencies all ...)      # reads all files again
   ```

4. **Recursive file processing**:
   ```python
   # lynguine/util/talk.py:107
   for i, filename in enumerate(filenames):
       if os.path.exists(filename):
           # Recursive call for each included file
           list_files[i+1:i+1] = extract_inputs(filename, snippets_path)
   ```

### Performance Impact

**Example**: ai-and-data-science.md
- Main file + ~50 included snippets
- Each snippet may include other snippets (2-3 levels deep)
- Total files processed: ~100-150 files
- **Each of the 6 dependency calls processes all 100-150 files**
- **Result: 600-900 file reads + parsing operations**

## Proposed Solutions

### Option A: Batch Dependency Extraction (Quick Win)

Create a single command that extracts all dependency types in one pass.

```python
# lamd/dependencies.py - new function
def extract_all_types(filename, snippets_path, diagrams_dir):
    """Extract all dependency types in one pass."""
    # Read files once
    all_inputs = nt.extract_inputs(filename, snippets_path)
    
    # Use cached file data to extract diagrams
    all_diagrams = extract_diagrams_from_cache(all_inputs)
    
    return {
        'inputs': all_inputs,
        'diagrams': all_diagrams['all'],
        'slidediagrams': all_diagrams['svg'],
        'texdiagrams': all_diagrams['pdf'],
        'docxdiagrams': all_diagrams['emf'],
    }
```

**Makefile usage**:
```make
# Extract all dependencies in one call, output as JSON
DEPS_JSON=$(shell dependencies batch ${BASE}.md --format json)

# Parse JSON to get individual variables
DEPS=$(shell echo $(DEPS_JSON) | jq -r '.inputs | join(" ")')
DIAGDEPS=$(shell echo $(DEPS_JSON) | jq -r '.diagrams | join(" ")')
```

**Expected savings**: 28s → 5-7s (4-5x improvement)

### Option B: File-based Caching

Cache dependency results to a temporary file.

```python
# Cache results to .deps_cache
import json
import hashlib

cache_file = f".{BASE}.deps_cache"
file_hash = hashlib.md5(open(filename, 'rb').read()).hexdigest()

if os.path.exists(cache_file):
    cache = json.load(open(cache_file))
    if cache['hash'] == file_hash:
        return cache['deps']  # Use cached results

# ... extract dependencies ...
json.dump({'hash': file_hash, 'deps': results}, open(cache_file, 'w'))
```

**Expected savings**: 28s → 1-2s (first run), 0.1s (cached runs)

### Option C: Lynguine Server Mode for Dependencies (Best Long-term)

Extend the lynguine server to maintain parsed file data in memory.

```python
# New endpoint in lynguine server
@app.post("/api/dependencies/batch")
async def extract_dependencies_batch(request: Dict):
    """Extract all dependency types using server-side cache."""
    filename = request['filename']
    
    # Server maintains parse cache in memory
    if filename in parse_cache:
        parsed_data = parse_cache[filename]
    else:
        parsed_data = parse_file_and_includes(filename)
        parse_cache[filename] = parsed_data
    
    return extract_all_deps_from_parsed(parsed_data)
```

**Expected savings**: 28s → 0.5-1s (14-28x improvement)

### Option D: Makefile-level Optimization (Immediate Quick Win)

Reduce redundant calls by reusing variables.

```make
# Instead of calling dependencies multiple times:
# Current (6 calls):
DEPS=$(shell dependencies inputs ...)
DIAGDEPS=$(shell dependencies diagrams ...)

# Optimized (1 call):
ALL_DEPS=$(shell dependencies all ... --include-types)
DEPS=$(filter %.md, $(ALL_DEPS))
DIAGDEPS=$(filter %.svg %.png, $(ALL_DEPS))
```

**Expected savings**: 28s → 8-10s (3x improvement)

## Recommended Approach

**Phase 1: Quick Win** (1-2 hours)
- Option D: Makefile-level optimization
- Expected: 28s → 8-10s (save 18-20s)

**Phase 2: Batch Extraction** (4-6 hours)
- Option A: Single batch command
- Expected: 8-10s → 3-5s (save additional 5-7s)

**Phase 3: Server Mode** (8-12 hours, if worthwhile)
- Option C: Lynguine server integration
- Expected: 3-5s → 0.5-1s (save additional 2-4s)

**Total Potential Savings**: 28s → 0.5-1s (28-56x improvement)

## Acceptance Criteria

### Phase 1 (Quick Win)
- [ ] Reduce redundant dependency calls in Makefiles
- [ ] Profile shows dependency scanning < 10s
- [ ] All existing builds still work correctly

### Phase 2 (Batch Extraction)
- [ ] Implement `dependencies batch` command
- [ ] Update Makefiles to use batch extraction
- [ ] Profile shows dependency scanning < 5s

### Phase 3 (Server Mode - Optional)
- [ ] Implement lynguine server dependencies endpoint
- [ ] Add caching for parsed file data
- [ ] Update lamd to use server mode for dependencies
- [ ] Profile shows dependency scanning < 1s

## Testing Strategy

```bash
# Benchmark current performance
time dependencies inputs ai-and-data-science.md
time dependencies diagrams ai-and-data-science.md
# ... repeat for all types

# Benchmark optimized version
time dependencies batch ai-and-data-science.md --format json

# Full build test
cd ~/lawrennd/talks/_ai
maketalk ai-and-data-science.md --profile

# Expected before: dependency scanning ~28s
# Expected after Phase 1: dependency scanning ~8-10s  
# Expected after Phase 2: dependency scanning ~3-5s
```

## Success Metrics

- [ ] Dependency scanning time reduced by 70%+ (Phase 1)
- [ ] Dependency scanning time reduced by 85%+ (Phase 2)
- [ ] No regressions in build correctness
- [ ] All existing talks build successfully

## Related

- **CIP**: 0009 (Further Performance Optimization) - Phase 2
- **Requirement**: req0005 (Fast Build Operations)
- **Impact**: **Highest priority** - addresses 61% of build time

## Progress Updates

### 2026-01-04

Task created after Phase 1 profiling revealed dependency scanning as the primary bottleneck (28s, 61.2% of total build time).

Root cause identified:
- No caching between calls
- Redundant file I/O
- Recursive processing repeated for each dependency type
- 6 separate Makefile calls each doing full processing

