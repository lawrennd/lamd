---
id: "2026-01-04_two-stage-cli-phase1"
title: "Create New lamd CLI Utility with talk/cv Subcommands"
status: "Proposed"
priority: "Medium"
created: "2026-01-04"
last_updated: "2026-01-04"
category: "feature"
related_cips: ["0006"]
related_requirements: ["0003"]
owner: ""
dependencies: []
---

# Task: Create New lamd CLI Utility with talk/cv Subcommands

## Description

**Revised Approach**: Instead of modifying `maketalk`/`makecv`, create a new `lamd` CLI utility with modern subcommand architecture. This provides 100% backward compatibility while enabling two-stage workflow and future extensibility.

**New Command Structure:**
```bash
lamd talk [options] file.md        # Build talk (generate + execute)
lamd talk --generate file.md       # Generate interface only
lamd talk --execute file.yml       # Execute from interface
lamd cv [options] file.md          # Build CV (similar options)
```

**Why This Approach is Better:**
- **Zero breaking changes** - `maketalk` and `makecv` remain untouched
- **Modern CLI design** - Subcommands are more scalable and intuitive
- **Clear migration path** - Users can adopt `lamd` when ready
- **Future extensibility** - Easy to add `lamd field`, `lamd list`, `lamd deps`, etc.
- **Two-stage as default** - Modern workflow from the start

## Acceptance Criteria

### New CLI Entry Point
- [ ] Create `lamd/cli.py` as main entry point
- [ ] Implement subcommand dispatcher (using `argparse` or `click`)
- [ ] Configure as `lamd` command in `pyproject.toml`
- [ ] Help text shows available subcommands: `lamd --help`

### Interface Schema Design
- [ ] Extend `lamd.config.interface.Interface` class to include `compute` section
- [ ] Interface YAML format documents:
  - `input`: Source files (markdown, configs, snippets, diagrams)
  - `output`: Target files (HTML, PDF, DOCX, slides, notes)
  - `compute`: Transformation steps (Makefile operations, format conversions)
- [ ] Schema is machine-readable and human-friendly
- [ ] Interface files can be version-controlled and shared

### Implement `lamd talk` Subcommand
- [ ] `lamd talk file.md` - Default: generate interface + execute (backward compatible)
- [ ] `lamd talk --generate file.md` - Generate interface file only
- [ ] `lamd talk --execute file.interface.yml` - Execute from interface file
- [ ] All `maketalk` flags work with `lamd talk` (--format, --to, --profile, --git-cache-minutes, etc.)
- [ ] Generated file named `{basename}.interface.yml`
- [ ] All dependencies are accurately captured
- [ ] Compute steps describe Makefile operations

### Implement `lamd cv` Subcommand
- [ ] `lamd cv file.md` - Default: generate interface + execute
- [ ] `lamd cv --generate file.md` - Generate interface file only
- [ ] `lamd cv --execute file.interface.yml` - Execute from interface file
- [ ] All `makecv` flags work with `lamd cv`
- [ ] Feature parity with `makecv`

### Backward Compatibility (Critical!)
- [ ] `maketalk` command continues working exactly as before
- [ ] `makecv` command continues working exactly as before
- [ ] No changes to existing command-line tools
- [ ] Legacy tools and new `lamd` CLI can coexist
- [ ] No breaking changes for existing users

### Testing
- [ ] Unit tests for interface file generation
- [ ] Unit tests for interface file parsing and validation
- [ ] Integration tests for two-stage workflow (generate → execute)
- [ ] Test with various talk formats (slides, notes, HTML, PDF)
- [ ] Test with various CV formats
- [ ] Performance tests (interface generation overhead < 100ms)
- [ ] Backward compatibility tests

### Documentation
- [ ] Add `--generate-interface` and `--from-interface` to help text
- [ ] Document interface file format with examples
- [ ] Provide workflow integration examples
- [ ] Update README with two-stage workflow use cases

## Implementation Notes

### Technical Approach

**1. New CLI Entry Point (`lamd/cli.py`)**
```python
#!/usr/bin/env python3
"""Main entry point for the lamd CLI utility."""

import argparse
import sys

def main():
    """Main CLI dispatcher."""
    parser = argparse.ArgumentParser(
        prog="lamd",
        description="Lamd content generation toolkit"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # lamd talk subcommand
    talk_parser = subparsers.add_parser("talk", help="Build talk presentations")
    talk_parser.add_argument("file", nargs="?", help="Markdown file to build")
    talk_parser.add_argument("--generate", action="store_true", 
                            help="Generate interface file only")
    talk_parser.add_argument("--execute", metavar="FILE",
                            help="Execute from interface file")
    # ... other maketalk arguments ...
    
    # lamd cv subcommand
    cv_parser = subparsers.add_parser("cv", help="Build CV documents")
    cv_parser.add_argument("file", nargs="?", help="Markdown file to build")
    cv_parser.add_argument("--generate", action="store_true",
                          help="Generate interface file only")
    cv_parser.add_argument("--execute", metavar="FILE",
                          help="Execute from interface file")
    # ... other makecv arguments ...
    
    args = parser.parse_args()
    
    if args.command == "talk":
        from lamd.commands.talk import run_talk
        run_talk(args)
    elif args.command == "cv":
        from lamd.commands.cv import run_cv
        run_cv(args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**2. Extract Common Logic (`lamd/commands/talk.py`)**
```python
"""Implementation of lamd talk subcommand."""

from lamd import maketalk

def run_talk(args):
    """Run the talk subcommand."""
    # Generate-only mode
    if args.generate:
        interface = generate_interface(args.file)
        write_interface_file(interface, f"{base}.interface.yml")
        return
    
    # Execute-from-interface mode
    if args.execute:
        interface = load_interface_file(args.execute)
        validate_inputs(interface)
        execute_from_interface(interface)
        return
    
    # Default: generate + execute (backward compatible)
    interface = generate_interface(args.file)
    execute_from_interface(interface)
```

**3. Schema Design**
Extend existing `lamd.config.interface.Interface`:
```python
interface_data = {
    "input": {
        "markdown": "talk.md",
        "config": ["_lamd.yml", "_config.yml"],
        "snippets": "/path/to/snippets",
        "diagrams": "/path/to/diagrams",
        "bibliography": ["/path/to/bibliography/lawrence.bib"]
    },
    "output": {
        "slides": "talk.slides.html",
        "notes": "talk.notes.html",
        "pdf": "talk.pdf"
    },
    "compute": {
        "type": "makefile",
        "steps": [
            {"target": "talk.slides.html", "dependencies": ["talk.md", "..."]},
            {"target": "talk.notes.html", "dependencies": ["talk.md", "..."]}
        ]
    }
}
```

**4. Configuration in pyproject.toml**
```toml
[project.scripts]
lamd = "lamd.cli:main"
maketalk = "lamd.maketalk:main"  # Unchanged
makecv = "lamd.makecv:main"      # Unchanged
```

**5. Leverage Existing Infrastructure**
- Refactor `maketalk.py` and `makecv.py` to extract reusable logic
- Build on current Makefile generation code
- Use existing `Interface` class for input/config handling
- Reuse dependency scanning from CIP-0009 optimizations
- Maintain compatibility with all existing flags

### Use Cases

**Use Case 1: Basic Usage (Backward Compatible)**
```bash
# New way - same behavior as maketalk
lamd talk my-talk.md

# Old way - still works!
maketalk my-talk.md
```

**Use Case 2: Workflow Documentation**
```bash
# Generate interface to document workflow
lamd talk --generate my-talk.md
# Review my-talk.interface.yml to understand inputs/outputs
# Version control the interface file alongside source
```

**Use Case 3: Reproducible Builds**
```bash
# Generate interface on machine A
lamd talk --generate talk.md

# Transfer interface file to machine B
# Execute from interface (after ensuring inputs exist)
lamd talk --execute talk.interface.yml
```

**Use Case 4: External Workflow Integration**
```bash
# Workflow manager generates interface files
for talk in *.md; do
    lamd talk --generate $talk
done

# Workflow manager orchestrates builds from interfaces
workflow-runner execute *.interface.yml
```

**Use Case 5: Debugging & Auditing**
```bash
# Generate interface to audit what will be built
lamd talk --generate talk.md
# Review interface to verify correct inputs/outputs
# Execute if satisfied
lamd talk --execute talk.interface.yml
```

**Use Case 6: Migration Path**
```bash
# Users can gradually migrate:
# 1. Keep using maketalk (works forever)
maketalk my-talk.md

# 2. Try lamd when ready (same behavior)
lamd talk my-talk.md

# 3. Adopt two-stage workflow when beneficial
lamd talk --generate my-talk.md
lamd talk --execute my-talk.interface.yml
```

### Performance Considerations

- Interface generation should be fast (< 100ms)
- Reuse existing dependency scanning (already optimized in CIP-0009)
- Don't add overhead to default single-stage usage
- Consider caching interface files for repeated builds

### User Feedback Collection (Phase 1 Goal)

After implementation, gather feedback:
- Is the interface file format intuitive?
- Does it improve workflow transparency?
- Is it useful for integration with other tools?
- What additional information would be helpful?
- Should we expand to other utilities?

## Related

- **CIP**: 0006 (Two-Stage Command Line Interface for lamd Utilities)
- **Requirement**: 0003 (Content Workflows Are Transparent and Traceable)
- **Tenets**: explicit-over-implicit, compose-dont-monolith
- **Related Projects**: referia (inspiration for interface pattern)

## Progress Updates

### 2026-01-04 (Initial)

Task created following acceptance of CIP-0006 with phased approach. This is Phase 1: pilot implementation with maketalk/makecv before expanding to other utilities.

### 2026-01-04 (Architectural Revision)

**Major improvement**: Revised approach to create a new `lamd` CLI utility instead of modifying existing tools. This provides:
- **100% backward compatibility** - No changes to `maketalk`/`makecv`
- **Modern CLI architecture** - Subcommand structure (`lamd talk`, `lamd cv`)
- **Clear migration path** - Users adopt `lamd` when ready
- **Future extensibility** - Easy to add more subcommands (`lamd field`, `lamd list`, etc.)

Benefits of this approach:
- Zero risk of breaking existing workflows
- Two-stage workflow can be default for new `lamd` command
- Both old and new commands coexist peacefully
- Users get modern CLI without losing legacy compatibility


