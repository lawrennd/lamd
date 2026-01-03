---
id: "explicit-over-implicit"
title: "Explicit Over Implicit"
status: "Active"
created: "2026-01-03"
last_reviewed: "2026-01-03"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- transparency
- debugging
- clarity
---

# Tenet: Explicit Over Implicit

## Tenet

**Description**: Transformation pipelines and dependencies should be transparent and traceable. Users should be able to understand and debug how their content becomes output. Magic is convenient until it breaks - then it becomes a nightmare to debug. The lamd philosophy favors explicit transformation steps over implicit behavior. Makefiles show the build pipeline clearly. Dependency tracking makes includes and references visible. Validation utilities catch configuration errors early and explain what went wrong. Interface files document inputs, outputs, and computations. This transparency empowers users to understand the system, customize it to their needs, and fix problems when they arise.

**Quote**: *"Show the path, don't hide it"*

**Examples**:
- Makefile-based build system shows explicit transformation steps rather than hiding them
- Dependency tracking makes includes and references visible in the build process
- Validation utilities catch configuration errors early with clear error messages
- Interface files (CIP-0006) explicitly document inputs, outputs, and computations
- Error messages explain what went wrong and suggest fixes
- Build logs show which commands are executed and in what order

**Counter-examples**:
- Automatic detection of file types without giving users visibility or control
- Silent failure when includes or dependencies are missing
- Magic behavior that "just works" until it doesn't, with no way to understand why
- Hiding build steps behind abstraction layers that can't be inspected
- Error messages that say "something went wrong" without explaining what or why

**Conflicts**:
- **Simplicity vs. Transparency**: Explicit steps can be more complex than automatic behavior
- Resolution: Provide sensible defaults that work automatically but allow users to override and inspect
- **Verbosity vs. Clarity**: Explicit systems can be verbose
- Resolution: Use good defaults to reduce boilerplate while maintaining visibility when needed

