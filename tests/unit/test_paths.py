"""Unit tests for lamd.paths (CIP-0010)."""

import os
import sys
import tempfile
import warnings

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lamd.paths import (  # noqa: E402
    join_url,
    load_config,
    looks_like_url,
    normalise_path,
    resolve_diagrams_filesystem,
    resolve_diagrams_web,
    validate_diagrams_root,
    warn_if_diagramsdir_is_url,
)


class TestNormalisePath:
    def test_resolves_relative_to_base(self):
        base = "/project/_lamd"
        assert normalise_path("../slides/diagrams/", base) == os.path.normpath(
            "/project/_lamd/../slides/diagrams"
        )

    def test_collapses_duplicate_slashes(self):
        base = "/project/_lamd"
        assert normalise_path("./slides//diagrams/", base) == os.path.normpath(
            "/project/_lamd/slides/diagrams"
        )

    def test_expands_environment_variables(self, monkeypatch):
        monkeypatch.setenv("LAMD_TEST_ROOT", "/tmp/lamd-test")
        assert normalise_path("$LAMD_TEST_ROOT/diagrams", "/ignored") == os.path.normpath(
            "/tmp/lamd-test/diagrams"
        )

    def test_leaves_urls_unchanged(self):
        url = "https://example.org/course/slides/diagrams/"
        assert normalise_path(url, "/any/cwd") == url


class TestResolveDiagramsFilesystem:
    def test_cli_override_wins(self):
        config = {"diagramsdir": "../slides/diagrams/"}
        assert resolve_diagrams_filesystem(config, cwd="/build/_lamd", cli="/override/diagrams") == os.path.normpath(
            "/override/diagrams"
        )

    def test_pattern_b_mlfc(self):
        config = {"diagramsdir": "../slides/diagrams/"}
        cwd = os.path.join("/repo", "mlfc", "_lamd")
        assert resolve_diagrams_filesystem(config, cwd=cwd) == os.path.normpath(
            os.path.join(cwd, "../slides/diagrams")
        )

    def test_pattern_a_wrong_under_lamd(self):
        config = {"diagramsdir": "./slides/diagrams/"}
        cwd = os.path.join("/repo", "advds", "_lamd")
        resolved = resolve_diagrams_filesystem(config, cwd=cwd)
        assert resolved == os.path.normpath(os.path.join(cwd, "slides/diagrams"))
        assert resolved.endswith(os.path.join("_lamd", "slides", "diagrams"))

    def test_warns_when_diagramsdir_is_url(self):
        config = {"diagramsdir": "https://example.org/diagrams/"}
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            resolve_diagrams_filesystem(config, cwd="/tmp")
        assert len(caught) == 1
        assert "diagramsurl" in str(caught[0].message)


class TestResolveDiagramsWeb:
    def test_diagramsurl_override(self):
        config = {
            "url": "https://mlatcl.github.io/",
            "baseurl": "mlfc/",
            "diagramsdir": "../slides/diagrams/",
            "diagramsurl": "https://mlatcl.github.io/mlfc/slides/diagrams/",
        }
        assert resolve_diagrams_web(config, cwd="/repo/mlfc/_lamd") == config["diagramsurl"]

    def test_diagramswebpath_fallback(self):
        config = {
            "url": "https://mlatcl.github.io/",
            "baseurl": "mlfc/",
            "diagramsdir": "../slides/diagrams/",
            "diagramswebpath": "slides/diagrams/",
        }
        assert resolve_diagrams_web(config, cwd="/repo/mlfc/_lamd") == "https://mlatcl.github.io/mlfc/slides/diagrams"

    def test_basename_fallback(self):
        config = {
            "url": "https://mlatcl.github.io/",
            "baseurl": "mlfc/",
            "diagramsdir": "../slides/diagrams/",
        }
        assert resolve_diagrams_web(config, cwd="/repo/mlfc/_lamd") == "https://mlatcl.github.io/mlfc/diagrams"

    def test_cli_web_override(self):
        config = {"diagramsdir": "../slides/diagrams/"}
        assert resolve_diagrams_web(config, cli_web="https://preview.local/diagrams/") == "https://preview.local/diagrams/"

    def test_cli_fs_override_for_local_html_preview(self):
        config = {
            "url": "https://example.org/",
            "baseurl": "talks/",
            "diagramsdir": "../slides/diagrams/",
        }
        assert resolve_diagrams_web(
            config,
            cwd="/talks/_ml",
            cli_fs="../slides/diagrams/",
        ) == os.path.normpath("/talks/_ml/../slides/diagrams")


class TestJoinUrl:
    def test_joins_without_duplicate_slashes(self):
        assert join_url("https://example.org/", "course/", "slides/diagrams/") == "https://example.org/course/slides/diagrams"


class TestValidateDiagramsRoot:
    def test_raises_for_missing_directory(self):
        with pytest.raises(FileNotFoundError, match="Diagrams directory not found"):
            validate_diagrams_root("/nonexistent/diagrams/path", cwd="/tmp")

    def test_passes_for_existing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            validate_diagrams_root(tmp, cwd=tmp)

    def test_skips_url_paths(self):
        validate_diagrams_root("https://example.org/diagrams/", cwd="/tmp")


class TestLoadConfig:
    def test_loads_from_lamd_yml(self):
        with tempfile.TemporaryDirectory() as tmp:
            lamd_dir = os.path.join(tmp, "_lamd")
            os.makedirs(lamd_dir)
            with open(os.path.join(lamd_dir, "_lamd.yml"), "w") as handle:
                handle.write(
                    "diagramsdir: ../slides/diagrams/\n"
                    "diagramswebpath: slides/diagrams/\n"
                    "url: https://example.org/\n"
                    "baseurl: course/\n"
                )
            config = load_config(lamd_dir)
            assert config["diagramsdir"] == "../slides/diagrams/"
            assert config["diagramswebpath"] == "slides/diagrams/"


class TestLooksLikeUrl:
    @pytest.mark.parametrize(
        "value,expected",
        [
            ("https://example.org/", True),
            ("http://localhost/diagrams", True),
            ("../slides/diagrams/", False),
            ("diagrams", False),
        ],
    )
    def test_detection(self, value, expected):
        assert looks_like_url(value) is expected
