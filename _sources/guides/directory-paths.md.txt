# Directory paths in LaMD builds

LaMD projects declare several directory fields in `_lamd.yml`. They look interchangeable
(`slidesdir`, `diagramsdir`, …) but each answers a different question and is resolved
relative to a **different anchor**. Mixing them up is the usual cause of “the file was
built but pandoc cannot find it” failures.

This guide documents **current field semantics** (as implemented in `mdpp`,
`dependencies`, makefiles, and `copy_web_diagrams.sh`). Planned changes are described
in [CIP-0010: Unified Diagram Path Resolution](../../cip/cip0010.md).

Authoring uses the gpp macro `\diagramsDir` (set at preprocess time). Content refers to
diagrams as `\diagramsDir/ml/foo000`, which becomes a path in generated markdown
(for example `../slides/diagrams//ml/foo000.emf` for PPTX).

| Consumer | What it needs | Typical anchor |
|----------|---------------|----------------|
| **Inkscape / make** | Build `foo.emf` from `foo.svg` | cwd when `make` runs (usually `_lamd/`) |
| **pandoc** | Open the path embedded in markdown | `--resource-path` plus paths relative to cwd |
| **dependencies** | List files for makefile prerequisites | Same as make (relative to cwd) |
| **Published HTML** | Browser URL for `<img src="…">` | Site root (`url` + `baseurl`), not the filesystem |

For local builds (pptx, docx, tex, …), paths resolve from the build cwd. `baseurl`
affects `\diagramsDir` only when `mdpp --to html` or `mdpp --to ipynb`.

---

## Anchor: where is the build?

Most course/talk repos use this layout:

```
project/
├── _lamd/              ← maketalk / make run here (cwd)
│   ├── _lamd.yml
│   ├── talk.md
│   └── makefile        ← generated
├── slides/             ← slide HTML outputs + diagram sources
│   └── diagrams/
│       └── ml/
│           └── foo000.svg
└── _lectures/          ← published lecture HTML (posts)
```

**Rule of thumb:** paths in `_lamd.yml` are usually written **relative to `_lamd/`**
(the build cwd), not relative to the repository root and not relative to `baseurl`.

For the layout above:

```yaml
slidesdir: ../slides/
diagramsdir: ../slides/diagrams/
```

Using `./slides/diagrams/` is wrong here: that resolves to `_lamd/slides/diagrams/`,
which is not where SVG sources live.

---

## Field reference

### `diagramsdir`

**Purpose:** Directory containing diagram **sources and converted assets** (SVG, EMF,
PDF, PNG) that macros reference via `\diagramsDir`.

**Used by:**

| Tool | How |
|------|-----|
| `mdpp` | Sets gpp `-DdiagramsDir=…` (see dual behaviour below) |
| `dependencies` | Substitutes `\diagramsDir` when scanning `\includediagram{…}` |
| Make (`PPTXDEPS`, `DOCXDEPS`, …) | Inkscape rules build `$(DIAGRAMSDIR)/…/*.emf` from `.svg` |
| `copy_web_diagrams.sh` | Locates source files to copy into publish trees |

**Dual behaviour in `mdpp`** (`lamd/mdpp.py`):

```python
url = diagramsurl or (url + baseurl)
diagrams_dir = url + diagramsdir          # when --to html or ipynb
diagrams_dir = diagramsdir              # when --to pptx, docx, tex, …
# Makefile always passes --diagrams-dir $(DIAGRAMSDIR), overriding the above
```

- **Local formats (pptx, docx, tex, …):** `\diagramsDir` is the filesystem path from
  config (or `--diagrams-dir`). Must be valid from `_lamd/` cwd.
- **HTML / ipynb:** `\diagramsDir` becomes a **URL prefix** unless `--diagrams-dir`
  overrides it. Prefer explicit `diagramsurl` when the published path differs from the
  filesystem layout.

**Not the same as:** `slidesdir` (outputs and resource-path only), `writediagramsdir`
(generated diagrams), or `baseurl` alone.

---

### `diagramsurl` (optional)

**Purpose:** Override the URL prefix used for `\diagramsDir` in HTML/ipynb when
`url + baseurl + diagramsdir` would be wrong.

**Example:** site at `https://example.org/course/` with diagrams served at
`https://example.org/course/slides/diagrams/`:

```yaml
url: https://example.org/
baseurl: course/
diagramsurl: https://example.org/course/slides/
diagramsdir: diagrams/    # URL suffix after diagramsurl, or filesystem path for local builds
```

If unset, `mdpp` uses `url + baseurl` as the URL prefix.

---

### `slidesdir`

**Purpose:** Where **built slide HTML** is copied (`cp … ${SLIDESDIR}/…`) and a root
for pandoc `--resource-path` (with `.` and `includes`).

**Used by:**

| Tool | How |
|------|-----|
| `make-slides.mk` | `cp ${BASE}.slides.html ${SLIDESDIR}/${OUT}.slides.html` |
| `make-talk-flags.mk` | `PPTXFLAGS=… --resource-path .:$(INCLUDESDIR):$(SLIDESDIR)` |
| `copy_web_diagrams.sh` | Second argument pair: publish target under slides tree |

**Relationship to diagrams:** In many projects, `diagramsdir` is **`slidesdir` +
`diagrams/`** (e.g. `../slides/` + `diagrams/` → `../slides/diagrams/`). That keeps
diagram assets next to slide outputs. They are still **separate keys** with separate
roles; duplicating the path in config is intentional.

**Not combined with `baseurl` for local file lookup.** `baseurl` does not appear in
makefile diagram rules or `dependencies`.

---

### `writediagramsdir`

**Purpose:** Where **generated** diagrams are written (e.g. manim, dynamic figures),
via gpp `-DwriteDiagramsDir=…`.

**Default:** `.` (often `_lamd/` itself).

**Distinct from `diagramsdir`:** `diagramsdir` is for checked-in SVG/EMF assets;
`writediagramsdir` is for outputs produced during build.

---

### `url` and `baseurl`

**Purpose:** Jekyll/GitHub Pages **site** location for published lecture pages.

**Used by:**

| Tool | How |
|------|-----|
| `mdpp` | Prefix for `\diagramsDir` when `--to html` or `--to ipynb` (unless `diagramsurl`) |
| `flags post` | `edit_url` metadata for GitHub edit links |

**Not used by:** pptx/docx build, inkscape conversion, or `dependencies batch` (local
paths only).

Example from a course site:

```yaml
url: "https://mlatcl.github.io/"
baseurl: mlfc/
```

Published pages live under `https://mlatcl.github.io/mlfc/…`. That is unrelated to
`../slides/diagrams/` on disk except that you usually **copy** diagrams into the tree
that GitHub Pages serves (`copy_web_diagrams.sh` → `${SLIDESDIR}/diagrams/`).

---

### Other output directories

| Field | Role |
|-------|------|
| `postsdir` / `practicalsdir` | Destination for compiled lecture/practical HTML |
| `notesdir` | PDF notes output |
| `notebooksdir` | Jupyter notebook output |
| `snippetsdir` | `\include{…}` search path (often absolute or `$HOME/…`) |
| `bibdir` | Bibliography files |
| `macrosdir` | gpp macro definitions |

These do not substitute for `diagramsdir`.

---

## End-to-end flow (PPTX example)

1. **Authoring:** `\includediagram{\diagramsDir/ml/quadratic_basis000}{…}` in snippets.
2. **dependencies batch** (with `--diagrams-dir $(DIAGRAMSDIR)`): lists
   `../slides/diagrams//ml/quadratic_basis000.emf` as `pptxdiagrams` prerequisite.
3. **make-figures.mk:** `../slides/diagrams//ml/quadratic_basis000.emf` built from
   `.svg` via Inkscape.
4. **mdpp** (`--diagrams-dir ../slides/diagrams/`): markdown contains
   `![](../slides/diagrams//ml/quadratic_basis000.emf)`.
5. **pandoc** (`--resource-path .:includes:../slides/`): resolves path from `_lamd/`
   cwd; EMF must exist at that relative path.

All five steps must agree on the same filesystem path for `\diagramsDir`.

---

## Configuration checklist

When diagram paths fail, verify in order:

1. **cwd:** Are you building from `_lamd/` (where `_lamd.yml` and generated makefile live)?
2. **`diagramsdir`:** From `_lamd/`, does `ls $(diagramsdir)/ml/*.svg` show sources?
3. **Consistency:** Does `dependencies batch … --diagrams-dir $(diagramsdir)` list the
   same `.emf` paths that appear in `*.slides.pptx.markdown`?
4. **Regenerate:** After changing `_lamd.yml`, run `maketalk` again so the makefile
   picks up new `DIAGRAMSDIR` / `PPTXDEPS`.
5. **HTML only:** If slides render locally but not on the site, check `url` / `baseurl`
   / `diagramsurl`, not `diagramsdir` alone.

---

## Related

- [Slides context](../contexts/slides.md) — `\includediagram` and reveal.js
- [CIP-0010: Unified Diagram Path Resolution](../../cip/cip0010.md)
- [Macro-aware diagram extraction](../../backlog/features/2026-08-09_macro-aware-diagram-dependency-extraction.md) — `\define` + `\concat` in diagram paths (lynguine)
