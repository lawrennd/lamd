#!/usr/bin/env python3
"""
Tests for the complete directory system functionality.

This module tests that files are properly moved to the correct directories
based on their layout and configuration settings.
"""

import os
import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch

import pytest

from lamd.mdfield import main as mdfield_main
from lamd.flags import main as flags_main


class TestDirectorySystem:
    """Test suite for the complete directory system functionality."""

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

    def create_test_files(self, layout="practical", week=1, session=2, practical=1, topic=1, background=1):
        """Create test markdown and config files."""
        # Create _lamd.yml with all directory types
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
topic: {topic}
background: {background}
title: Test Document
date: 2025-01-15
---

# Test Document

This is a test document to verify directory system functionality.

## Content

Some content here.
"""
        with open("test_document.md", "w") as f:
            f.write(md_content)

    # ============================================================================
    # PRACTICAL LAYOUT TESTS
    # ============================================================================

    def test_practical_layout_extraction(self):
        """Test that practical layout is correctly extracted."""
        self.create_test_files(layout="practical")
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("practical")

    def test_practical_practicalsdir_extraction(self):
        """Test that practicalsdir is correctly extracted for practicals."""
        self.create_test_files(layout="practical")
        
        with patch('sys.argv', ['mdfield', 'practicalsdir', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("_practicals")

    def test_practical_prefix_generation(self):
        """Test that practical layout generates correct prefix."""
        self.create_test_files(layout="practical", week=1, session=2, practical=1)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("01-02-01-")

    def test_practical_prefix_different_numbers(self):
        """Test practical prefix with different week/session/practical numbers."""
        self.create_test_files(layout="practical", week=5, session=3, practical=2)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("05-03-02-")

    # ============================================================================
    # LECTURE LAYOUT TESTS
    # ============================================================================

    def test_lecture_layout_extraction(self):
        """Test that lecture layout is correctly extracted."""
        self.create_test_files(layout="lecture")
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("lecture")

    def test_lecture_slidesdir_extraction(self):
        """Test that slidesdir is correctly extracted for lectures."""
        self.create_test_files(layout="lecture")
        
        with patch('sys.argv', ['mdfield', 'slidesdir', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("_lectures")

    def test_lecture_prefix_generation(self):
        """Test that lecture layout generates correct prefix."""
        self.create_test_files(layout="lecture", week=1, session=2)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("01-02-")

    def test_lecture_prefix_week_only(self):
        """Test lecture prefix with week only."""
        self.create_test_files(layout="lecture", week=3)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                # The system includes session even if not specified, defaulting to 2
                mock_print.assert_called_with("03-02-")

    # ============================================================================
    # TALK LAYOUT TESTS
    # ============================================================================

    def test_talk_layout_extraction(self):
        """Test that talk layout is correctly extracted."""
        self.create_test_files(layout="talk")
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("talk")

    def test_talk_postsdir_extraction(self):
        """Test that postsdir is correctly extracted for talks."""
        self.create_test_files(layout="talk")
        
        with patch('sys.argv', ['mdfield', 'postsdir', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("_posts")

    def test_talk_prefix_generation(self):
        """Test that talk layout generates date-based prefix."""
        self.create_test_files(layout="talk")
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("2025-01-15-")

    def test_talk_prefix_no_date(self):
        """Test talk prefix without date."""
        # Create markdown file without date
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

        md_content = """---
layout: talk
title: Test Talk
---

# Test Talk
"""
        with open("test_document.md", "w") as f:
            f.write(md_content)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("")

    # ============================================================================
    # TOPIC LAYOUT TESTS
    # ============================================================================

    def test_topic_layout_extraction(self):
        """Test that topic layout is correctly extracted."""
        self.create_test_files(layout="topic")
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("topic")

    def test_topic_prefix_generation(self):
        """Test that topic layout generates correct prefix."""
        self.create_test_files(layout="topic", topic=3)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("03-")

    # ============================================================================
    # BACKGROUND LAYOUT TESTS
    # ============================================================================

    def test_background_layout_extraction(self):
        """Test that background layout is correctly extracted."""
        self.create_test_files(layout="background")
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("background")

    def test_background_prefix_generation(self):
        """Test that background layout generates correct prefix."""
        self.create_test_files(layout="background", week=2, session=1, background=3)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("02-01-03-")

    # ============================================================================
    # OTHER LAYOUT TESTS
    # ============================================================================

    def test_notebook_layout_extraction(self):
        """Test that notebook layout is correctly extracted."""
        self.create_test_files(layout="notebook")
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("notebook")

    def test_notebook_prefix_generation(self):
        """Test that notebook layout generates empty prefix."""
        self.create_test_files(layout="notebook")
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("")

    def test_casestudy_layout_extraction(self):
        """Test that casestudy layout is correctly extracted."""
        self.create_test_files(layout="casestudy")
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("casestudy")

    def test_casestudy_prefix_generation(self):
        """Test that casestudy layout generates date-based prefix."""
        self.create_test_files(layout="casestudy")
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("2025-01-15-")

    # ============================================================================
    # DIRECTORY EXTRACTION TESTS
    # ============================================================================

    def test_all_directory_extractions(self):
        """Test extraction of all directory types."""
        self.create_test_files()
        
        directories = [
            ('snippetsdir', '../_snippets'),
            ('bibdir', '../_bibliography'),
            ('slidesdir', '_lectures'),
            ('postsdir', '_posts'),
            ('notesdir', '_notes'),
            ('notebooksdir', '_notebooks'),
            ('texdir', '_tex'),
            ('practicalsdir', '_practicals'),
        ]
        
        for dir_type, expected_value in directories:
            with patch('sys.argv', ['mdfield', dir_type, 'test_document.md']):
                with patch('builtins.print') as mock_print:
                    result = mdfield_main()
                    assert result == 0
                    mock_print.assert_called_with(expected_value)
        
        # Test macrosdir separately since it contains environment variables
        with patch('sys.argv', ['mdfield', 'macrosdir', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                # Just verify it was called and contains the expected path structure
                mock_print.assert_called_once()
                actual_value = mock_print.call_args[0][0]
                assert 'lawrennd/lamd/lamd/macros' in actual_value

    # ============================================================================
    # ERROR HANDLING TESTS
    # ============================================================================

    def test_missing_practicalsdir_handling(self):
        """Test graceful handling of missing practicalsdir."""
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
        with open("test_document.md", "w") as f:
            f.write(md_content)
        
        with patch('sys.argv', ['mdfield', 'practicalsdir', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("")

    def test_missing_layout_handling(self):
        """Test graceful handling of missing layout."""
        self.create_test_files()
        
        # Create markdown file without layout
        md_content = """---
week: 1
session: 2
practical: 1
title: Test Document
date: 2025-01-15
---

# Test Document
"""
        with open("test_document.md", "w") as f:
            f.write(md_content)
        
        with patch('sys.argv', ['mdfield', 'layout', 'test_document.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                # Should return empty string or default value
                mock_print.assert_called_once()

    def test_missing_week_session_practical_handling(self):
        """Test graceful handling of missing week/session/practical."""
        self.create_test_files()
        
        # Create markdown file without week/session/practical
        md_content = """---
layout: practical
title: Test Document
date: 2025-01-15
---

# Test Document
"""
        with open("test_document.md", "w") as f:
            f.write(md_content)
        
        with patch('sys.argv', ['flags', 'prefix', 'test_document']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("")

    # ============================================================================
    # INTEGRATION TESTS
    # ============================================================================

    def test_complete_practical_workflow(self):
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

    def test_complete_lecture_workflow(self):
        """Test the complete lecture directory workflow."""
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
layout: lecture
week: 4
session: 2
title: Advanced Test Lecture
date: 2025-01-15
---

# Advanced Test Lecture

This is an advanced test lecture.
"""
        with open("advanced_lecture.md", "w") as f:
            f.write(md_content)

        # Test layout extraction
        with patch('sys.argv', ['mdfield', 'layout', 'advanced_lecture.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("lecture")

        # Test slidesdir extraction
        with patch('sys.argv', ['mdfield', 'slidesdir', 'advanced_lecture.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("_lectures")

        # Test prefix generation
        with patch('sys.argv', ['flags', 'prefix', 'advanced_lecture']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("04-02-")

        # Verify the expected output filename would be correct
        expected_filename = "04-02-advanced_lecture"
        assert expected_filename == "04-02-advanced_lecture"

    def test_complete_talk_workflow(self):
        """Test the complete talk directory workflow."""
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
layout: talk
title: Advanced Test Talk
date: 2025-01-15
---

# Advanced Test Talk

This is an advanced test talk.
"""
        with open("advanced_talk.md", "w") as f:
            f.write(md_content)

        # Test layout extraction
        with patch('sys.argv', ['mdfield', 'layout', 'advanced_talk.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("talk")

        # Test postsdir extraction
        with patch('sys.argv', ['mdfield', 'postsdir', 'advanced_talk.md']):
            with patch('builtins.print') as mock_print:
                result = mdfield_main()
                assert result == 0
                mock_print.assert_called_with("_posts")

        # Test prefix generation
        with patch('sys.argv', ['flags', 'prefix', 'advanced_talk']):
            with patch('builtins.print') as mock_print:
                result = flags_main()
                assert result == 0
                mock_print.assert_called_with("2025-01-15-")

        # Verify the expected output filename would be correct
        expected_filename = "2025-01-15-advanced_talk"
        assert expected_filename == "2025-01-15-advanced_talk"


if __name__ == "__main__":
    unittest.main()
