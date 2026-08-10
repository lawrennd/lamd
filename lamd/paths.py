#!/usr/bin/env python3
"""Unified path resolution for LaMD builds (CIP-0010).

Separates filesystem diagram roots from web URL prefixes used in HTML/ipynb.
"""

from __future__ import annotations

import argparse
import os
import sys
import warnings
from typing import Mapping, MutableMapping

import lynguine.util.yaml as ny

DEFAULT_DIAGRAMS_DIR = "diagrams"


def get_build_cwd(explicit: str | None = None) -> str:
    """Return the build working directory (anchor for relative paths)."""
    return os.path.abspath(explicit or os.getcwd())


def _expand(value: str) -> str:
    return os.path.expandvars(value)


def looks_like_url(value: str) -> bool:
    """Return True if value appears to be an HTTP(S) URL."""
    lowered = value.lower()
    return lowered.startswith("http://") or lowered.startswith("https://")


def normalise_path(path: str, base: str) -> str:
    """Normalise a filesystem path relative to base.

    Expands environment variables, resolves ``.`` and ``..``, and collapses
    duplicate separators. URL-like paths are returned unchanged.
    """
    expanded = _expand(path)
    if looks_like_url(expanded):
        return expanded
    if os.path.isabs(expanded):
        return os.path.normpath(expanded)
    return os.path.normpath(os.path.join(base, expanded))


def join_url(*parts: str) -> str:
    """Join URL path segments without duplicating slashes."""
    if not parts:
        return ""
    result = parts[0].rstrip("/")
    for part in parts[1:]:
        segment = part.strip("/")
        if segment:
            result = f"{result}/{segment}"
    return result


def path_config_from_mapping(mapping: Mapping[str, object]) -> dict[str, str]:
    """Extract path-related config keys from an interface mapping."""
    return {
        "diagramsdir": "" if mapping.get("diagramsdir") is None else str(mapping.get("diagramsdir", DEFAULT_DIAGRAMS_DIR)),
        "diagramsurl": "" if mapping.get("diagramsurl") is None else str(mapping.get("diagramsurl", "")),
        "diagramswebpath": "" if mapping.get("diagramswebpath") is None else str(mapping.get("diagramswebpath", "")),
        "url": "" if mapping.get("url") is None else str(mapping.get("url", "")),
        "baseurl": "" if mapping.get("baseurl") is None else str(mapping.get("baseurl", "")),
    }


def warn_if_diagramsdir_is_url(config: Mapping[str, str]) -> None:
    """Warn when ``diagramsdir`` looks like a URL (filesystem-only after CIP-0010)."""
    diagramsdir = _expand(str(config.get("diagramsdir", DEFAULT_DIAGRAMS_DIR)))
    if looks_like_url(diagramsdir):
        warnings.warn(
            "diagramsdir looks like a URL; use diagramsurl for web paths "
            "(diagramsdir is filesystem-only after CIP-0010)",
            stacklevel=3,
        )


def resolve_diagrams_filesystem(
    config: Mapping[str, str],
    cwd: str | None = None,
    cli: str | None = None,
) -> str:
    """Resolve the filesystem root for diagram assets."""
    if cli:
        return normalise_path(cli, get_build_cwd(cwd))

    warn_if_diagramsdir_is_url(config)
    diagramsdir = str(config.get("diagramsdir", DEFAULT_DIAGRAMS_DIR))
    return normalise_path(diagramsdir, get_build_cwd(cwd))


def resolve_diagrams_web(
    config: Mapping[str, str],
    cwd: str | None = None,
    cli_fs: str | None = None,
    cli_web: str | None = None,
) -> str:
    """Resolve the web URL prefix for ``\\diagramsDir`` in HTML/ipynb output."""
    if cli_web:
        return _expand(cli_web)
    if cli_fs:
        return resolve_diagrams_filesystem(config, cwd=cwd, cli=cli_fs)

    diagramsurl = _expand(str(config.get("diagramsurl", ""))).strip()
    if diagramsurl:
        return diagramsurl

    url = _expand(str(config.get("url", "")))
    baseurl = _expand(str(config.get("baseurl", "")))
    prefix = join_url(url, baseurl)

    diagramswebpath = _expand(str(config.get("diagramswebpath", ""))).strip()
    if diagramswebpath:
        return join_url(prefix, diagramswebpath)

    fs_dir = resolve_diagrams_filesystem(config, cwd=cwd)
    web_suffix = os.path.basename(fs_dir) or DEFAULT_DIAGRAMS_DIR
    return join_url(prefix, web_suffix)


def validate_diagrams_root(path: str, *, cwd: str | None = None) -> None:
    """Raise FileNotFoundError when the resolved diagrams directory is missing."""
    build_cwd = get_build_cwd(cwd)
    if looks_like_url(path):
        return
    if os.path.isdir(path):
        return
    raise FileNotFoundError(
        f"Diagrams directory not found: {path!r} "
        f"(build cwd: {build_cwd!r}; check diagramsdir in _lamd.yml or --diagrams-dir)"
    )


def load_config(cwd: str = ".") -> dict[str, str]:
    """Load path-related keys from ``_lamd.yml`` / ``_config.yml`` in cwd."""
    defaults: MutableMapping[str, str] = {
        "diagramsdir": DEFAULT_DIAGRAMS_DIR,
        "diagramsurl": "",
        "diagramswebpath": "",
        "url": "",
        "baseurl": "",
    }
    try:
        iface = ny.Interface.from_file(["_lamd.yml", "_config.yml"], directory=cwd)
        for key in defaults:
            value = iface.get(key, defaults[key])
            defaults[key] = "" if value is None else str(value)
    except (ny.FileFormatError, OSError):
        pass
    return dict(defaults)


def build_arg_parser() -> argparse.ArgumentParser:
    """Argument parser for the ``lamd-resolve-diagrams-dir`` CLI."""
    parser = argparse.ArgumentParser(
        description="Resolve diagram directory paths from _lamd.yml (CIP-0010)",
    )
    parser.add_argument(
        "--filesystem",
        action="store_true",
        help="Print filesystem diagrams root (default)",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Print web URL prefix for HTML/ipynb",
    )
    parser.add_argument(
        "-d",
        "--diagrams-dir",
        type=str,
        help="Override filesystem diagrams root",
    )
    parser.add_argument(
        "--diagrams-web-dir",
        type=str,
        help="Override web diagrams URL prefix",
    )
    parser.add_argument(
        "--cwd",
        type=str,
        default=".",
        help="Build working directory (default: current directory)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point: print resolved filesystem or web diagrams path."""
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    config = load_config(args.cwd)
    use_web = args.web and not args.filesystem

    if use_web:
        path = resolve_diagrams_web(
            config,
            cwd=args.cwd,
            cli_fs=args.diagrams_dir,
            cli_web=args.diagrams_web_dir,
        )
    else:
        path = resolve_diagrams_filesystem(
            config,
            cwd=args.cwd,
            cli=args.diagrams_dir,
        )

    print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
