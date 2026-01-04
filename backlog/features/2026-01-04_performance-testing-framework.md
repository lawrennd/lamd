---
id: "2026-01-04_performance-testing-framework"
title: "Performance Testing Framework"
status: "Proposed"
priority: "Medium"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "feature"
related_cips: ["0009"]
owner: ""
dependencies: ["2026-01-04_performance-profiling-infrastructure"]
---

# Task: Performance Testing Framework

## Description

Create automated performance testing framework to:
1. Prevent performance regressions
2. Validate optimizations
3. Track performance over time
4. Ensure consistent performance across platforms

**Goal**: Catch performance regressions in CI/CD before they reach users.

## Acceptance Criteria

### Test Infrastructure
- [ ] Create `tests/performance/` directory
- [ ] Implement performance test suite with pytest-benchmark
- [ ] Add fixtures for small/medium/large test files
- [ ] Performance thresholds for each test

### Test Coverage
- [ ] Single talk build performance
- [ ] Single CV build performance
- [ ] Batch builds (multiple talks)
- [ ] Cold start vs warm cache
- [ ] Server mode vs direct mode comparison

### CI/CD Integration
- [ ] Performance tests run in CI
- [ ] Fail build if regression detected
- [ ] Report performance metrics
- [ ] Track performance over time (optional)

### Documentation
- [ ] How to run performance tests
- [ ] How to interpret results
- [ ] How to update thresholds

## Implementation Approach

### Directory Structure

```
tests/
├── performance/
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures
│   ├── test_talk_builds.py   # Talk build performance
│   ├── test_cv_builds.py     # CV build performance
│   ├── test_mdfield.py        # mdfield performance
│   └── fixtures/              # Test markdown files
│       ├── small_talk.md
│       ├── medium_talk.md
│       └── large_talk.md
```

### Performance Tests

```python
# tests/performance/test_talk_builds.py

import pytest
import subprocess
from pathlib import Path
from time import perf_counter

# Performance thresholds (based on CIP-0008/0009 baselines)
THRESHOLDS = {
    "small_talk_server": 10.0,   # Small talk with server mode: <10s
    "medium_talk_server": 40.0,  # Medium talk with server mode: <40s
    "large_talk_server": 60.0,   # Large talk with server mode: <60s
    "small_talk_direct": 30.0,   # Small talk direct mode: <30s
}

@pytest.mark.performance
def test_small_talk_build_server_mode(tmp_path, small_talk_fixture):
    """Test build time for small talk (server mode)."""
    # Setup
    setup_talk_environment(tmp_path, small_talk_fixture)
    
    # Measure
    start = perf_counter()
    result = subprocess.run(
        ["maketalk", "small_talk.md"],
        cwd=tmp_path,
        capture_output=True
    )
    elapsed = perf_counter() - start
    
    # Assert
    assert result.returncode == 0, f"Build failed: {result.stderr}"
    assert elapsed < THRESHOLDS["small_talk_server"], \
        f"Build too slow: {elapsed:.2f}s (threshold: {THRESHOLDS['small_talk_server']}s)"

@pytest.mark.performance
@pytest.mark.benchmark(group="maketalk")
def test_medium_talk_benchmark(benchmark, tmp_path, medium_talk_fixture):
    """Benchmark medium talk build with pytest-benchmark."""
    setup_talk_environment(tmp_path, medium_talk_fixture)
    
    def build_talk():
        subprocess.run(
            ["maketalk", "medium_talk.md"],
            cwd=tmp_path,
            check=True,
            capture_output=True
        )
    
    benchmark(build_talk)

@pytest.mark.performance
def test_server_vs_direct_speedup(tmp_path, medium_talk_fixture):
    """Verify server mode is at least 3x faster than direct mode."""
    setup_talk_environment(tmp_path, medium_talk_fixture)
    
    # Measure direct mode
    start = perf_counter()
    subprocess.run(
        ["maketalk", "medium_talk.md", "--no-server"],
        cwd=tmp_path,
        check=True,
        capture_output=True
    )
    direct_time = perf_counter() - start
    
    # Measure server mode
    start = perf_counter()
    subprocess.run(
        ["maketalk", "medium_talk.md"],
        cwd=tmp_path,
        check=True,
        capture_output=True
    )
    server_time = perf_counter() - start
    
    # Assert speedup
    speedup = direct_time / server_time
    assert speedup >= 3.0, \
        f"Server mode not fast enough: {speedup:.1f}x (expected: ≥3.0x)"
```

### Fixtures

```python
# tests/performance/conftest.py

import pytest
from pathlib import Path

@pytest.fixture
def small_talk_fixture():
    """Small talk (few includes, <100 lines)."""
    return """---
title: "Small Test Talk"
author: Test Author
date: 2026-01-04
---

# Small Talk

A small test talk with minimal content.
"""

@pytest.fixture
def medium_talk_fixture():
    """Medium talk (typical size, several includes)."""
    return """---
title: "Medium Test Talk"
author: Test Author
date: 2026-01-04
layout: talk
---

\\include{_ai/includes/embodiment-factors.md}
\\include{_ai/includes/conversation.md}

# Medium Talk

Typical talk with several includes.
"""

@pytest.fixture
def large_talk_fixture():
    """Large talk (many includes, diagrams, >1000 lines)."""
    # ... large content

def setup_talk_environment(path: Path, content: str):
    """Setup complete talk environment with dependencies."""
    # Create _lamd.yml
    (path / "_lamd.yml").write_text("""
snippetsdir: ../snippets
bibdir: ../bib
diagramsdir: ../diagrams
""")
    
    # Create talk file
    (path / "talk.md").write_text(content)
    
    # Create mock dependencies
    # ...
```

### Running Performance Tests

```bash
# Run all performance tests
pytest tests/performance/ -v

# Run with benchmark report
pytest tests/performance/ --benchmark-only

# Compare against baseline
pytest tests/performance/ --benchmark-compare=baseline

# Skip slow tests in normal CI
pytest tests/ -m "not performance"
```

### CI/CD Integration

```yaml
# .github/workflows/performance.yml

name: Performance Tests

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      
      - name: Run performance tests
        run: |
          poetry run pytest tests/performance/ \
            --benchmark-only \
            --benchmark-json=output.json
      
      - name: Check for regressions
        run: |
          poetry run python scripts/check_performance_regression.py \
            --current output.json \
            --baseline baseline.json \
            --threshold 1.1  # Allow 10% slowdown
```

## Success Metrics

- [ ] Performance tests run reliably in CI
- [ ] Can detect ≥10% performance regressions
- [ ] Tests pass on fresh install (reproducible)
- [ ] Clear error messages when regression detected
- [ ] Benchmarks track improvements from CIP-0009

## Related

- **CIP**: 0009 (Performance Optimization) - Phase 4
- **Dependency**: Profiling infrastructure (establishes baselines)
- **Tools**: pytest-benchmark, pytest markers

## Progress Updates

### 2026-01-04

Task created as part of CIP-0009 Phase 4. Essential for preventing regressions as we optimize.

