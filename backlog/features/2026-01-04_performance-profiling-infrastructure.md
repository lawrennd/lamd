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
- [ ] Add `--profile` flag to maketalk/makecv
- [ ] Profile wrapper overhead (config loading, git pulls, makefile generation)
- [ ] **Profile make execution internals** (where real work happens)
- [ ] Instrument Makefile with timing for each major operation

### Profiling Coverage

**Wrapper Level** (Python):
- [ ] Config file loading time
- [ ] Git operations time
- [ ] Makefile generation time
- [ ] Total make subprocess time

**Makefile Level** (where most time is spent):
- [ ] Each mdfield call (22 calls)
- [ ] Preprocessor (mdpp) execution
- [ ] Dependency scanning
- [ ] Pandoc execution (slides, notes, etc.)
- [ ] File I/O and copying operations
- [ ] Each major make target

### Output Format
- [ ] Hierarchical timing breakdown (wrapper → make → operations)
- [ ] Percentage of total time per operation
- [ ] Sorted by time (slowest first)
- [ ] Clear identification of bottlenecks

### Documentation
- [ ] Usage examples in docstrings
- [ ] Add to CIP-0009 as completed
- [ ] Document baseline measurements

## Implementation Notes

### Multi-Level Profiling Approach

Since most work happens in the generated Makefile, we need **two-level profiling**:

1. **Python wrapper level**: Profile maketalk/makecv overhead
2. **Makefile level**: Profile actual build operations (where 95% of time is)

### Approach 1: Makefile Instrumentation (Recommended)

**Key Insight**: Use make's built-in timing with wrapper script.

```bash
# lamd/scripts/profile-command
#!/bin/bash
# Wrapper to time individual make commands

COMMAND="$@"
START=$(python3 -c "import time; print(time.perf_counter())")

# Execute the command
eval "$COMMAND"
EXIT_CODE=$?

END=$(python3 -c "import time; print(time.perf_counter())")
ELAPSED=$(python3 -c "print($END - $START)")

# Log to profile file
echo "$ELAPSED|$COMMAND" >> /tmp/make_profile_$$.log

exit $EXIT_CODE
```

**Modified Makefile** (when --profile is enabled):

```make
# If profiling enabled, wrap commands
ifdef PROFILE
    TIME_CMD = $(SCRIPTDIR)/profile-command
else
    TIME_CMD =
endif

# Wrap each expensive operation
DATE=$(shell $(TIME_CMD) mdfield date ${BASE}.md)
CATEGORIES=$(shell $(TIME_CMD) mdfield categories ${BASE}.md)

%.notes.html.markdown: %.md ${DEPS}
	$(TIME_CMD) ${PP} $< -o $@ --format notes --to html ...
```

### Approach 2: GNU Time Integration

Use GNU time for detailed profiling:

```bash
# In maketalk.py with --profile flag
if args.profile:
    # Use GNU time to profile make execution
    make_cmd = f"/usr/bin/time -v make {target} 2>&1 | tee make_profile.log"
else:
    make_cmd = f"make {target}"
```

### Approach 3: Make's Built-in Debug Output

Parse make's debug output for timing:

```python
# In maketalk.py
if args.profile:
    import re
    
    # Run make with timing info
    result = subprocess.run(
        ["make", "--debug=basic", target],
        capture_output=True,
        text=True
    )
    
    # Parse output for shell command execution times
    parse_make_timings(result.stderr)
```

### Recommended Hybrid Approach

Combine all three for comprehensive profiling:

```python
# lamd/profiler.py

class BuildProfiler:
    """Two-level profiler: wrapper + makefile operations."""
    
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.wrapper_timings = {}  # Python wrapper timing
        self.make_timings = {}      # Makefile operations
        self.profile_file = f"/tmp/lamd_profile_{os.getpid()}.log"
    
    def enable_makefile_profiling(self):
        """Set environment variable to enable Makefile profiling."""
        os.environ["LAMD_PROFILE"] = "1"
        os.environ["LAMD_PROFILE_FILE"] = self.profile_file
    
    def parse_makefile_profile(self):
        """Parse timing data from Makefile execution."""
        if not os.path.exists(self.profile_file):
            return
        
        with open(self.profile_file) as f:
            for line in f:
                elapsed, command = line.strip().split("|", 1)
                # Categorize command
                category = self._categorize_command(command)
                if category not in self.make_timings:
                    self.make_timings[category] = []
                self.make_timings[category].append(float(elapsed))
    
    def _categorize_command(self, command: str) -> str:
        """Categorize make command for reporting."""
        if "mdfield" in command:
            return "mdfield calls"
        elif "mdpp" in command or "PP" in command:
            return "preprocessor"
        elif "pandoc" in command:
            return "pandoc"
        elif "dependencies" in command:
            return "dependency scanning"
        else:
            return "other make operations"
    
    def report(self):
        """Generate hierarchical timing report."""
        print("\n" + "=" * 70)
        print("Build Performance Profile (Hierarchical)")
        print("=" * 70)
        
        # Wrapper timings
        print("\n📦 Python Wrapper Operations:")
        print("-" * 70)
        for op, elapsed in sorted(self.wrapper_timings.items(), key=lambda x: -x[1]):
            print(f"  {op:50s}: {elapsed:6.2f}s")
        
        # Parse makefile profile
        self.parse_makefile_profile()
        
        # Makefile timings (aggregated by category)
        print("\n🔨 Make Execution (Detailed):")
        print("-" * 70)
        
        total_make_time = 0
        for category, times in sorted(
            self.make_timings.items(),
            key=lambda x: -sum(x[1])
        ):
            total = sum(times)
            count = len(times)
            avg = total / count if count > 0 else 0
            total_make_time += total
            
            print(f"  {category:40s}: {total:6.2f}s ({count:3d} calls, {avg:.3f}s avg)")
        
        # Summary
        wrapper_total = sum(self.wrapper_timings.values())
        overall = wrapper_total + total_make_time
        
        print("\n" + "=" * 70)
        print(f"{'Wrapper overhead':50s}: {wrapper_total:6.2f}s ({wrapper_total/overall*100:5.1f}%)")
        print(f"{'Make execution':50s}: {total_make_time:6.2f}s ({total_make_time/overall*100:5.1f}%)")
        print(f"{'Total build time':50s}: {overall:6.2f}s")
        print("=" * 70 + "\n")
```

### Integration Example (maketalk.py)

```python
from lamd.profiler import BuildProfiler

def main() -> int:
    parser = argparse.ArgumentParser(...)
    parser.add_argument(
        "--profile",
        action="store_true",
        help="Enable detailed performance profiling (wrapper + makefile)"
    )
    args = parser.parse_args()
    
    profiler = BuildProfiler(enabled=args.profile)
    profiler.start()
    
    # Enable Makefile-level profiling (environment variables)
    if args.profile:
        profiler.enable_makefile_profiling()
    
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
            # Add profiling variables to generated Makefile
            if args.profile:
                f.write(f"PROFILE=1\n")
                f.write(f"PROFILE_FILE={profiler.profile_file}\n")
                f.write(f"TIME_CMD={dirname}/scripts/profile-command\n")
            else:
                f.write("TIME_CMD=\n")
            
            # Rest of makefile generation...
            f.write(f"BASE={base}\n")
            f.write(f"include $(MAKEFILESDIR)/make-talk-flags.mk\n")
            # ...
    
    with profiler.measure("Make Execution (total)"):
        # This is where 95% of the time is spent
        # The Makefile will use TIME_CMD to profile individual operations
        result = os.system(make_cmd)
    
    # Parse Makefile profile data and generate hierarchical report
    if args.profile:
        profiler.parse_makefile_profile()
        profiler.report()
        profiler.cleanup()
    
    return result
```

### Makefile Changes

In `make-talk-flags.mk` and other makefiles, wrap expensive operations:

```make
# If TIME_CMD is set (profiling enabled), commands will be timed
# Otherwise TIME_CMD is empty and behaves normally

# Example: Field extraction (22 calls)
DATE=$(shell $(TIME_CMD) $(MDFIELD_CLIENT) date ${BASE}.md)
CATEGORIES=$(shell $(TIME_CMD) $(MDFIELD_CLIENT) categories ${BASE}.md)
# ... etc

# Example: Preprocessing
%.notes.html.markdown: %.md ${DEPS}
	$(TIME_CMD) ${PP} $< -o $@ --format notes --to html ...

# Example: Pandoc
$(BASE).slides.html: $(BASE).slides.html.markdown
	$(TIME_CMD) pandoc -s $(PDSFLAGS) ...
```

**Key insight**: `$(TIME_CMD)` is either empty (normal) or points to `profile-command` script (profiling enabled).

### Expected Output

```
======================================================================
Build Performance Profile (Hierarchical)
talk: ai-and-data-science.md
======================================================================

📦 Python Wrapper Operations:
----------------------------------------------------------------------
  Config File Loading                               :   1.23s
  Dependency Git Pulls                              :   3.12s
  Makefile Generation                               :   0.18s
  Make Execution (total)                            :  32.45s

🔨 Make Execution (Detailed Breakdown):
----------------------------------------------------------------------
  pandoc                                :  18.23s ( 15 calls, 1.215s avg)
  preprocessor (mdpp)                   :  10.12s (  8 calls, 1.265s avg)
  dependency scanning                   :   2.34s (  4 calls, 0.585s avg)
  mdfield calls                         :   1.45s ( 22 calls, 0.066s avg)
  other make operations                 :   0.31s (  7 calls, 0.044s avg)

======================================================================
Wrapper overhead                                  :   4.53s ( 12.2%)
Make execution                                    :  32.45s ( 87.8%)
Total build time                                  :  37.00s
======================================================================

🎯 Top Bottlenecks:
  1. pandoc             : 18.2s (49% of total) - document conversion
  2. preprocessor       : 10.1s (27% of total) - include processing
  3. git pulls          :  3.1s ( 8% of total) - dependency updates
  4. dependency scanning:  2.3s ( 6% of total) - file scanning

💡 Optimization Opportunities:
  - Pandoc: Can we cache or parallelize conversions?
  - Preprocessor: Can we cache preprocessed output?
  - Git pulls: Implement conditional pulls (CIP-0009 Phase 2)
  - mdfield: Already optimized! (was 26s, now 1.5s)
======================================================================
```

This output shows **exactly where the time is going** at both levels:
- Wrapper level (what Python does)
- Makefile level (where the real work happens)

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

