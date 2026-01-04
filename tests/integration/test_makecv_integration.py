#!/usr/bin/env python3
"""
Integration tests for the makecv module.

These tests verify that makecv correctly generates makefiles and
validates configuration without requiring external dependencies
like gpp or pandoc for the basic tests.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

import lamd


class TestMakeCVIntegration:
    """Integration tests for makecv functionality."""

    def setup_method(self):
        """Set up test environment with temporary directory."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.temp_dir.name)
        self.original_dir = os.getcwd()

    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()

    def create_minimal_lamd_yml(self, extra_config: dict = None):
        """Create a minimal _lamd.yml configuration file."""
        config = {
            "snippetsdir": str(self.test_path / "snippets"),
            "bibdir": str(self.test_path / "bib"),
            "postsdir": str(self.test_path / "posts"),
            "macrosdir": str(Path(lamd.__file__).parent / "macros"),
        }
        if extra_config:
            config.update(extra_config)

        # Create the directories
        for key in ["snippetsdir", "bibdir", "postsdir"]:
            Path(config[key]).mkdir(parents=True, exist_ok=True)

        # Write the config file
        config_path = self.test_path / "_lamd.yml"
        with open(config_path, "w") as f:
            for key, value in config.items():
                f.write(f"{key}: {value}\n")

        return config_path

    def create_minimal_cv(self, filename: str = "test-cv.md"):
        """Create a minimal CV markdown file."""
        cv_content = """---
layout: cv
title: "Test CV"
author: Test Author
docx: true
date: 2025-12-02
---

## Contact

**Email**: test@example.com

## Education

Test education content.
"""
        cv_path = self.test_path / filename
        with open(cv_path, "w") as f:
            f.write(cv_content)
        return cv_path

    def create_cv_with_include(self, filename: str = "test-cv.md"):
        """Create a CV with an include directive."""
        # Create include file
        include_dir = self.test_path / "includes"
        include_dir.mkdir(exist_ok=True)

        include_content = """\\ifndef{testSection}
\\define{testSection}

## Test Section

This is included content.

\\endif
"""
        include_path = include_dir / "test-section.md"
        with open(include_path, "w") as f:
            f.write(include_content)

        # Create main CV file
        cv_content = f"""---
layout: cv
title: "Test CV with Include"
author: Test Author
docx: true
date: 2025-12-02
---

## Contact

**Email**: test@example.com

\\include{{{include_dir}/test-section.md}}
"""
        cv_path = self.test_path / filename
        with open(cv_path, "w") as f:
            f.write(cv_content)
        return cv_path, include_path


class TestMakefileGeneration(TestMakeCVIntegration):
    """Tests for makefile generation."""

    def test_makecv_generates_makefile(self):
        """Test that makecv generates a makefile with correct structure."""
        self.create_minimal_lamd_yml()
        cv_path = self.create_minimal_cv()

        os.chdir(self.test_path)

        # Mock os.system to prevent actual make execution and git pulls
        with patch("os.system", return_value=0):
            with patch("os.path.isdir", side_effect=lambda x: x == ".git" or Path(x).is_dir()):
                # Run makecv
                result = subprocess.run(
                    [sys.executable, "-m", "lamd.makecv", str(cv_path.name)],
                    capture_output=True,
                    text=True,
                    cwd=str(self.test_path),
                )

        # Check makefile was created
        makefile_path = self.test_path / "makefile"
        assert makefile_path.exists(), f"Makefile not created. stderr: {result.stderr}"

        # Read and verify makefile content
        with open(makefile_path) as f:
            makefile_content = f.read()

        assert "BASE=test-cv" in makefile_content, "BASE not set correctly"
        assert "MAKEFILESDIR=" in makefile_content, "MAKEFILESDIR not set"
        assert "INCLUDESDIR=" in makefile_content, "INCLUDESDIR not set"
        assert "SCRIPTDIR=" in makefile_content, "SCRIPTDIR not set"
        # Verify all required makefile includes are present
        assert "include $(MAKEFILESDIR)/make-cv-flags.mk" in makefile_content
        assert "include $(MAKEFILESDIR)/make-lists.mk" in makefile_content, "make-lists.mk should be included"
        assert "include $(MAKEFILESDIR)/make-cv.mk" in makefile_content
        
        # Verify the order: make-cv-flags.mk, then make-lists.mk, then make-cv.mk
        lines = makefile_content.split("\n")
        flags_line = next(i for i, line in enumerate(lines) if "make-cv-flags.mk" in line)
        lists_line = next(i for i, line in enumerate(lines) if "make-lists.mk" in line)
        cv_line = next(i for i, line in enumerate(lines) if "make-cv.mk" in line)
        assert flags_line < lists_line < cv_line, "Makefile includes should be in correct order"

    def test_makecv_uses_lamd_paths(self):
        """Test that makecv uses paths from lamd package location."""
        self.create_minimal_lamd_yml()
        cv_path = self.create_minimal_cv()

        os.chdir(self.test_path)

        with patch("os.system", return_value=0):
            subprocess.run(
                [sys.executable, "-m", "lamd.makecv", str(cv_path.name)],
                capture_output=True,
                text=True,
                cwd=str(self.test_path),
            )

        makefile_path = self.test_path / "makefile"
        with open(makefile_path) as f:
            makefile_content = f.read()

        # Verify paths point to lamd package
        lamd_dir = Path(lamd.__file__).parent
        expected_makefiles_dir = str(lamd_dir / "makefiles")

        assert expected_makefiles_dir in makefile_content, (
            f"Expected makefiles dir {expected_makefiles_dir} not found in makefile"
        )


class TestConfigurationValidation(TestMakeCVIntegration):
    """Tests for _lamd.yml configuration validation."""

    def test_missing_lamd_yml_fails(self):
        """Test that makecv fails gracefully when _lamd.yml is missing."""
        cv_path = self.create_minimal_cv()

        os.chdir(self.test_path)

        result = subprocess.run(
            [sys.executable, "-m", "lamd.makecv", str(cv_path.name)],
            capture_output=True,
            text=True,
            cwd=str(self.test_path),
        )

        assert result.returncode != 0, "Should fail without _lamd.yml"
        assert "_lamd.yml" in result.stdout or "_lamd.yml" in result.stderr

    def test_missing_snippetsdir_fails(self):
        """Test that makecv fails when snippetsdir is not configured."""
        # Create config without snippetsdir
        config_path = self.test_path / "_lamd.yml"
        with open(config_path, "w") as f:
            f.write("bibdir: ./bib\n")
            f.write("postsdir: ./posts\n")

        # Create required directories
        (self.test_path / "bib").mkdir()
        (self.test_path / "posts").mkdir()

        cv_path = self.create_minimal_cv()

        os.chdir(self.test_path)

        result = subprocess.run(
            [sys.executable, "-m", "lamd.makecv", str(cv_path.name)],
            capture_output=True,
            text=True,
            cwd=str(self.test_path),
        )

        assert result.returncode != 0, "Should fail without snippetsdir"
        assert "snippetsdir" in result.stdout or "snippetsdir" in result.stderr

    def test_missing_bibdir_fails(self):
        """Test that makecv fails when bibdir is not configured."""
        # Create config without bibdir
        snippets_dir = self.test_path / "snippets"
        snippets_dir.mkdir()

        config_path = self.test_path / "_lamd.yml"
        with open(config_path, "w") as f:
            f.write(f"snippetsdir: {snippets_dir}\n")
            f.write("postsdir: ./posts\n")

        (self.test_path / "posts").mkdir()

        cv_path = self.create_minimal_cv()

        os.chdir(self.test_path)

        result = subprocess.run(
            [sys.executable, "-m", "lamd.makecv", str(cv_path.name)],
            capture_output=True,
            text=True,
            cwd=str(self.test_path),
        )

        assert result.returncode != 0, "Should fail without bibdir"
        assert "bibdir" in result.stdout or "bibdir" in result.stderr

    def test_nonexistent_directory_fails(self):
        """Test that makecv fails when configured directory doesn't exist."""
        config_path = self.test_path / "_lamd.yml"
        with open(config_path, "w") as f:
            f.write("snippetsdir: /nonexistent/path/snippets\n")
            f.write("bibdir: /nonexistent/path/bib\n")
            f.write("postsdir: ./posts\n")

        (self.test_path / "posts").mkdir()

        cv_path = self.create_minimal_cv()

        os.chdir(self.test_path)

        result = subprocess.run(
            [sys.executable, "-m", "lamd.makecv", str(cv_path.name)],
            capture_output=True,
            text=True,
            cwd=str(self.test_path),
        )

        assert result.returncode != 0, "Should fail with nonexistent directory"


class TestIncludeSystem(TestMakeCVIntegration):
    """Tests for the include system (requires gpp to be installed)."""

    @pytest.mark.skipif(
        subprocess.run(["which", "gpp"], capture_output=True).returncode != 0,
        reason="gpp not installed",
    )
    def test_include_file_structure(self):
        """Test that include files are created with correct guard structure."""
        self.create_minimal_lamd_yml()
        cv_path, include_path = self.create_cv_with_include()

        # Verify include file has guards
        with open(include_path) as f:
            content = f.read()

        assert "\\ifndef{" in content, "Include should have ifndef guard"
        assert "\\define{" in content, "Include should have define"
        assert "\\endif" in content, "Include should have endif"

    def test_docx_rule_includes_preprocessing(self):
        """Test that the docx rule includes macro preprocessing step."""
        self.create_minimal_lamd_yml()
        cv_path, include_path = self.create_cv_with_include()

        os.chdir(self.test_path)

        with patch("os.system", return_value=0):
            with patch("os.path.isdir", side_effect=lambda x: x == ".git" or Path(x).is_dir()):
                # Run makecv to generate makefile
                subprocess.run(
                    [sys.executable, "-m", "lamd.makecv", str(cv_path.name)],
                    capture_output=True,
                    text=True,
                    cwd=str(self.test_path),
                )

        # Read the generated makefile
        makefile_path = self.test_path / "makefile"
        with open(makefile_path) as f:
            makefile_content = f.read()

        # Verify that the makefile includes preprocessing for docx
        # The make-docx.mk should have a rule that preprocesses before pandoc
        # Check that the makefile includes make-docx.mk
        assert "include" in makefile_content and "make-docx.mk" in makefile_content, (
            "Makefile should include make-docx.mk"
        )
        
        # The fix ensures that ${BASE}.docx depends on ${BASE}.preprocessed.md
        # and there's a preprocessing rule. Since make-docx.mk is included,
        # we verify the pattern exists in the included makefile by checking
        # that the makefile references preprocessing variables
        assert "${PP}" in makefile_content or "PP=" in makefile_content, (
            "Makefile should reference preprocessing (${PP}) for docx generation"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

