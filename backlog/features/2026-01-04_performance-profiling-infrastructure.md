---
id: "2026-01-04_performance-profiling-infrastructure"
title: "Add Performance Profiling Infrastructure"
status: "Proposed"
priority: "Medium"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "feature"
related_cips: ["0009"]
owner: ""
dependencies: []
---

# Task: Add Performance Profiling Infrastructure

## Description

Implement profiling infrastructure for `maketalk` and `makecv` to identify build pipeline bottlenecks. This is Phase 1 of CIP-0009: Further Performance Optimization.

**Current State**: 4x overall speedup (CIP-0008) but 95% of build time is unknown.

**Goal**: Understand where the other 35 seconds are spent in a 37-second build.

## Acceptance Criteria

### Core Profiling Infrastructure
- [ ] Create `lamd/profiler.py` with `BuildProfiler` class
- [ ] Integrate profiler into `lamd/maketalk.py`
- [ ] Integrate profiler into `lamd/makecv.py`
- [ ] Add `--profile` flag to both commands

### Profiling Coverage
- [ ] Measure config loading time
- [ ] Measure git operations time
- [ ] Measure Makefile generation time
- [ ] Measure make execution time (total)
- [ ] Identify top 5 time consumers

### Output Format
- [ ] Clear, readable timing breakdown
- [ ] Percentage of total time per operation
- [ ] Sorted by time (slowest first)
- [ ] Optional JSON output for automation

### Documentation
- [ ] Usage examples in docstrings
- [ ] Add to CIP-0009 as completed
- [ ] Document baseline measurements

## Implementation Notes

### Profiler Design

```python
# lamd/profiler.py
import time
from contextlib import contextmanager
from typing import Dict, Optional

class BuildProfiler:
    """Profile build operations to identify bottlenecks."""
    
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.timings: Dict[str, float] = {}
        self.start_time: Optional[float] = None
    
    def start(self):
        """Start overall timing."""
        self.start_time = time.perf_counter()
    
    @contextmanager
    def measure(self, operation: str):
        """Context manager to measure operation time."""
        if not self.enabled:
            yield
            return
        
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            self.timings[operation] = elapsed
    
    def report(self, format: str = "text"):
        """Generate timing report."""
        if not self.enabled or not self.timings:
            return
        
        total = sum(self.timings.values())
        overall = time.perf_counter() - self.start_time if self.start_time else total
        
        print("\n" + "=" * 60)
        print("Build Performance Profile")
        print("=" * 60)
        
        for op, elapsed in sorted(self.timings.items(), key=lambda x: -x[1]):
            pct = (elapsed / total) * 100 if total > 0 else 0
            print(f"{op:40s}: {elapsed:6.2f}s ({pct:5.1f}%)")
        
        print("-" * 60)
        print(f"{'Total measured':40s}: {total:6.2f}s")
        print(f"{'Overall build time':40s}: {overall:6.2f}s")
        
        if overall > total:
            unmeasured = overall - total
            pct = (unmeasured / overall) * 100
            print(f"{'Unmeasured overhead':40s}: {unmeasured:6.2f}s ({pct:5.1f}%)")
        
        print("=" * 60 + "\n")
```

### Integration Example (maketalk.py)

```python
from lamd.profiler import BuildProfiler

def main() -> int:
    parser = argparse.ArgumentParser(...)
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable performance profiling"
    )
    args = parser.parse_args()
    
    profiler = BuildProfiler(enabled=args.profile)
    profiler.start()
    
    with profiler.measure("Argument Parsing"):
        # Already done above
        pass
    
    with profiler.measure("Config File Loading"):
        if not os.path.exists("_lamd.yml"):
            ...
        iface = Interface.from_file(...)
    
    with profiler.measure("Dependency Git Pulls"):
        for field in ["snippetsdir", "bibdir"]:
            ...
            if os.path.isdir(git_dir):
                os.system(f"cd {answer}; git pull")
    
    with profiler.measure("Makefile Generation"):
        with open("makefile", "w+") as f:
            f.write(...)
    
    with profiler.measure("Make Execution"):
        result = os.system(make_cmd)
    
    profiler.report()
    return result
```

### Expected Output

```
============================================================
Build Performance Profile
============================================================
Make Execution                          :  32.45s ( 87.7%)
Dependency Git Pulls                    :   3.12s (  8.4%)
Config File Loading                     :   1.23s (  3.3%)
Makefile Generation                     :   0.18s (  0.5%)
Argument Parsing                        :   0.02s (  0.1%)
------------------------------------------------------------
Total measured                          :  37.00s
Overall build time                      :  37.02s
Unmeasured overhead                     :   0.02s (  0.1%)
============================================================
```

## Testing Strategy

### Manual Testing
```bash
# Profile a talk build
maketalk my-talk.md --profile

# Profile a CV build
makecv my-cv.md --profile

# Profile different sizes
maketalk small-talk.md --profile
maketalk medium-talk.md --profile
maketalk large-talk.md --profile
```

### Validation
- [ ] Profiler adds <100ms overhead
- [ ] Timings are consistent across runs (±10%)
- [ ] Percentages sum to ~100%
- [ ] Works on both macOS and Linux

## Next Steps After Completion

1. **Run comprehensive benchmarks** on various talk/CV files
2. **Document baseline** in `docs/performance-baseline.md`
3. **Identify quick wins** (operations taking >2s that can be optimized)
4. **Create backlog items** for top 3 optimization opportunities
5. **Update CIP-0009** with findings and recommendations

## Success Metrics

- [ ] Profiling infrastructure works reliably
- [ ] Can identify where 95% of build time is spent
- [ ] Clear path to next optimizations
- [ ] Baseline documented for future comparison

## Related

- **CIP**: 0009 (Further Performance Optimization)
- **CIP**: 0008 (Server Mode - already optimized mdfield)
- **Requirement**: req0005 (Fast Build Operations)

## Progress Updates

### 2026-01-04

Task created as part of CIP-0009 Phase 1. This is the foundation for all future performance optimizations.

