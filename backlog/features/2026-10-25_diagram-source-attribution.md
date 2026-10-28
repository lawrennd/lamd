---
id: "2026-10-25_diagram-source-attribution"
title: "Incorporate diagram source URLs as attribution"
status: "In Progress"
priority: "Medium"
created: "2026-10-25"
last_updated: "2026-10-25"
category: "features"
related_cips: ["0016"]
owner: "Neil Lawrence"
dependencies: []
tags:
- backlog
- diagrams
- attribution
- licensing
- academic-rigor
---

# Task: Incorporate diagram source URLs as attribution

> **Note**: Backlog tasks are DOING the work defined in CIPs (HOW).
> Use `related_cips` to link to CIPs. Don't link directly to requirements (bottom-up pattern).
>
> CIP-0016 is Accepted and In Progress. This task tracks the lamd implementation.

## Description

Many third-party images under `~/lawrennd/slides/diagrams/` have a sibling
`.url` file containing a single source URL (often Wikimedia Commons
`upload.wikimedia.org`, also Flickr, Pixabay, Wikipedia, news sites, and
others). The build never reads these files. Attribution, when it appears at
all, is hand-written into figure captions (for example the Bernoulli portrait
snippet). Lamd already defines `\credit{name}{url}` for slides and notes, but
snippets and talks do not use it, and it is not documented in the media
context.

A source URL is provenance, not a credit line. Creative Commons BY / BY-SA
need Title, Author, Source, and License (TASL). Direct binary URLs also skip
the Commons File page, which is the preferred source link.

Inventory as of 2026-10-25:

- 281 `.url` files; 275 have a matching image; all are a single URL line
- Wikimedia/Commons: 130; Flickr: 11; Pixabay: 4; Wikipedia: 2; other: 131
- Three empty `.url` files
- Sample JPEGs have no IPTC/EXIF license payload; metadata lives only in the sidecar

Related content lives in three places: `slides` (images and `.url` files),
`snippets` (includes), and `lamd` (macros and figure rendering). Slides HTML
currently puts `\figure` captions in speaker notes only, so caption-only
credits would not appear on the slide.

## Acceptance Criteria

- [ ] Agreed sidecar schema that can store at least: source URL, title, author,
      license id, license URL, and optional modifications
- [ ] Decision recorded: keep plain `.url` and add YAML, or replace `.url` with
      YAML that still contains `source`
- [ ] Lamd can render a credit from that sidecar in notes/HTML and on slides
      without silently changing every `\includejpg` / `\includediagram`
- [ ] Wikimedia-hosted files can be backfilled via the Commons API; other hosts
      remain manual
- [ ] Unknown / fair-use / trademark (logos, book covers, news photos) are
      classified rather than credited as CC
- [x] CIP opened if the macro/schema work is accepted as a design change
      ([CIP-0016](../../cip/cip0016.md), In Progress)

## Implementation Notes

### What CC-BY actually needs

For CC BY and BY-SA, a URL is not enough. Store:

| Field | Why |
|---|---|
| `title` | TASL Title |
| `author` (and optional `author_url`) | TASL Author |
| `source` | TASL Source; prefer the File: page, not only the upload binary |
| `license` + `license_url` | TASL License (CC-BY-4.0, CC-BY-SA-4.0, CC0, PD, Pixabay, unknown, …) |
| `modifications` | Required when the local file is cropped or redrawn |
| `status` | `own` / `third-party` / `public-domain` / `unknown` |

Own diagrams need no third-party credit. Public-domain / CC0 items still
benefit from a source line as scholarship. Wikipedia `upload.wikimedia.org/wikipedia/en/`
files are often fair use (book covers) and must not be labelled CC.

### Suggested phases

1. **Inventory in `slides`**: classify existing `.url` hosts; flag high-risk
   (news, Twitter, Wikipedia-en, logos).
2. **Sidecar schema**: YAML next to the image. Configuration-lives-with-content
   argues against a single global credits catalogue.
3. **Lamd rendering**: extend or replace `\credit`. Keep includes explicit
   (a credited-include helper, or an opt-in figure argument) rather than
   auto-injecting credits on every image include.
4. **Backfill**: Commons API for Wikimedia URLs; manual for the rest.
5. **Optional check**: warn when a talk includes a third-party image with no
   sidecar.

### Open design choices

- Slide density vs legal credit: small corner credit vs speaker-notes-only vs
  a collected credits slide.
- Whether generated matplotlib SVGs should carry authorship at all.
- Whether `\credit` stays `name`+`url` or grows license fields.

## Related

- CIP: [0016](../../cip/cip0016.md) (In Progress)
- Repos: `lawrennd/slides` (`.url` files), `lawrennd/snippets` (includes),
  `lawrennd/lamd` (macros)
- Existing macro: `\credit{name}{url}` in `talk-macros-slides.gpp` /
  `talk-macros-notes.gpp` (unused in snippets)
- Example of caption-level credit:
  `snippets/_physics/includes/daniel-bernoulli-portrait.md`
- Tenet: academic-rigor-through-tooling; also explicit-over-implicit and
  configuration-lives-with-content

## Progress Updates

### 2026-10-25

Task created with Proposed status after reviewing `.url` sidecars and current
figure/credit macros.

CIP-0016 drafted (Proposed): sibling `.credit.yml` as the TASL sidecar, explicit
`\diagramcredit{stem}` expanded by mdpp, `.url` kept as source-only shorthand.
Awaiting review before Accept.

CIP-0016 accepted and moved to In Progress; implementation started in lamd
(`credit` resolver, mdpp expansion, Commons backfill helper).
