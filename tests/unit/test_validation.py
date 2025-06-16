#!/usr/bin/env python3
"""
Tests for the validation module.
"""

import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from lamd.validation import (
    DependencyError,
    ValidationError,
    check_dependency,
    check_version,
    install_dependency,
    resolve_dependencies,
)


def test_check_dependency():
    """Test the check_dependency function."""
    with patch("shutil.which", return_value="/usr/bin/poetry"):
        assert check_dependency("poetry") is True

    with patch("shutil.which", return_value=None):
        assert check_dependency("nonexistent") is False


def test_check_version():
    """Test the check_version function."""
    with patch("subprocess.run", return_value=MagicMock(stdout="2.24", stderr="")):
        assert check_version("gpp", "2.24") is True

    with patch("subprocess.run", return_value=MagicMock(stdout="2.23", stderr="")):
        assert check_version("gpp", "2.24") is False

    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "gpp")):
        assert check_version("gpp", "2.24") is False


def test_resolve_dependencies_no_poetry():
    """Test resolve_dependencies when Poetry is not installed."""
    with patch("lamd.validation.check_dependency", return_value=False):
        with pytest.raises(DependencyError, match="Poetry is required"):
            resolve_dependencies({"gpp": "2.24"})


def test_resolve_dependencies_no_pyproject():
    """Test resolve_dependencies when not in a Poetry project."""
    with patch("lamd.validation.check_dependency", return_value=True), patch("os.path.exists", return_value=False):
        with pytest.raises(DependencyError, match="Not in a Poetry project"):
            resolve_dependencies({"gpp": "2.24"})


def test_resolve_dependencies_check_only():
    """Test resolve_dependencies in check-only mode."""
    mock_show_output = """
gpp 2.24
lynguine 0.1.0
"""
    with (
        patch("lamd.validation.check_dependency", return_value=True),
        patch("os.path.exists", return_value=True),
        patch("subprocess.run", return_value=MagicMock(stdout=mock_show_output, stderr="")),
    ):
        # Should not raise an exception
        resolve_dependencies({"gpp": "2.24", "lynguine": "0.1.0"})


def test_resolve_dependencies_missing_deps():
    """Test resolve_dependencies with missing dependencies."""
    mock_show_output = """
lynguine 0.1.0
"""
    with (
        patch("lamd.validation.check_dependency", return_value=True),
        patch("os.path.exists", return_value=True),
        patch("subprocess.run", return_value=MagicMock(stdout=mock_show_output, stderr="")),
    ):
        with pytest.raises(DependencyError, match="Missing or outdated dependencies"):
            resolve_dependencies({"gpp": "2.24", "lynguine": "0.1.0"})


def test_resolve_dependencies_auto_install():
    """Test resolve_dependencies with auto-install."""
    with (
        patch("lamd.validation.check_dependency", return_value=True),
        patch("os.path.exists", return_value=True),
        patch("subprocess.run") as mock_run,
    ):
        # Mock successful add and install
        mock_run.return_value = MagicMock(stdout="", stderr="")

        resolve_dependencies({"gpp": "2.24"}, auto_install=True)

        # Verify poetry commands were called
        assert mock_run.call_count == 2
        mock_run.assert_any_call(["poetry", "add", "gpp==2.24"], check=True, capture_output=True, text=True)
        mock_run.assert_any_call(["poetry", "install"], check=True, capture_output=True, text=True)


def test_resolve_dependencies_auto_install_failure():
    """Test resolve_dependencies with auto-install failure."""
    with (
        patch("lamd.validation.check_dependency", return_value=True),
        patch("os.path.exists", return_value=True),
        patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "poetry", stderr="Installation failed")),
    ):
        with pytest.raises(DependencyError, match="Failed to add dependency"):
            resolve_dependencies({"gpp": "2.24"}, auto_install=True)


def test_install_dependency():
    """Test install_dependency function."""
    with patch("lamd.validation.check_dependency", return_value=True), patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="", stderr="")

        install_dependency("gpp", "2.24")

        mock_run.assert_called_once_with(["poetry", "add", "gpp==2.24"], check=True, capture_output=True, text=True)


def test_install_dependency_no_poetry():
    """Test install_dependency when Poetry is not installed."""
    with patch("lamd.validation.check_dependency", return_value=False):
        with pytest.raises(DependencyError, match="Poetry is required"):
            install_dependency("gpp", "2.24")


def test_install_dependency_failure():
    """Test install_dependency with installation failure."""
    with (
        patch("lamd.validation.check_dependency", return_value=True),
        patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "poetry", stderr="Installation failed")),
    ):
        with pytest.raises(DependencyError, match="Failed to install"):
            install_dependency("gpp", "2.24")
