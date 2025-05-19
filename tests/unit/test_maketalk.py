"""
Unit tests for the maketalk module.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock, mock_open, call

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lamd.maketalk import main


class TestMaketalk:
    """Test suite for the maketalk module."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a test markdown file
        self.test_md_content = """---
title: Test Talk
author: Test Author
date: 2023-01-01
categories: [test, example]
layout: talk
---

# Test Heading

This is a test paragraph.
"""
        self.test_md_path = os.path.join(self.temp_dir.name, "test.md")
        with open(self.test_md_path, "w") as f:
            f.write(self.test_md_content)

    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory and its contents
        self.temp_dir.cleanup()

    @patch("sys.argv", ["maketalk", "test.md"])
    @patch("lamd.maketalk.open", new_callable=mock_open)
    @patch("os.system")
    @patch("os.path.exists")
    def test_makefile_creation(self, mock_exists, mock_system, mock_file):
        """Test that a makefile is created with the correct content."""
        # Mock _lamd.yml exists
        mock_exists.return_value = True

        # Mock the location of the lamd module
        with patch("lamd.__file__", "/path/to/lamd/__init__.py"):
            # Mock Interface.from_file
            with patch("lamd.config.interface.Interface.from_file") as mock_interface:
                mock_interface.return_value = {"snippetsdir": "test-snippets", "bibdir": "test-bib"}

                # Call main function
                main()

                # Assert file was opened for writing
                mock_file.assert_called_with("makefile", "w+")

                # Assert correct content was written to the file
                handle = mock_file()
                expected_writes = [
                    "BASE=test\n",
                    "MAKEFILESDIR=/path/to/lamd/makefiles\n",
                    "INCLUDESDIR=/path/to/lamd/includes\n",
                    "TEMPLATESDIR=/path/to/lamd/templates\n",
                    "SCRIPTDIR=/path/to/lamd/scripts\n",
                    "include $(MAKEFILESDIR)/make-talk-flags.mk\n",
                    "include $(MAKEFILESDIR)/make-talk.mk\n",
                ]

                calls = [call[0][0] for call in handle.write.call_args_list]
                for expected in expected_writes:
                    assert expected in calls

                # Assert make all was called
                assert mock_system.call_args_list[-1][0][0] == "make all"

    @patch("sys.argv", ["maketalk", "test.md", "--format", "slides"])
    @patch("lamd.maketalk.open", new_callable=mock_open)
    @patch("os.system")
    @patch("os.path.exists")
    def test_format_option(self, mock_exists, mock_system, mock_file):
        """Test that the --format option affects the make command."""
        # Mock _lamd.yml exists
        mock_exists.return_value = True

        # Mock necessary dependencies
        with patch("lamd.__file__", "/path/to/lamd/__init__.py"):
            with patch("lamd.config.interface.Interface.from_file") as mock_interface:
                mock_interface.return_value = {"snippetsdir": "test-snippets", "bibdir": "test-bib"}

                # Call main function
                main()

                # Assert the correct make command was called
                assert mock_system.call_args_list[-1][0][0] == "make slides"

    @patch("sys.argv", ["maketalk", "test.md", "--to", "html"])
    @patch("lamd.maketalk.open", new_callable=mock_open)
    @patch("os.system")
    @patch("os.path.exists")
    def test_to_option(self, mock_exists, mock_system, mock_file):
        """Test that the --to option affects the make command."""
        # Mock _lamd.yml exists
        mock_exists.return_value = True

        # Mock necessary dependencies
        with patch("lamd.__file__", "/path/to/lamd/__init__.py"):
            with patch("lamd.config.interface.Interface.from_file") as mock_interface:
                mock_interface.return_value = {"snippetsdir": "test-snippets", "bibdir": "test-bib"}

                # Call main function
                main()

                # Assert the correct make command was called
                assert mock_system.call_args_list[-1][0][0] == "make html"

    @patch("sys.argv", ["maketalk", "test.md", "--format", "notes", "--to", "pdf"])
    @patch("lamd.maketalk.open", new_callable=mock_open)
    @patch("os.system")
    @patch("os.path.exists")
    def test_format_and_to_options(self, mock_exists, mock_system, mock_file):
        """Test that combining --format and --to options works correctly."""
        # Mock _lamd.yml exists
        mock_exists.return_value = True

        # Mock necessary dependencies
        with patch("lamd.__file__", "/path/to/lamd/__init__.py"):
            with patch("lamd.config.interface.Interface.from_file") as mock_interface:
                mock_interface.return_value = {"snippetsdir": "test-snippets", "bibdir": "test-bib"}

                # Call main function
                main()

                # Assert the correct make command was called with the combined target
                assert mock_system.call_args_list[-1][0][0] == "make test.notes.pdf"

    @patch("sys.argv", ["maketalk", "test.md"])
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.system")
    @patch("os.path.exists")
    def test_missing_lamd_yml(self, mock_exists, mock_system, mock_file):
        """Test that the script exits when _lamd.yml is missing."""
        # Mock _lamd.yml does not exist
        mock_exists.return_value = False

        # Call main function
        with pytest.raises(SystemExit) as excinfo:
            main()

        # Check exit code
        assert excinfo.value.code == 1

        # Verify no makefile was created
        mock_file.assert_not_called()

        # Verify no make commands were run
        mock_system.assert_not_called()

    @patch("sys.argv", ["maketalk", "test.md"])
    @patch("lamd.maketalk.open", new_callable=mock_open)
    @patch("os.system")
    @patch("os.path.exists")
    def test_missing_required_fields(self, mock_exists, mock_system, mock_file):
        """Test that the script exits when required fields are missing from _lamd.yml."""
        # Mock _lamd.yml exists
        mock_exists.return_value = True

        # Mock Interface.from_file to return missing fields
        with patch("lamd.config.interface.Interface.from_file") as mock_interface:
            mock_interface.return_value = {}  # Empty dict means no fields defined

            # Call main function
            with pytest.raises(SystemExit) as excinfo:
                main()

            # Check exit code
            assert excinfo.value.code == 1

            # Verify no makefile was created
            mock_file.assert_not_called()

            # Verify no make commands were run
            mock_system.assert_not_called()

    @patch("sys.argv", ["maketalk", "test.md"])
    @patch("lamd.maketalk.open", new_callable=mock_open)
    @patch("os.system")
    @patch("os.path.exists")
    def test_nonexistent_directories(self, mock_exists, mock_system, mock_file):
        """Test that the script exits when directories specified in _lamd.yml don't exist."""
        # Mock _lamd.yml exists
        mock_exists.side_effect = lambda path: path == "_lamd.yml"  # Only _lamd.yml exists

        # Mock Interface.from_file to return directories
        with patch("lamd.config.interface.Interface.from_file") as mock_interface:
            mock_interface.return_value = {"snippetsdir": "nonexistent-snippets", "bibdir": "nonexistent-bib"}

            # Call main function
            with pytest.raises(SystemExit) as excinfo:
                main()

            # Check exit code
            assert excinfo.value.code == 1

            # Verify no makefile was created
            mock_file.assert_not_called()

            # Verify no make commands were run
            mock_system.assert_not_called()
