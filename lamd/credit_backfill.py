"""Backfill ``.credit.yml`` sidecars from Wikimedia Commons (CIP-0016).

Not a required build step. Given a diagrams directory, reads ``*.url`` files,
queries the Commons API for Wikimedia-hosted images, and writes YAML. Non-
Wikimedia hosts are left for manual attribution. Wikipedia-en uploads are
classified as fair use and never labelled Creative Commons.

Live HTTP is not used in tests; pass a ``fetch`` callable to inject responses.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from collections.abc import Mapping
from dataclasses import asdict
from typing import Any, Callable, Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlparse
from urllib.request import Request, urlopen

import yaml

from lamd.credit import Credit, load_credit_yaml, load_url_sidecar

USER_AGENT = "lamd-credit-backfill/0.1 (https://github.com/lawrennd/lamd; lawrennd@gmail.com)"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
HTML_TAG_RE = re.compile(r"<[^>]+>")

LICENSE_SHORT_TO_ID: dict[str, str] = {
    "cc by 4.0": "CC-BY-4.0",
    "cc by-sa 4.0": "CC-BY-SA-4.0",
    "cc by 3.0": "CC-BY-3.0",
    "cc by-sa 3.0": "CC-BY-SA-3.0",
    "cc0": "CC0-1.0",
    "cc0 1.0": "CC0-1.0",
    "public domain": "PD",
    "pd": "PD",
}

FetchFn = Callable[[str], dict[str, Any]]


def strip_html(text: str) -> str:
    """Remove tags and unescape HTML entities from Commons extmetadata."""
    return html.unescape(HTML_TAG_RE.sub("", text)).strip()


def _url_hostname(url: str) -> str:
    """Hostname from ``url``, lowercased. Empty when the URL has no host."""
    return (urlparse(url).hostname or "").lower()


def classify_source_url(url: str) -> str:
    """Return ``commons``, ``wikipedia-en``, or ``other``."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    path = parsed.path.lower()

    if host == "en.wikipedia.org" or (host == "upload.wikimedia.org" and path.startswith("/wikipedia/en/")):
        return "wikipedia-en"
    if host == "commons.wikimedia.org" or (host == "upload.wikimedia.org" and path.startswith("/wikipedia/commons/")):
        return "commons"
    return "other"


def filename_from_url(url: str) -> str | None:
    """Best-effort File: basename from a Commons File page or upload URL."""
    parsed = urlparse(url)
    path = unquote(parsed.path)
    if "/wiki/File:" in path or path.startswith("/wiki/File:"):
        marker = "File:"
        idx = path.find(marker)
        if idx >= 0:
            return path[idx + len(marker) :]
    name = path.rsplit("/", 1)[-1]
    return name or None


def license_id_from_short_name(short: str | None) -> str | None:
    """Map Commons ``LicenseShortName`` to a sidecar license id."""
    if not short:
        return None
    key = " ".join(short.strip().lower().split())
    key = key.replace("attribution-sharealike", "by-sa").replace("attribution", "by")
    return LICENSE_SHORT_TO_ID.get(key)


def _ext_value(extmetadata: Mapping[str, Any], key: str) -> str | None:
    block = extmetadata.get(key)
    if not isinstance(block, dict):
        return None
    value = block.get("value")
    if value is None:
        return None
    text = strip_html(str(value))
    return text or None


def credit_from_commons_payload(payload: Mapping[str, Any], *, source_binary: str | None = None) -> Credit | None:
    """Parse a Commons API ``action=query`` payload into a ``Credit``."""
    pages = (payload.get("query") or {}).get("pages") or {}
    if not isinstance(pages, dict):
        return None
    page = next(iter(pages.values()), None)
    if not isinstance(page, dict) or page.get("missing") is not None:
        return None
    infos = page.get("imageinfo") or []
    if not infos or not isinstance(infos[0], dict):
        return None
    info = infos[0]
    ext = info.get("extmetadata") or {}
    if not isinstance(ext, dict):
        ext = {}
    source = info.get("descriptionurl") or None
    binary = info.get("url") or source_binary
    title = _ext_value(ext, "ObjectName") or _ext_value(ext, "ImageDescription")
    author = _ext_value(ext, "Artist")
    license_short = _ext_value(ext, "LicenseShortName")
    license_url = _ext_value(ext, "LicenseUrl")
    license_id = license_id_from_short_name(license_short)
    status = "public-domain" if license_id in {"PD", "CC0-1.0"} else "third-party"
    return Credit(
        status=status,
        title=title,
        author=author,
        source=source,
        source_binary=binary,
        license=license_id,
        license_url=license_url,
        origin="yaml",
    )


def default_fetch(file_title: str, timeout: float = 20.0) -> dict[str, Any]:
    """Query the Commons API for ``File:...`` metadata."""
    title = file_title if file_title.startswith("File:") else f"File:{file_title}"
    query = f"{COMMONS_API}?action=query&format=json" f"&prop=imageinfo&iiprop=url|extmetadata" f"&titles={quote(title)}"
    request = Request(query, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:
        parsed = json.loads(response.read().decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("Commons API returned a non-object JSON payload")
    return parsed


def yaml_is_complete(credit: Credit | None) -> bool:
    """True when an existing sidecar already has title and license (skip unless ``--force``)."""
    if credit is None:
        return False
    return bool(credit.title and credit.license)


def credit_to_yaml_mapping(credit: Credit) -> dict[str, Any]:
    """Serialise a credit for ``.credit.yml`` (omit empty and internal fields)."""
    mapping = asdict(credit)
    mapping.pop("origin", None)
    if not mapping.get("show_own"):
        mapping.pop("show_own", None)
    if not mapping.get("modifications"):
        mapping.pop("modifications", None)
    return {key: value for key, value in mapping.items() if value not in (None, "", [])}


def write_credit_yaml(path: str, credit: Credit) -> None:
    """Write a sidecar YAML file."""
    payload = credit_to_yaml_mapping(credit)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        yaml.safe_dump(payload, handle, sort_keys=False, allow_unicode=True)


def iter_url_sidecars(diagramsdir: str) -> Iterable[tuple[str, str]]:
    """Yield ``(stem, url_path)`` for every ``.url`` file under ``diagramsdir``."""
    for root, _dirs, files in os.walk(diagramsdir):
        for name in files:
            if not name.endswith(".url"):
                continue
            url_path = os.path.join(root, name)
            rel = os.path.relpath(url_path, diagramsdir)
            stem = rel[: -len(".url")]
            yield stem.replace("\\", "/"), url_path


def plan_backfill(
    diagramsdir: str,
    *,
    force: bool = False,
    fetch: FetchFn | None = None,
) -> list[tuple[str, Credit | None, str]]:
    """Return ``(yaml_path, credit_or_none, action)`` for each ``.url`` file.

    ``action`` is ``write``, ``skip-complete``, ``skip-other``, or ``skip-error``.
    """
    fetch_fn = fetch or (lambda title: default_fetch(title))
    plans: list[tuple[str, Credit | None, str]] = []
    for stem, url_path in iter_url_sidecars(diagramsdir):
        yaml_path = os.path.join(diagramsdir, stem + ".credit.yml")
        existing = load_credit_yaml(yaml_path)
        if yaml_is_complete(existing) and not force:
            plans.append((yaml_path, existing, "skip-complete"))
            continue
        url_credit = load_url_sidecar(url_path)
        source_url = (url_credit.source if url_credit else None) or ""
        kind = classify_source_url(source_url)
        if kind == "other":
            plans.append((yaml_path, None, "skip-other"))
            continue
        filename = filename_from_url(source_url)
        if kind == "wikipedia-en":
            wiki_source = f"https://en.wikipedia.org/wiki/File:{filename}" if filename else source_url
            credit = Credit(
                status="fair-use",
                source=wiki_source,
                source_binary=source_url if _url_hostname(source_url) == "upload.wikimedia.org" else None,
                origin="yaml",
            )
            plans.append((yaml_path, credit, "write"))
            continue
        if not filename:
            plans.append((yaml_path, None, "skip-error"))
            continue
        try:
            payload = fetch_fn(f"File:{filename}")
            parsed_credit = credit_from_commons_payload(payload, source_binary=source_url)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, OSError, ValueError, KeyError):
            plans.append((yaml_path, None, "skip-error"))
            continue
        if parsed_credit is None:
            plans.append((yaml_path, None, "skip-error"))
            continue
        plans.append((yaml_path, parsed_credit, "write"))
    return plans


def run_backfill(
    diagramsdir: str,
    *,
    dry_run: bool = False,
    force: bool = False,
    fetch: FetchFn | None = None,
) -> int:
    """Execute a backfill. Returns the number of YAML files written (or that would be)."""
    written = 0
    for yaml_path, credit, action in plan_backfill(diagramsdir, force=force, fetch=fetch):
        if action != "write" or credit is None:
            continue
        written += 1
        if not dry_run:
            write_credit_yaml(yaml_path, credit)
    return written


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backfill diagram .credit.yml sidecars from Wikimedia Commons (CIP-0016).",
    )
    parser.add_argument(
        "--diagrams-dir",
        required=True,
        help="Filesystem diagrams root containing .url sidecars",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes without creating YAML files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite YAML files that already have title and license",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    diagramsdir = os.path.abspath(args.diagrams_dir)
    if not os.path.isdir(diagramsdir):
        print(f"Diagrams directory not found: {diagramsdir}", file=sys.stderr)
        return 1
    plans = plan_backfill(diagramsdir, force=args.force)
    written = 0
    for yaml_path, credit, action in plans:
        rel = os.path.relpath(yaml_path, diagramsdir)
        if action == "write" and credit is not None:
            written += 1
            print(f"write {rel} [{credit.status}] {credit.title or credit.source or ''}")
            if not args.dry_run:
                write_credit_yaml(yaml_path, credit)
        else:
            print(f"{action} {rel}")
    if args.dry_run:
        print(f"Dry run: {written} file(s) would be written.")
    else:
        print(f"Wrote {written} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
