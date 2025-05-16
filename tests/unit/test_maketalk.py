"""
Unit tests for the maketalk module.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock, mock_open, call

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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
        with open(self.test_md_path, 'w') as f:
            f.write(self.test_md_content)
    
    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory and its contents
        self.temp_dir.cleanup()
    
    @patch('sys.argv', ['maketalk', 'test.md'])
    @patch('lamd.maketalk.open', new_callable=mock_open)
    @patch('os.system')
    def test_makefile_creation(self, mock_system, mock_file):
        """Test that a makefile is created with the correct content."""
        # Mock the location of the lamd module
        with patch('lamd.__file__', '/path/to/lamd/__init__.py'):
            # Mock talk_field and Interface.from_file
            with patch('lynguine.util.talk.talk_field', return_value=''):
                with patch('lamd.config.interface.Interface.from_file') as mock_interface:
                    mock_interface.return_value = {'snippetsdir': '', 'bibdir': ''}
                    
                    # Call main function
                    main()
                    
                    # Assert file was opened for writing
                    mock_file.assert_called_with('makefile', 'w+')
                    
                    # Assert correct content was written to the file
                    handle = mock_file()
                    expected_writes = [
                        'BASE=test\n',
                        'MAKEFILESDIR=/path/to/lamd/makefiles\n',
                        'INCLUDESDIR=/path/to/lamd/includes\n',
                        'TEMPLATESDIR=/path/to/lamd/templates\n',
                        'SCRIPTDIR=/path/to/lamd/scripts\n',
                        'include $(MAKEFILESDIR)/make-talk-flags.mk\n',
                        'include $(MAKEFILESDIR)/make-talk.mk\n',
                    ]
                    
                    calls = [call[0][0] for call in handle.write.call_args_list]
                    for expected in expected_writes:
                        assert expected in calls
                    
                    # Assert make all was called
                    assert mock_system.call_args_list[-1][0][0] == 'make all'
    
    @patch('sys.argv', ['maketalk', 'test.md', '--format', 'slides'])
    @patch('lamd.maketalk.open', new_callable=mock_open)
    @patch('os.system')
    def test_format_option(self, mock_system, mock_file):
        """Test that the --format option affects the make command."""
        # Mock necessary dependencies
        with patch('lamd.__file__', '/path/to/lamd/__init__.py'):
            with patch('lynguine.util.talk.talk_field', return_value=''):
                with patch('lamd.config.interface.Interface.from_file') as mock_interface:
                    mock_interface.return_value = {'snippetsdir': '', 'bibdir': ''}
                    
                    # Call main function
                    main()
                    
                    # Assert the correct make command was called
                    assert mock_system.call_args_list[-1][0][0] == 'make slides'

    @patch('sys.argv', ['maketalk', 'test.md', '--to', 'html'])
    @patch('lamd.maketalk.open', new_callable=mock_open)
    @patch('os.system')
    def test_to_option(self, mock_system, mock_file):
        """Test that the --to option affects the make command."""
        # Mock necessary dependencies
        with patch('lamd.__file__', '/path/to/lamd/__init__.py'):
            with patch('lynguine.util.talk.talk_field', return_value=''):
                with patch('lamd.config.interface.Interface.from_file') as mock_interface:
                    mock_interface.return_value = {'snippetsdir': '', 'bibdir': ''}
                    
                    # Call main function
                    main()
                    
                    # Assert the correct make command was called
                    assert mock_system.call_args_list[-1][0][0] == 'make html'

    @patch('sys.argv', ['maketalk', 'test.md', '--format', 'notes', '--to', 'pdf'])
    @patch('lamd.maketalk.open', new_callable=mock_open)
    @patch('os.system')
    def test_format_and_to_options(self, mock_system, mock_file):
        """Test that combining --format and --to options works correctly."""
        # Mock necessary dependencies
        with patch('lamd.__file__', '/path/to/lamd/__init__.py'):
            with patch('lynguine.util.talk.talk_field', return_value=''):
                with patch('lamd.config.interface.Interface.from_file') as mock_interface:
                    mock_interface.return_value = {'snippetsdir': '', 'bibdir': ''}
                    
                    # Call main function
                    main()
                    
                    # Assert the correct make command was called with the combined target
                    assert mock_system.call_args_list[-1][0][0] == 'make test.notes.pdf'
    
    @patch('sys.argv', ['maketalk', 'test.md'])
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.system')
    @patch('lynguine.util.talk.talk_field')
    def test_handles_field_error(self, mock_talk_field, mock_system, mock_file):
        """Test that the script handles errors when extracting fields."""
        # Mock talk_field to raise an error
        import lynguine.util.yaml as ny
        mock_talk_field.side_effect = ny.FileFormatError('Test error')
        
        # Mock the interface
        with patch('lamd.config.interface.Interface.from_file') as mock_interface:
            mock_interface.return_value = {'snippetsdir': 'test-snippets', 'bibdir': 'test-bib'}
            
            # Call main function
            main()
            
            # Check that git pull was called with the right path for non-empty directories
            assert f"CURDIR=`pwd`;cd test-snippets; git pull; cd $CURDIR" in [call[0][0] for call in mock_system.call_args_list]
            assert f"CURDIR=`pwd`;cd test-bib; git pull; cd $CURDIR" in [call[0][0] for call in mock_system.call_args_list] 