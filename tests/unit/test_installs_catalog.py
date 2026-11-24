"""Tests for the shared install package catalog (CIP-001C)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from lamd.installs import PACKAGES_JSON, PACKAGES_YML, load_packages, load_packages_json, load_packages_yaml, resolve_spec


def test_yaml_and_json_catalogs_match() -> None:
    yml = load_packages_yaml(PACKAGES_YML)
    js = load_packages_json(PACKAGES_JSON)
    assert yml == js
    assert "pods" in yml
    assert yml["pods"].startswith("git+https://github.com/lawrennd/ods.git")


def test_load_packages_default() -> None:
    packages = load_packages()
    assert packages["GPy"] == "gpy>=1.15"
    assert packages["mlai"].startswith("git+")


def test_load_packages_overrides() -> None:
    packages = load_packages(overrides={"pods": "pods>=0.1.20"})
    assert packages["pods"] == "pods>=0.1.20"
    assert packages["GPy"] == "gpy>=1.15"


def test_resolve_spec_known_and_unknown() -> None:
    packages = load_packages()
    assert resolve_spec("pods", packages) == packages["pods"]
    assert resolve_spec("seaborn", packages) == "seaborn"


def test_env_json_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "packages.json"
    path.write_text(
        json.dumps({"packages": {"pods": "pods==9.9.9", "GPy": "gpy>=1.15"}}),
        encoding="utf-8",
    )
    monkeypatch.setenv("LAMD_PACKAGES_JSON", str(path))
    monkeypatch.delenv("LAMD_PACKAGES_YML", raising=False)
    assert load_packages()["pods"] == "pods==9.9.9"


def test_yaml_file_parses_with_pyyaml() -> None:
    data = yaml.safe_load(PACKAGES_YML.read_text(encoding="utf-8"))
    assert set(data["packages"]) == set(load_packages_json())
