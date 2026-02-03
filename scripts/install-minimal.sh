#!/usr/bin/env bash
#
# LaMD minimal installer (agent hints + optional venv)
#
# Intended usage (run from a target repo root, e.g. talks/ or execed/):
#   bash -c "$(curl -fsSL https://raw.githubusercontent.com/lawrennd/lamd/main/scripts/install-minimal.sh)"
#
# Clean installation philosophy:
# - Safe to re-run
# - Updates LaMD "system" hint files
# - Preserves user content
#
set -euo pipefail

LAMD_DOCS_URL="${LAMD_DOCS_URL:-https://inverseprobability.com/lamd/}"
LAMD_VENV_DIR_DEFAULT=".venv-lamd"

usage() {
  cat <<'EOF'
LaMD minimal installer

Installs:
- Cursor rules: .cursor/rules/lamd_talks.mdc
- Optional: .cursorrules (if missing)
- Optional: inserts/updates a marked LaMD block in AGENTS.md and CLAUDE.md
- Optional: creates a local venv and installs `lamd` so `maketalk` is available

Options:
  --with-venv            Create venv and install lamd (network needed)
  --venv-dir PATH        Venv directory (default: .venv-lamd)
  --no-cursorrules       Do not create .cursorrules (even if missing)
  --no-agents            Do not touch AGENTS.md
  --no-claude            Do not touch CLAUDE.md
  -h, --help             Show this help

Notes:
- System prerequisites like `gpp` and `pandoc` are NOT installed by this script.
EOF
}

WITH_VENV=0
VENV_DIR="$LAMD_VENV_DIR_DEFAULT"
INSTALL_CURSORRULES=1
INSTALL_AGENTS=1
INSTALL_CLAUDE=1
INSTALL_CURSORS_RULES_FILE=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --with-venv) WITH_VENV=1; shift ;;
    --venv-dir) VENV_DIR="${2:-}"; shift 2 ;;
    --no-cursorrules) INSTALL_CURSORS_RULES_FILE=0; shift ;;
    --no-agents) INSTALL_AGENTS=0; shift ;;
    --no-claude) INSTALL_CLAUDE=0; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

PROJECT_ROOT="$(pwd)"

have_cmd() { command -v "$1" >/dev/null 2>&1; }

write_if_changed() {
  local dest="$1"
  local tmp
  tmp="$(mktemp)"
  cat >"$tmp"

  mkdir -p "$(dirname "$dest")"
  if [[ -f "$dest" ]] && cmp -s "$tmp" "$dest"; then
    rm -f "$tmp"
    return 0
  fi
  mv "$tmp" "$dest"
}

upsert_marked_block_python() {
  local filepath="$1"
  local block_tmp="$2"
  python3 - "$filepath" "$block_tmp" <<'PY'
import sys
from pathlib import Path

filepath = Path(sys.argv[1])
block_tmp = Path(sys.argv[2])

block = block_tmp.read_text(encoding="utf-8")
begin = "<!-- LAMD:BEGIN -->"
end = "<!-- LAMD:END -->"

if not filepath.exists():
    filepath.write_text(block + "\n", encoding="utf-8")
    sys.exit(0)

text = filepath.read_text(encoding="utf-8")
if begin in text and end in text and text.index(begin) < text.index(end):
    pre = text[: text.index(begin)]
    post = text[text.index(end) + len(end) :]
    new_text = (pre.rstrip("\n") + "\n\n" + block.strip("\n") + "\n\n" + post.lstrip("\n"))
else:
    new_text = text.rstrip("\n") + "\n\n" + block.strip("\n") + "\n"

filepath.write_text(new_text, encoding="utf-8")
PY
}

install_cursor_rules() {
  if [[ "$INSTALL_CURSORRULES" -ne 1 ]]; then
    return 0
  fi

  write_if_changed "$PROJECT_ROOT/.cursor/rules/lamd_talks.mdc" <<'EOF'
---
description: Guidance for repositories that build content with LaMD (talks/lectures/notes).
globs:
alwaysApply: true
---

# LaMD authoring + build conventions

You are assisting with repositories that use **LaMD** to convert markdown-with-macros into **slides/notes/pages** via `maketalk` (and related commands like `mdpp`, `mdfield`, `mdpeople`).

## What LaMD content looks like

- **YAML frontmatter is required** at the top of each talk/lecture markdown file.
- **Macros** (LaMD / gpp) extend markdown (e.g. `\include{...}`, `\slides{...}`, `\notes{...}`).
- Reusable text belongs in a **snippets repository** and is pulled in via `\include{_topic/includes/file.md}`.

## Slides vs notes

- Use `\slides{...}` for slide-visible content and `\notes{...}` for detailed speaker notes.
- For presenter-only notes in reveal.js output, use `\speakernotes{...}` (does not appear on the slide itself).
- Keep slide density low:
  - Aim for **≤ 3 bullets per slide** (or **≤ 2 formulae**).
  - Prefer multiple slides over one crowded slide.
- Create new slides with `\newslides{Title}` (slides-only) or `\subsection{Title}` (both slides and notes).

## Incremental / progressive reveal (slides)

LaMD supports progressive reveal patterns for HTML slides (reveal.js):

- `\slidesincremental{...}` wraps content (typically a bullet list) so bullets reveal incrementally.
- `\fragment{...}{type}` marks an element as a reveal.js fragment (e.g. `fade-in`, `grow`).

Examples:

```markdown
\newslides{Key points}

\slidesincremental{
* First point
* Second point
* Third point
}
```

```markdown
\slides{We can build this idea step-by-step: \fragment{first}{fade-in} \fragment{then}{fade-in}}
```

## Repo structure expectations (common pattern)

- Source lives under topic directories like `_ai/`, `_ml/`, `_information/` etc.
- Each topic directory often has its own `_lamd.yml` controlling paths and build options.
- Build outputs typically go to sibling directories (`_posts/`, `_lectures/`, `slides/`, `_notes/`, `_notebooks/`), configured by `_lamd.yml`.

## How to run builds

- Run `maketalk your-file.md` **from the directory that contains** the relevant `_lamd.yml`.
- `maketalk` generates a local `makefile` and invokes `make` targets.
  - Treat that generated `makefile` as **build artefact**; don’t hand-edit it.

## External dependencies (can’t be “fixed in code”)

LaMD relies on tools that must exist on the machine:
- `gpp` (macro preprocessor)
- `pandoc` (conversion engine)
- for some pipelines: LaTeX, `inkscape`, etc.

If a build fails due to missing system tools, prefer:
- printing **actionable** missing-tool messages
- suggesting `brew install gpp pandoc` (macOS) / `apt-get install gpp pandoc` (Linux)

## Editing guidance (what to optimize for)

- Preserve the author’s voice and the macro idioms already used in the repo.
- If a section looks broadly reusable, move it into the snippets repo and include it.
- Keep changes composable: prefer small includes over monolithic blocks.
EOF
}

install_cursorrules_if_missing() {
  if [[ "$INSTALL_CURSORS_RULES_FILE" -ne 1 ]]; then
    return 0
  fi

  if [[ -f "$PROJECT_ROOT/.cursorrules" ]]; then
    return 0
  fi

  mkdir -p "$PROJECT_ROOT"
  cat >"$PROJECT_ROOT/.cursorrules" <<'EOF'
general
You are supporting a machine learning expert with content written in the LaMD markdown language (markdown + macros).

Key LaMD conventions:
- `\slides{}` controls slide-visible content.
- `\notes{}` controls speaker notes / detailed text.
- `\speakernotes{}` adds presenter-only notes in reveal.js output.
- `\slidesincremental{}` enables incremental bullet reveals in slides.
- `\fragment{text}{type}` creates reveal.js fragments (e.g. `fade-in`).
- `\newslides{Title}` creates a new slide (slides only).
- `\subsection{Title}` creates a section that appears in both slides and notes.
- Keep each slide to a maximum of three bullets (or two formulae).

Content reuse:
- If a section is likely reusable, move it into a snippets repository and include it with `\include{_topic/includes/file.md}`.
EOF
}

install_agents_markdown() {
  if [[ "$INSTALL_AGENTS" -ne 1 ]]; then
    return 0
  fi

  local block_tmp
  block_tmp="$(mktemp)"
  cat >"$block_tmp" <<EOF
<!-- LAMD:BEGIN -->
# LaMD agent hints (Codex / general agents)

- **Docs**: \`$LAMD_DOCS_URL\`
- **Build entrypoint**: \`maketalk\` (requires Python + LaMD install)
- **Config**: builds are controlled by per-directory \`_lamd.yml\` files.
- **Macro language**: markdown is preprocessed (gpp) then converted (pandoc).

## How to build

- Run \`maketalk some-talk.md\` **from the directory containing** \`_lamd.yml\`.
- If a build fails, check system prerequisites first: \`gpp\`, \`pandoc\`, and sometimes LaTeX / \`inkscape\`.

## Authoring principles

- Keep slides low-density (≤ 3 bullets).
- Use \`\\slides{...}\` vs \`\\notes{...}\` to control what shows where.
- Use \`\\slidesincremental{...}\` and \`\\fragment{...}{...}\` for progressive reveal when presenting.
- Use \`\\speakernotes{...}\` for presenter-only notes in reveal.js output.
- Prefer reusable includes in a snippets repo rather than copy/paste duplication.
<!-- LAMD:END -->
EOF

  if have_cmd python3; then
    upsert_marked_block_python "$PROJECT_ROOT/AGENTS.md" "$block_tmp"
  else
    # Fallback: don’t attempt in-place edits without Python.
    write_if_changed "$PROJECT_ROOT/AGENTS.lamd.md" <"$block_tmp"
  fi

  rm -f "$block_tmp"
}

install_claude_markdown() {
  if [[ "$INSTALL_CLAUDE" -ne 1 ]]; then
    return 0
  fi

  local block_tmp
  block_tmp="$(mktemp)"
  cat >"$block_tmp" <<EOF
<!-- LAMD:BEGIN -->
# LaMD agent hints (Claude Code)

This repository uses **LaMD** to build talks/lectures/notes from markdown-with-macros.

- **Docs**: \`$LAMD_DOCS_URL\`
- **Build command**: \`maketalk\` (LaMD console script)
- **Config file**: \`_lamd.yml\` must exist in the working directory where builds are run

## What to assume

- LaMD content is markdown preprocessed by **gpp** and converted by **pandoc**.
- The project may pull in reusable content via \`\\include{...}\` from a snippets repository.
- HTML slides (reveal.js) support \`\\slidesincremental{...}\` and \`\\fragment{...}{...}\` for progressive reveal.
- Presenter-only notes are supported via \`\\speakernotes{...}\` (in reveal.js output).

## How to behave when editing content

- Preserve macro style and frontmatter.
- Keep slide text sparse; break content into multiple slides rather than dense slides.
- Use incremental reveals sparingly; prefer clear slide structure over complex animation.
- If a block is reusable, factor it into a snippets include.
<!-- LAMD:END -->
EOF

  if have_cmd python3; then
    upsert_marked_block_python "$PROJECT_ROOT/CLAUDE.md" "$block_tmp"
  else
    write_if_changed "$PROJECT_ROOT/CLAUDE.lamd.md" <"$block_tmp"
  fi

  rm -f "$block_tmp"
}

ensure_venv_and_install_lamd() {
  if [[ "$WITH_VENV" -ne 1 ]]; then
    return 0
  fi

  if ! have_cmd python3; then
    echo "Error: python3 not found; cannot create venv." >&2
    exit 1
  fi

  if [[ ! -d "$PROJECT_ROOT/$VENV_DIR" ]]; then
    python3 -m venv "$PROJECT_ROOT/$VENV_DIR"
  fi

  "$PROJECT_ROOT/$VENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel

  # Install lamd (network required). If you need local dev, install editable from a checkout instead.
  "$PROJECT_ROOT/$VENV_DIR/bin/python" -m pip install --upgrade lamd

  cat <<EOF

LaMD venv ready at: $VENV_DIR

Try:
  PATH="$PROJECT_ROOT/$VENV_DIR/bin:\$PATH" maketalk your-talk.md

System prerequisites (install separately):
  - gpp
  - pandoc
EOF
}

main() {
  install_cursor_rules
  install_cursorrules_if_missing
  install_agents_markdown
  install_claude_markdown
  ensure_venv_and_install_lamd

  echo "LaMD minimal install complete."
}

main
