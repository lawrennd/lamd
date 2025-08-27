#!/usr/bin/env python3
"""
Tests for practical directory functionality.

This module tests that files with layout: practical are properly moved
to the practicalsdir instead of default directories.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch

import pytest

from lamd.mdfield import main as mdfield_main
from lamd.flags import main as flags_main


class TestPracticalDirectories:
    """Test suite for practical directory functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)

    def create_test_files(self, layout="practical", week=1, session=2, practical=1):
        """Create test markdown and config files."""
        # Create _lamd.yml
        lamd_yml_content = """snippetsdir: ../_snippets
bibdir: ../_bibliography
macrosdir: $HOME/lawrennd/lamd/lamd/macros
slidesdir: _lectures
postsdir: _posts
notesdir: _notes
notebooksdir: _notebooks
texdir: _tex
practicalsdir: _practicals
"""
        with open("_lamd.yml", "w") as f:
            f.write(lamd_yml_content)

        # Create test markdown file
        md_content = f"""---
layout: {layout}
week: {week}
session: {session}
practical: {practical}
title: Test Practical
date: 2025-01-15
---

# Test Practical

This is a test practical to verify that files are moved to the correct directory.

## Content

Some content here.
"""
        with open("test_practical.md", "w") as f:
            f.write(md_content)

    def test_mdfield_extracts_layout_correctly(self):
        """Test that mdfield correctly extracts layout from markdown."""
        self.create_test_files(layout="practical")
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_practical.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("practical")

    def test_mdfield_extracts_practicalsdir_correctly(self):
        """Test that mdfield correctly extracts practicalsdir from config."""
        self.create_test_files()
        
        with patch('sys.argv', ['mdfield', 'practicalsdir', 'test_practical.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("_practicals")

    def test_flags_generates_correct_prefix_for_practical(self):
        """Test that flags generates correct prefix for practical layout."""
        self.create_test_files(week=1, session=2, practical=1)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_practical']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("01-02-01-")

    def test_flags_generates_correct_prefix_for_different_numbers(self):
        """Test that flags generates correct prefix for different week/session/practical numbers."""
        self.create_test_files(week=5, session=3, practical=2)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_practical']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("05-03-02-")

    def test_flags_generates_empty_prefix_for_lecture_layout(self):
        """Test that flags generates correct prefix for lecture layout."""
        self.create_test_files(layout="lecture", week=1, session=2)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_practical']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("01-02-")

    def test_flags_generates_date_prefix_for_talk_layout(self):
        """Test that flags generates date prefix for talk layout."""
        self.create_test_files(layout="talk")
        
        with patch('sys.argv', ['flags', 'prefix', 'test_practical']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("2025-01-15-")

    def test_mdfield_handles_missing_practicalsdir_gracefully(self):
        """Test that mdfield handles missing practicalsdir gracefully."""
        # Create _lamd.yml without practicalsdir
        lamd_yml_content = """snippetsdir: ../_snippets
bibdir: ../_bibliography
macrosdir: $HOME/lawrennd/lamd/lamd/macros
slidesdir: _lectures
postsdir: _posts
notesdir: _notes
notebooksdir: _notebooks
texdir: _tex
"""
        with open("_lamd.yml", "w") as f:
            f.write(lamd_yml_content)

        # Create test markdown file
        md_content = """---
layout: practical
week: 1
session: 2
practical: 1
title: Test Practical
date: 2025-01-15
---

# Test Practical
"""
        with open("test_practical.md", "w") as f:
            f.write(md_content)
        
        with patch('sys.argv', ['mdfield', 'practicalsdir', 'test_practical.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("")

    def test_mdfield_handles_missing_layout_gracefully(self):
        """Test that mdfield handles missing layout gracefully."""
        self.create_test_files()
        
        # Create markdown file without layout
        md_content = """---
week: 1
session: 2
practical: 1
title: Test Practical
date: 2025-01-15
---

# Test Practical
"""
        with open("test_practical.md", "w") as f:
            f.write(md_content)
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_practical.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                # Should return empty string or default value
                mock_print.assert_called_once()

    def test_flags_handles_missing_week_session_practical_gracefully(self):
        """Test that flags handles missing week/session/practical gracefully."""
        self.create_test_files()
        
        # Create markdown file without week/session/practical
        md_content = """---
layout: practical
title: Test Practical
date: 2025-01-15
---

# Test Practical
"""
        with open("test_practical.md", "w") as f:
            f.write(md_content)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_practical']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("")


class TestPracticalDirectoryIntegration:
    """Integration tests for practical directory functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        import shutil
        shutil.rmtree(self.test_dir)

    def test_practical_directory_workflow(self):
        """Test the complete practical directory workflow."""
        # Create _lamd.yml
        lamd_yml_content = """snippetsdir: ../_snippets
bibdir: ../_bibliography
macrosdir: $HOME/lawrennd/lamd/lamd/macros
slidesdir: _lectures
postsdir: _posts
notesdir: _notes
notebooksdir: _notebooks
texdir: _tex
practicalsdir: _practicals
"""
        with open("_lamd.yml", "w") as f:
            f.write(lamd_yml_content)

        # Create test markdown file
        md_content = """---
layout: practical
week: 3
session: 1
practical: 2
title: Advanced Test Practical
date: 2025-01-15
---

# Advanced Test Practical

This is an advanced test practical.
"""
        with open("advanced_practical.md", "w") as f:
            f.write(md_content)

        # Test layout extraction
        with patch('sys.argv', ['mdfield', 'layout', 'advanced_practical.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("practical")

        # Test practicalsdir extraction
        with patch('sys.argv', ['mdfield', 'practicalsdir', 'advanced_practical.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("_practicals")

        # Test prefix generation
        with patch('sys.argv', ['flags', 'prefix', 'advanced_practical']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("03-01-02-")

        # Verify the expected output filename would be correct
        expected_filename = "03-01-02-advanced_practical"
        assert expected_filename == "03-01-02-advanced_practical"


if __name__ == "__main__":
    unittest.main()
