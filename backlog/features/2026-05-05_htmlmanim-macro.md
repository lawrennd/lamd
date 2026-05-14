---
category: features
created: '2026-05-05'
id: 2026-05-05_htmlmanim-macro
last_updated: '2026-05-05'
priority: Low
related_cips:
- 000C
status: Completed
owner: "Neil Lawrence"
title: Introduce \htmlmanim{html_content}{manim_alt} dispatching macro
---

# Task: Introduce `\htmlmanim{html_content}{manim_alt}` dispatching macro

## Description

Currently, HTML-only content (interactive widgets, JavaScript simulations) is
suppressed entirely in Manim output via `\html{}`.  This means Manim
presentations show a blank space where a rich visual should be.

The `\htmlmanim{html_content}{manim_alt}` macro would allow content authors to
provide a **Manim-native alternative** for HTML widgets, enabling richer Manim
presentations without duplicating slide content for other formats.

## Macro Semantics

```markdown
\htmlmanim{
  \html{
    <canvas id="sim"></canvas>
    \include{_scripts/includes/sim-js.md}
  }
}{
  \slidesmanim{
      _img = ImageMobject("simulation-screenshot.png")
      self.play(FadeIn(_img))
  }
}
```

| Format | Expands to |
|---|---|
| HTML slides | First argument (JS widget via `\html{}`) |
| Manim (`--to manim`, `--to manim-video`) | Second argument (Manim code via `\slidesmanim{}`) |
| PDF, PPTX, notes | Neither argument (both are no-ops) |

## Acceptance Criteria

- `\htmlmanim{a}{b}` defined as a no-op in `talk-macros-null.gpp` (both args
  discarded).
- `\htmlmanim{a}{b}` defined to expand `\a` (first arg) in `talk-macros-html.gpp`.
- `\htmlmanim{a}{b}` defined to expand `\b` (second arg) in
  `talk-macros-manim.gpp`.
- A test verifies the correct argument is expanded in each output format.
- Documentation updated in `docs/guides/manim-output.md`.

## Implementation Notes

- Analogous to `\slidenotes{slide}{notes}` which expands differently per format.
- The two-argument GPP macro syntax: `\define{\htmlmanim{html}{manim_alt}}{...}`.
- No changes to `mdpp.py` are required; this is a pure GPP macro change.

## Related

- CIP: 000C
- See also: `backlog/features/2026-05-05_html-stripping-safety-net.md`
- See also: `backlog/features/2026-05-05_snippets-html-audit.md`

## Progress Updates

### 2026-05-05
Task created.  Status Proposed — design approved, implementation deferred.