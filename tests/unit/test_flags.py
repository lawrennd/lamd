"""
Unit tests for the flags module.
"""

import os
import sys
import tempfile
from datetime import date
from unittest.mock import MagicMock, patch

import pytest

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import lynguine.util.yaml as ny

from lamd.flags import main


class TestFlags:
    """Test suite for the flags module."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a test markdown file with YAML front matter - use raw string to avoid escape issues
        self.test_md_content = r"""---
title: Test Document
layout: talk
date: 2023-05-15
week: 3
session: 2
practical: 1
topic: 5
background: 2
reveal: true
docx: true
pptx: true
ipynb: true
slidesipynb: true
notespdf: true
pdf: true
---

# Test Content

This is test content.
"""
        self.test_md_path = os.path.join(self.temp_dir.name, "test.md")
        with open(self.test_md_path, "w") as f:
            f.write(self.test_md_content)

        # Create a config file for testing
        self.config_content = """
dotx: path/to/reference.dotx
potx: path/to/presentation.potx
revealjs_url: https://example.com/reveal.js
talktheme: white
talkcss: path/to/custom.css
ghub:
  organization: testorg
  repository: testrepo
  branch: main
  directory: docs
"""
        self.config_path = os.path.join(self.temp_dir.name, "_lamd.yml")
        with open(self.config_path, "w") as f:
            f.write(self.config_content)

    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory and its contents
        self.temp_dir.cleanup()

    def _setup_common_mocks(self, mock_field):
        """Set up common mock behavior for all required fields."""

        def mock_header_field(field, *args, **kwargs):
            if field == "date":
                return date(2023, 5, 15)
            elif field == "layout":
                return "talk"
            elif field == "week":
                return 3
            elif field == "topic":
                return 5
            elif field == "session":
                return 2
            elif field == "practical":
                return 1
            elif field == "background":
                return 2
            elif field == "revealjs_url":
                return "https://example.com/reveal.js"
            elif field == "talktheme":
                return "white"
            elif field == "talkcss":
                return "path/to/custom.css"
            elif field == "dotx":
                return "path/to/reference.dotx"
            elif field == "potx":
                return "path/to/presentation.potx"
            elif field in ["docx", "pptx", "reveal", "ipynb", "slidesipynb", "notespdf", "pdf"]:
                return True
            elif field == "assignment":
                return True
            elif field == "ghub":
                return [{"organization": "testorg", "repository": "testrepo", "branch": "main", "directory": "docs"}]
            # Return None for any other field to trigger FileFormatError
            return None

        mock_field.side_effect = mock_header_field

    @patch("sys.argv", ["flags", "prefix", "test"])
    @patch("builtins.print")
    def test_prefix_output(self, mock_print):
        """Test the prefix output option."""
        # Setup mock for header_fields and header_field
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Set up common mocks
                self._setup_common_mocks(mock_field)

                # Call the main function
                main()

                # Check that print was called with the expected prefix
                mock_print.assert_called_once_with("2023-05-15-")

    @patch("sys.argv", ["flags", "post", "test"])
    @patch("builtins.print")
    def test_post_output(self, mock_print):
        """Test the post output option with various metadata fields."""
        # Setup mocks
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Set up common mocks
                self._setup_common_mocks(mock_field)

                # Call the main function
                main()

                # Check output contains expected metadata
                args, kwargs = mock_print.call_args
                output = args[0]

                assert "--metadata date=2023-05-15" in output
                assert "--metadata docx=2023-05-15-test.docx" in output
                assert "--metadata pptx=2023-05-15-test.pptx" in output
                assert "--metadata reveal=2023-05-15-test.slides.html" in output
                assert "--metadata ipynb=2023-05-15-test.ipynb" in output
                assert "--metadata layout=talk" in output
                assert "--metadata week=3" in output
                assert "--metadata topic=5" in output
                assert "--metadata session=2" in output
                assert "--metadata practical=1" in output
                assert "--metadata edit_url=https://github.com/testorg/testrepo/edit/main/docs/test.md" in output

    @patch("sys.argv", ["flags", "docx", "test"])
    @patch("builtins.print")
    def test_docx_output(self, mock_print):
        """Test the docx output option."""
        # Setup mocks
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Set up common mocks
                self._setup_common_mocks(mock_field)

                # Call the main function
                main()

                # Check output has reference doc
                mock_print.assert_called_once_with("--reference-doc path/to/reference.dotx")

    @patch("sys.argv", ["flags", "pptx", "test"])
    @patch("builtins.print")
    def test_pptx_output(self, mock_print):
        """Test the pptx output option."""
        # Setup mocks
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Set up common mocks
                self._setup_common_mocks(mock_field)

                # Call the main function
                main()

                # Check output has reference doc
                mock_print.assert_called_once_with("--reference-doc path/to/presentation.potx")

    @patch("sys.argv", ["flags", "reveal", "test"])
    @patch("builtins.print")
    def test_reveal_output(self, mock_print):
        """Test the reveal output option."""
        # Setup mocks
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Set up common mocks
                self._setup_common_mocks(mock_field)

                # Call the main function
                main()

                # Check output has reveal.js settings
                args, kwargs = mock_print.call_args
                output = args[0]

                assert "--slide-level 2" in output
                assert "--variable revealjs-url=https://example.com/reveal.js" in output
                assert "--variable theme=white" in output
                assert "--css path/to/custom.css" in output

    @patch("sys.argv", ["flags", "pp", "test"])
    @patch("builtins.print")
    def test_pp_output(self, mock_print):
        """Test the preprocessor output option."""
        # Setup mocks
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Set up common mocks
                self._setup_common_mocks(mock_field)

                # Call the main function
                main()

                # Check output has preprocessor flags
                args, kwargs = mock_print.call_args
                output = args[0]

                assert "--include-path ./.." in output
                assert "--assignment" in output

    @patch("sys.argv", ["flags", "cv", "test"])
    @patch("builtins.print")
    def test_cv_output(self, mock_print):
        """Test the CV output option."""
        # Setup mocks
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Set up common mocks
                self._setup_common_mocks(mock_field)

                # This option is not implemented yet, but should not error
                main()

                # Nothing should be printed for CV output option
                # Just check that the function was called
                assert mock_print.call_count == 0

    @patch("sys.argv", ["flags", "reveal", "test"])
    @patch("builtins.print")
    def test_default_values_for_reveal(self, mock_print):
        """Test that default values are used when fields are missing for reveal output."""
        # Setup mocks
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Configure mock to raise FileFormatError for most fields
                def mock_header_field(field, *args, **kwargs):
                    if field == "layout":
                        return "talk"
                    # Return None to trigger FileFormatError for everything else
                    raise ny.FileFormatError(f"Field not found: {field}")

                mock_field.side_effect = mock_header_field

                # Call the main function
                main()

                # Check output has default values
                args, kwargs = mock_print.call_args
                output = args[0]

                assert "--variable revealjs-url=https://unpkg.com/reveal.js@3.9.2" in output
                assert "--variable theme=black" in output
                assert "--css https://inverseprobability.com/assets/css/talks.css" in output

    @patch("sys.argv", ["flags", "prefix", "test"])
    @patch("builtins.print")
    def test_default_values_for_prefix(self, mock_print):
        """Test that empty prefix is used when date is missing."""
        # Setup mocks
        with patch("lynguine.util.yaml.header_fields", return_value={}):
            with patch("lynguine.util.yaml.header_field") as mock_field:
                # Configure mock to raise FileFormatError for most fields
                def mock_header_field(field, *args, **kwargs):
                    if field == "layout":
                        return "talk"
                    # Return None to trigger FileFormatError for everything else
                    raise ny.FileFormatError(f"Field not found: {field}")

                mock_field.side_effect = mock_header_field

                # Call the main function
                main()

                # Check that an empty prefix is returned when date is missing
                mock_print.assert_called_once_with("")
