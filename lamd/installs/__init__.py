"""Shared install package catalog for lamd consumers.

The YAML file is the editable source of truth; ``packages.json`` is the
stdlib-safe twin used by talk ``\\installcode`` helpers and offline fallbacks.
Keep them in sync (see ``tests/unit/test_installs_catalog.py``).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Mapping, MutableMapping
from urllib.error import URLError
from urllib.request import urlopen

CATALOG_DIR = Path(__file__).resolve().parent
PACKAGES_YML = CATALOG_DIR / "packages.yml"
PACKAGES_JSON = CATALOG_DIR / "packages.json"

DEFAULT_CATALOG_YML_URL = "https://raw.githubusercontent.com/lawrennd/lamd/main/lamd/installs/packages.yml"
DEFAULT_CATALOG_JSON_URL = "https://raw.githubusercontent.com/lawrennd/lamd/main/lamd/installs/packages.json"


def _from_mapping(data: object) -> dict[str, str]:
    if not isinstance(data, dict):
        raise ValueError("catalog root must be a mapping")
    packages = data.get("packages", data)
    if not isinstance(packages, dict) or not packages:
        raise ValueError("catalog must contain a non-empty 'packages' mapping")
    out: dict[str, str] = {}
    for key, spec in packages.items():
        if not isinstance(key, str) or not isinstance(spec, str) or not spec.strip():
            raise ValueError(f"invalid catalog entry: {key!r}: {spec!r}")
        out[key] = spec.strip()
    return out


def load_packages_json(path: Path | None = None) -> dict[str, str]:
    """Load the JSON catalog (no third-party deps)."""
    if path is None:
        env = os.environ.get("LAMD_PACKAGES_JSON")
        path = Path(env) if env else PACKAGES_JSON
    return _from_mapping(json.loads(path.read_text(encoding="utf-8")))


def load_packages_yaml(path: Path | None = None) -> dict[str, str]:
    """Load the YAML catalog (requires PyYAML)."""
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover
        raise ImportError("PyYAML required to load packages.yml") from exc
    if path is None:
        env = os.environ.get("LAMD_PACKAGES_YML")
        path = Path(env) if env else PACKAGES_YML
    return _from_mapping(yaml.safe_load(path.read_text(encoding="utf-8")))


def fetch_packages_json(url: str | None = None, timeout: float = 5.0) -> dict[str, str]:
    """Fetch the JSON catalog from a URL (default: lamd main on GitHub)."""
    target = url or os.environ.get("LAMD_PACKAGES_JSON_URL", DEFAULT_CATALOG_JSON_URL)
    with urlopen(target, timeout=timeout) as response:  # noqa: S310 — curated URL
        return _from_mapping(json.loads(response.read().decode("utf-8")))


def load_packages(
    *,
    overrides: Mapping[str, str] | None = None,
    prefer_yaml: bool = False,
    fetch_remote: bool = False,
) -> dict[str, str]:
    """Resolve the package catalog with optional overrides.

    Order:
    1. ``LAMD_PACKAGES_YML`` / ``LAMD_PACKAGES_JSON`` env paths if set
    2. Packaged ``packages.yml`` (if ``prefer_yaml``) or ``packages.json``
    3. Optional remote JSON fetch when ``fetch_remote`` is true and local fails
    """
    packages: dict[str, str] | None = None
    errors: list[str] = []

    if "LAMD_PACKAGES_YML" in os.environ:
        try:
            packages = load_packages_yaml()
        except Exception as exc:  # noqa: BLE001 — collect and continue
            errors.append(str(exc))
    if packages is None and "LAMD_PACKAGES_JSON" in os.environ:
        try:
            packages = load_packages_json()
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    if packages is None and prefer_yaml and PACKAGES_YML.is_file():
        try:
            packages = load_packages_yaml(PACKAGES_YML)
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    if packages is None and PACKAGES_JSON.is_file():
        try:
            packages = load_packages_json(PACKAGES_JSON)
        except Exception as exc:  # noqa: BLE001
            errors.append(str(exc))

    if packages is None and fetch_remote:
        try:
            packages = fetch_packages_json()
        except (URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))

    if packages is None:
        detail = "; ".join(errors) if errors else "no catalog sources available"
        raise FileNotFoundError(f"could not load install package catalog: {detail}")

    if overrides:
        merged: MutableMapping[str, str] = dict(packages)
        for key, spec in overrides.items():
            if not isinstance(spec, str) or not spec.strip():
                raise ValueError(f"invalid override for {key!r}: {spec!r}")
            merged[key] = spec.strip()
        return dict(merged)
    return packages


def resolve_spec(name: str, packages: Mapping[str, str] | None = None) -> str:
    """Return the pip/uv requirement for ``name``, or ``name`` itself if unknown."""
    catalog = packages if packages is not None else load_packages()
    return catalog.get(name, name)
