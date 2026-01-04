---
id: "2026-01-04_two-stage-cli-phase1"
title: "Implement Two-Stage CLI Interface (Phase 1: maketalk/makecv)"
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

# Task: Implement Two-Stage CLI Interface (Phase 1: maketalk/makecv)

## Description

Implement Phase 1 of CIP-0006: Add two-stage workflow support to `maketalk` and `makecv` utilities as a pilot program. This enables workflow transparency and integration with external workflow managers while gathering user feedback before expanding to other utilities.

**Two-Stage Process:**
1. **Stage 1 (Interface Generation)**: `maketalk --generate-interface talk.md` creates an interface file documenting inputs, outputs, and computations
2. **Stage 2 (Execution)**: `maketalk --from-interface talk.interface.yml` executes the build from the interface file

**Why Phase 1 with maketalk/makecv?**
- These utilities already generate Makefiles (similar concept to interface files)
- They have complex workflows with many inputs (markdown, configs, snippets, diagrams)
- They're frequently used, so we'll get good feedback
- They benefit most from reproducibility and workflow integration

## Acceptance Criteria

### Interface Schema Design
- [ ] Extend `lamd.config.interface.Interface` class to include `compute` section
- [ ] Interface YAML format documents:
  - `input`: Source files (markdown, configs, snippets, diagrams)
  - `output`: Target files (HTML, PDF, DOCX, slides, notes)
  - `compute`: Transformation steps (Makefile operations, format conversions)
- [ ] Schema is machine-readable and human-friendly
- [ ] Interface files can be version-controlled and shared

### Implementation: --generate-interface Flag
- [ ] Add `--generate-interface` flag to `maketalk.py`
- [ ] Add `--generate-interface` flag to `makecv.py`
- [ ] Flag generates interface file without executing build
- [ ] Generated file named `{basename}.interface.yml`
- [ ] All dependencies are accurately captured (git repos, snippets, diagrams, bibliography)
- [ ] Output formats and targets are correctly documented
- [ ] Compute steps describe Makefile operations

### Implementation: --from-interface Flag
- [ ] Add `--from-interface` flag to `maketalk.py`
- [ ] Add `--from-interface` flag to `makecv.py`
- [ ] Flag reads and validates interface file
- [ ] Verifies all inputs exist before execution
- [ ] Executes build according to interface specification
- [ ] Produces same output as direct execution

### Backward Compatibility
- [ ] Existing usage without flags works unchanged
- [ ] No performance impact on default (single-stage) usage
- [ ] All existing command-line arguments still work
- [ ] Two-stage workflow is completely opt-in

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

**1. Schema Design**
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
            {"target": "talk.slides.html", "dependencies": ["talk.md", "...]},
            {"target": "talk.notes.html", "dependencies": ["talk.md", "..."]}
        ]
    }
}
```

**2. Implementation in maketalk.py**
```python
# Add arguments
parser.add_argument("--generate-interface", action="store_true", 
                   help="Generate interface file without executing build")
parser.add_argument("--from-interface", type=str, metavar="FILE",
                   help="Execute build from interface file")

# Generate interface
if args.generate_interface:
    interface = generate_interface(args.filename, iface)
    write_interface_file(interface, f"{base}.interface.yml")
    sys.exit(0)

# Execute from interface
if args.from_interface:
    interface = load_interface_file(args.from_interface)
    validate_inputs(interface)
    execute_from_interface(interface)
    sys.exit(0)
```

**3. Leverage Existing Infrastructure**
- Build on current Makefile generation code
- Use existing `Interface` class for input/config handling
- Reuse dependency scanning from CIP-0009 optimizations
- Maintain compatibility with `--git-cache-minutes` and other flags

### Use Cases

**Use Case 1: Workflow Documentation**
```bash
# Generate interface to document workflow
maketalk --generate-interface my-talk.md
# Review my-talk.interface.yml to understand inputs/outputs
# Version control the interface file alongside source
```

**Use Case 2: Reproducible Builds**
```bash
# Generate interface on machine A
maketalk --generate-interface talk.md

# Transfer interface file to machine B
# Execute from interface (after ensuring inputs exist)
maketalk --from-interface talk.interface.yml
```

**Use Case 3: External Workflow Integration**
```bash
# Workflow manager generates interface files
for talk in *.md; do
    maketalk --generate-interface $talk
done

# Workflow manager orchestrates builds from interfaces
workflow-runner execute *.interface.yml
```

**Use Case 4: Debugging & Auditing**
```bash
# Generate interface to audit what will be built
maketalk --generate-interface talk.md
# Review interface to verify correct inputs/outputs
# Execute if satisfied
maketalk --from-interface talk.interface.yml
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

### 2026-01-04

Task created following acceptance of CIP-0006 with phased approach. This is Phase 1: pilot implementation with maketalk/makecv before expanding to other utilities.


