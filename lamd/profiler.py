"""
Build performance profiler for lamd.

Part of CIP-0009 Phase 1: Performance Profiling Infrastructure

This module provides two-level profiling:
1. Python wrapper level: config loading, git operations, makefile generation
2. Makefile level: actual build operations (pandoc, mdpp, mdfield, etc.)
"""

import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional


class BuildProfiler:
    """Two-level profiler for lamd builds: wrapper + makefile operations."""
    
    def __init__(self, enabled: bool = False):
        """
        Initialize the build profiler.
        
        Args:
            enabled: Whether profiling is enabled
        """
        self.enabled = enabled
        self.wrapper_timings: Dict[str, float] = {}  # Python wrapper timing
        self.make_timings: Dict[str, List[float]] = {}  # Makefile operations (aggregated)
        self.start_time: Optional[float] = None
        
        # Create unique profile file for this build
        if self.enabled:
            self.profile_file = f"/tmp/lamd_profile_{os.getpid()}.log"
        else:
            self.profile_file = None
    
    def start(self):
        """Start overall build timing."""
        if self.enabled:
            self.start_time = time.perf_counter()
    
    @contextmanager
    def measure(self, operation: str):
        """
        Context manager to measure operation time at wrapper level.
        
        Args:
            operation: Name of the operation being measured
            
        Example:
            with profiler.measure("Config loading"):
                iface = Interface.from_file(...)
        """
        if not self.enabled:
            yield
            return
        
        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            self.wrapper_timings[operation] = elapsed
    
    def enable_makefile_profiling(self):
        """
        Enable Makefile-level profiling by setting environment variables.
        
        This sets:
        - LAMD_PROFILE=1: Signals to Makefiles that profiling is enabled
        - LAMD_PROFILE_FILE: Path to the profile log file
        """
        if self.enabled and self.profile_file:
            os.environ["LAMD_PROFILE"] = "1"
            os.environ["LAMD_PROFILE_FILE"] = self.profile_file
    
    def parse_makefile_profile(self):
        """
        Parse timing data from Makefile execution.
        
        Reads the profile file written by profile-command script and
        categorizes operations for reporting.
        """
        if not self.enabled or not self.profile_file:
            return
        
        profile_path = Path(self.profile_file)
        if not profile_path.exists():
            return
        
        try:
            with open(profile_path) as f:
                for line in f:
                    line = line.strip()
                    if not line or '|' not in line:
                        continue
                    
                    elapsed_str, command = line.split("|", 1)
                    try:
                        elapsed = float(elapsed_str)
                    except ValueError:
                        continue
                    
                    # Categorize command
                    category = self._categorize_command(command)
                    if category not in self.make_timings:
                        self.make_timings[category] = []
                    self.make_timings[category].append(elapsed)
        except IOError as e:
            print(f"Warning: Could not read profile file: {e}")
    
    def _categorize_command(self, command: str) -> str:
        """
        Categorize a make command for reporting.
        
        Args:
            command: The command string
            
        Returns:
            Category name for aggregation
        """
        cmd_lower = command.lower()
        
        if "mdfield" in cmd_lower:
            return "mdfield calls"
        elif "mdlist" in cmd_lower:
            return "mdlist calls"
        elif "mdpp" in cmd_lower or "${pp}" in cmd_lower:
            return "preprocessor (mdpp)"
        elif "pandoc" in cmd_lower:
            return "pandoc"
        elif "dependencies" in cmd_lower:
            return "dependency scanning"
        elif "git" in cmd_lower:
            return "git operations"
        else:
            return "other make operations"
    
    def report(self):
        """
        Generate hierarchical timing report.
        
        Shows:
        1. Python wrapper operations
        2. Makefile operations (aggregated by category)
        3. Summary and bottleneck identification
        """
        if not self.enabled:
            return
        
        # Parse makefile profile data
        self.parse_makefile_profile()
        
        print("\n" + "=" * 70)
        print("Build Performance Profile (Hierarchical)")
        print("=" * 70)
        
        # Python wrapper timings
        if self.wrapper_timings:
            print("\n📦 Python Wrapper Operations:")
            print("-" * 70)
            for op, elapsed in sorted(self.wrapper_timings.items(), key=lambda x: -x[1]):
                print(f"  {op:50s}: {elapsed:6.2f}s")
        
        # Makefile timings (aggregated by category)
        if self.make_timings:
            print("\n🔨 Make Execution (Detailed Breakdown):")
            print("-" * 70)
            
            # Calculate totals and sort by total time
            category_stats = []
            for category, times in self.make_timings.items():
                total = sum(times)
                count = len(times)
                avg = total / count if count > 0 else 0
                category_stats.append((category, total, count, avg))
            
            category_stats.sort(key=lambda x: -x[1])  # Sort by total time
            
            for category, total, count, avg in category_stats:
                print(f"  {category:40s}: {total:6.2f}s ({count:3d} calls, {avg:.3f}s avg)")
        
        # Summary
        wrapper_total = sum(self.wrapper_timings.values())
        make_total = sum(sum(times) for times in self.make_timings.values())
        overall = time.perf_counter() - self.start_time if self.start_time else wrapper_total + make_total
        
        print("\n" + "=" * 70)
        if wrapper_total > 0:
            print(f"{'Wrapper overhead':50s}: {wrapper_total:6.2f}s ({wrapper_total/overall*100:5.1f}%)")
        if make_total > 0:
            print(f"{'Make execution':50s}: {make_total:6.2f}s ({make_total/overall*100:5.1f}%)")
        print(f"{'Total build time':50s}: {overall:6.2f}s")
        print("=" * 70)
        
        # Identify bottlenecks
        if self.make_timings:
            print("\n🎯 Top Bottlenecks:")
            bottlenecks = [(cat, sum(times)) for cat, times in self.make_timings.items()]
            bottlenecks.sort(key=lambda x: -x[1])
            
            for i, (category, total) in enumerate(bottlenecks[:5], 1):
                pct = (total / overall) * 100 if overall > 0 else 0
                print(f"  {i}. {category:30s}: {total:5.1f}s ({pct:4.1f}% of total)")
        
        print("=" * 70 + "\n")
    
    def cleanup(self):
        """Clean up temporary profile file."""
        if self.enabled and self.profile_file:
            profile_path = Path(self.profile_file)
            if profile_path.exists():
                try:
                    profile_path.unlink()
                except OSError:
                    pass  # Ignore cleanup errors

