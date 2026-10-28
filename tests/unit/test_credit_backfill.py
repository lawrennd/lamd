"""Tests for CIP-0016 Commons credit backfill (no live HTTP)."""

from __future__ import annotations

import os

import yaml

from lamd.credit import load_credit_yaml
from lamd.credit_backfill import (
    classify_source_url,
    credit_from_commons_payload,
    filename_from_url,
    license_id_from_short_name,
    plan_backfill,
    run_backfill,
    strip_html,
)

FIXTURES = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "fixtures", "cip0016"))

COMMONS_PAYLOAD = {
    "query": {
        "pages": {
            "123": {
                "title": "File:Daniel Bernoulli.jpg",
                "imageinfo": [
                    {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Daniel_Bernoulli.jpg",
                        "descriptionurl": "https://commons.wikimedia.org/wiki/File:Daniel_Bernoulli.jpg",
                        "extmetadata": {
                            "ObjectName": {"value": "Portrait of Daniel Bernoulli"},
                            "Artist": {"value": '<a href="https://commons.wikimedia.org/wiki/User:Example">Huber</a>'},
                            "LicenseShortName": {"value": "CC BY-SA 4.0"},
                            "LicenseUrl": {"value": "https://creativecommons.org/licenses/by-sa/4.0"},
                        },
                    }
                ],
            }
        }
    }
}


def test_classify_source_url() -> None:
    assert classify_source_url("https://commons.wikimedia.org/wiki/File:Foo.jpg") == "commons"
    assert classify_source_url("https://upload.wikimedia.org/wikipedia/commons/a/ab/Foo.jpg") == "commons"
    assert classify_source_url("https://upload.wikimedia.org/wikipedia/en/a/a0/Cover.jpg") == "wikipedia-en"
    assert classify_source_url("https://www.flickr.com/photos/x/1") == "other"


def test_filename_from_url() -> None:
    assert filename_from_url("https://commons.wikimedia.org/wiki/File:Daniel_Bernoulli.jpg") == "Daniel_Bernoulli.jpg"
    assert (
        filename_from_url("https://upload.wikimedia.org/wikipedia/commons/d/d3/Daniel_Bernoulli.jpg") == "Daniel_Bernoulli.jpg"
    )


def test_license_id_from_short_name() -> None:
    assert license_id_from_short_name("CC BY-SA 4.0") == "CC-BY-SA-4.0"
    assert license_id_from_short_name("Public domain") == "PD"
    assert license_id_from_short_name("mystery") is None


def test_strip_html_artist() -> None:
    assert strip_html('<a href="https://example.org">Huber</a>') == "Huber"


def test_credit_from_commons_payload() -> None:
    credit = credit_from_commons_payload(COMMONS_PAYLOAD)
    assert credit is not None
    assert credit.status == "third-party"
    assert credit.title == "Portrait of Daniel Bernoulli"
    assert credit.author == "Huber"
    assert credit.source == "https://commons.wikimedia.org/wiki/File:Daniel_Bernoulli.jpg"
    assert credit.license == "CC-BY-SA-4.0"
    assert credit.license_url == "https://creativecommons.org/licenses/by-sa/4.0"


def test_plan_skips_flickr_and_complete_yaml(tmp_path) -> None:  # type: ignore[no-untyped-def]
    diagrams = tmp_path / "diagrams"
    diagrams.mkdir()
    (diagrams / "photo.url").write_text("https://www.flickr.com/photos/x/1\n", encoding="utf-8")
    (diagrams / "done.credit.yml").write_text(
        "status: third-party\ntitle: Already\nlicense: CC-BY-4.0\n",
        encoding="utf-8",
    )
    (diagrams / "done.url").write_text(
        "https://upload.wikimedia.org/wikipedia/commons/a/ab/Done.jpg\n",
        encoding="utf-8",
    )
    plans = {
        os.path.basename(path): action
        for path, _credit, action in plan_backfill(str(diagrams), fetch=lambda _t: COMMONS_PAYLOAD)
    }
    assert plans["photo.credit.yml"] == "skip-other"
    assert plans["done.credit.yml"] == "skip-complete"


def test_wikipedia_en_is_fair_use_not_cc(tmp_path) -> None:  # type: ignore[no-untyped-def]
    diagrams = tmp_path / "diagrams"
    diagrams.mkdir()
    (diagrams / "cover.url").write_text(
        "https://upload.wikimedia.org/wikipedia/en/a/a0/Example_cover.jpg\n",
        encoding="utf-8",
    )

    def fail_if_called(_title: str) -> dict:
        raise AssertionError("Wikipedia-en must not be queried as Commons CC")

    plans = plan_backfill(str(diagrams), fetch=fail_if_called)
    _path, credit, action = plans[0]
    assert action == "write"
    assert credit is not None
    assert credit.status == "fair-use"
    assert credit.license is None
    assert "en.wikipedia.org" in (credit.source or "")


def test_run_backfill_writes_yaml_from_mocked_commons(tmp_path) -> None:  # type: ignore[no-untyped-def]
    diagrams = tmp_path / "diagrams"
    diagrams.mkdir()
    (diagrams / "portrait.url").write_text(
        "https://upload.wikimedia.org/wikipedia/commons/d/d3/Daniel_Bernoulli.jpg\n",
        encoding="utf-8",
    )
    written = run_backfill(str(diagrams), fetch=lambda _t: COMMONS_PAYLOAD)
    assert written == 1
    yaml_path = diagrams / "portrait.credit.yml"
    credit = load_credit_yaml(str(yaml_path))
    assert credit is not None
    assert credit.license == "CC-BY-SA-4.0"
    assert credit.source.startswith("https://commons.wikimedia.org/wiki/File:")
    with open(yaml_path, encoding="utf-8") as handle:
        dumped = yaml.safe_load(handle)
    assert dumped["license"] != "CC-BY-SA-4.0" or "wikipedia/en" not in dumped.get("source_binary", "")


def test_dry_run_does_not_write(tmp_path) -> None:  # type: ignore[no-untyped-def]
    diagrams = tmp_path / "diagrams"
    diagrams.mkdir()
    (diagrams / "portrait.url").write_text(
        "https://upload.wikimedia.org/wikipedia/commons/d/d3/Daniel_Bernoulli.jpg\n",
        encoding="utf-8",
    )
    written = run_backfill(str(diagrams), dry_run=True, fetch=lambda _t: COMMONS_PAYLOAD)
    assert written == 1
    assert not (diagrams / "portrait.credit.yml").exists()


def test_force_overwrites_complete_yaml(tmp_path) -> None:  # type: ignore[no-untyped-def]
    diagrams = tmp_path / "diagrams"
    diagrams.mkdir()
    (diagrams / "portrait.url").write_text(
        "https://upload.wikimedia.org/wikipedia/commons/d/d3/Daniel_Bernoulli.jpg\n",
        encoding="utf-8",
    )
    (diagrams / "portrait.credit.yml").write_text(
        "status: third-party\ntitle: Old\nlicense: CC-BY-4.0\n",
        encoding="utf-8",
    )
    plans = plan_backfill(str(diagrams), force=True, fetch=lambda _t: COMMONS_PAYLOAD)
    assert plans[0][2] == "write"
    assert plans[0][1] is not None
    assert plans[0][1].title == "Portrait of Daniel Bernoulli"
