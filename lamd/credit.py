"""Diagram source attribution from sidecar metadata (CIP-0016).

Reads ``{stem}.credit.yml`` (canonical TASL) or a legacy ``{stem}.url``
shorthand next to a diagram, then formats a credit line for notes, slides,
or TeX. Expansion is explicit via ``\\diagramcredit{stem}``; image includes
do not auto-credit.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Mapping

import yaml

DIAGRAMCREDIT_RE = re.compile(r"\\diagramcredit\s*\{([^{}]+)\}")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".svg", ".gif", ".webp", ".pdf"}
DIAGRAMS_DIR_PREFIXES = (r"\diagramsDir/", r"\diagramsDir", "diagramsDir/")

LICENSE_LABELS: dict[str, str] = {
    "CC-BY-4.0": "CC BY 4.0",
    "CC-BY-SA-4.0": "CC BY-SA 4.0",
    "CC-BY-3.0": "CC BY 3.0",
    "CC-BY-SA-3.0": "CC BY-SA 3.0",
    "CC0-1.0": "CC0 1.0",
    "PD": "Public Domain",
    "Pixabay": "Pixabay License",
}

NO_LICENSE_STATUSES = frozenset({"unknown", "fair-use", "trademark"})
NO_CREDIT_LICENSES = frozenset({"FairUse", "Unknown", "Trademark"})
SILENT_STATUSES = frozenset({"trademark"})


@dataclass(frozen=True)
class Credit:
    """TASL fields plus classification for one diagram stem."""

    status: str = "unknown"
    title: str | None = None
    author: str | None = None
    author_url: str | None = None
    source: str | None = None
    source_binary: str | None = None
    license: str | None = None
    license_url: str | None = None
    modifications: tuple[str, ...] = field(default_factory=tuple)
    show_own: bool = False
    origin: str = "yaml"


def credit_output_context(to: str | None, fmt: str | None) -> str:
    """Return a formatter key for mdpp ``--to`` / ``--format``."""
    if to in {"pptx", "docx", "manim", "manim-video", "manim-svg", "python", "svg"}:
        return "empty"
    if fmt == "code":
        return "empty"
    if to == "tex":
        return "tex"
    if fmt == "slides":
        return "slides-html"
    return "notes-html"


def normalise_stem(raw: str, diagramsdir: str | None = None) -> str:
    """Turn a ``\\diagramcredit`` argument into a path relative to ``diagramsdir``."""
    stem = raw.strip()
    for prefix in DIAGRAMS_DIR_PREFIXES:
        if stem.startswith(prefix):
            stem = stem[len(prefix) :].lstrip("/")
            break
    if diagramsdir:
        diagramsdir = os.path.normpath(diagramsdir)
        candidate = os.path.normpath(stem)
        if os.path.isabs(candidate) or candidate.startswith(diagramsdir):
            try:
                rel = os.path.relpath(candidate, diagramsdir)
            except ValueError:
                rel = candidate
            if not rel.startswith(".."):
                stem = rel
    root, ext = os.path.splitext(stem)
    if ext.lower() in IMAGE_EXTENSIONS:
        stem = root
    return stem.replace("\\", "/").lstrip("./")


def _nonempty_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def credit_from_mapping(data: Mapping[str, Any], *, origin: str = "yaml") -> Credit:
    """Build a ``Credit`` from a YAML mapping."""
    modifications_raw = data.get("modifications") or []
    if isinstance(modifications_raw, str):
        modifications: tuple[str, ...] = (modifications_raw,) if modifications_raw.strip() else ()
    elif isinstance(modifications_raw, list):
        modifications = tuple(str(item).strip() for item in modifications_raw if str(item).strip())
    else:
        modifications = ()
    show_own = bool(data.get("show_own", False))
    return Credit(
        status=_nonempty_str(data.get("status")) or "unknown",
        title=_nonempty_str(data.get("title")),
        author=_nonempty_str(data.get("author")),
        author_url=_nonempty_str(data.get("author_url")),
        source=_nonempty_str(data.get("source")),
        source_binary=_nonempty_str(data.get("source_binary")),
        license=_nonempty_str(data.get("license")),
        license_url=_nonempty_str(data.get("license_url")),
        modifications=modifications,
        show_own=show_own,
        origin=origin,
    )


def load_credit_yaml(path: str) -> Credit | None:
    """Load ``.credit.yml``. Invalid or empty files return ``None``."""
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return None
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    return credit_from_mapping(data, origin="yaml")


def load_url_sidecar(path: str) -> Credit | None:
    """Load a one-line ``.url`` file as source-only, unclassified credit."""
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return None
    url = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not url:
        return None
    return Credit(status="unknown", source=url, origin="url")


def resolve_credit(diagramsdir: str, stem: str) -> Credit | None:
    """Return credit for ``stem``, preferring YAML over a legacy ``.url`` file."""
    relative = normalise_stem(stem, diagramsdir)
    base = os.path.normpath(os.path.join(diagramsdir, relative))
    yaml_path = base + ".credit.yml"
    credit = load_credit_yaml(yaml_path)
    if credit is not None:
        return credit
    return load_url_sidecar(base + ".url")


def license_label(license_id: str | None) -> str | None:
    """Human license label; unknown ids pass through unless they are classifiers."""
    if not license_id:
        return None
    if license_id in NO_CREDIT_LICENSES:
        return None
    return LICENSE_LABELS.get(license_id, license_id)


def may_show_license(credit: Credit) -> bool:
    """CC/PD labels are never inferred from a bare ``.url`` or unknown/fair-use status."""
    if credit.origin == "url":
        return False
    if credit.status in NO_LICENSE_STATUSES:
        return False
    return license_label(credit.license) is not None


def should_emit(credit: Credit) -> bool:
    """Whether this credit produces output for the current document."""
    if credit.status == "own" and not credit.show_own:
        return False
    if credit.status in SILENT_STATUSES:
        return False
    return bool(credit.title or credit.author or credit.source)


def _md_link(label: str, url: str) -> str:
    safe_label = label.replace("[", "\\[").replace("]", "\\]")
    return f"[{safe_label}]({url})"


def _gpp_safe(text: str) -> str:
    """Strip gpp delimiters so interpolated titles cannot nest macros."""
    return text.replace("\\", "").replace("{", "").replace("}", "")


def format_notes(credit: Credit) -> str:
    """Full TASL line for HTML/ipynb notes (Markdown)."""
    if not should_emit(credit):
        return ""
    bits: list[str] = []
    if credit.title and credit.author:
        bits.append(f"{credit.title} by {credit.author}.")
    elif credit.title:
        bits.append(f"{credit.title}.")
    elif credit.author:
        bits.append(f"Image by {credit.author}.")
    if credit.source:
        bits.append(f"{_md_link('Source', credit.source)}.")
    if may_show_license(credit):
        label = license_label(credit.license)
        assert label is not None
        if credit.license_url:
            bits.append(f"{_md_link(label, credit.license_url)}.")
        else:
            bits.append(f"{label}.")
    if credit.modifications:
        bits.append("Modified: " + ", ".join(credit.modifications) + ".")
    if not bits:
        return ""
    return "*Credit:* " + " ".join(bits)


def format_slides(credit: Credit) -> str:
    """Compact, slide-visible credit using existing ``\\small`` / ``\\alignright`` macros."""
    if not should_emit(credit):
        return ""
    title = _gpp_safe(credit.title or "Source")
    if credit.source:
        inner = _md_link(title, credit.source)
    else:
        inner = title
    paren: list[str] = []
    if credit.author:
        paren.append(_gpp_safe(credit.author))
    if may_show_license(credit):
        label = license_label(credit.license)
        if label:
            paren.append(label)
    suffix = f" ({', '.join(paren)})" if paren else ""
    return r"\small{\alignright{" + inner + suffix + r"}}"


def format_tex(credit: Credit) -> str:
    """TeX notes: Markdown credit line (pandoc turns links into ``\\href``)."""
    return format_notes(credit)


def format_credit(credit: Credit | None, context: str) -> str:
    """Format ``credit`` for a mdpp output context."""
    if credit is None or context == "empty":
        return ""
    if context == "slides-html":
        return format_slides(credit)
    if context == "tex":
        return format_tex(credit)
    return format_notes(credit)


def expand_diagramcredit(text: str, diagramsdir: str, context: str) -> str:
    """Replace ``\\diagramcredit{stem}`` with a formatted credit (or empty)."""

    def _replace(match: re.Match[str]) -> str:
        credit = resolve_credit(diagramsdir, match.group(1))
        return format_credit(credit, context)

    return DIAGRAMCREDIT_RE.sub(_replace, text)
