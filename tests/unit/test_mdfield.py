"""
Unit tests for the mdfield module.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lamd.mdfield import main

class TestMdfield:
    """Test suite for the mdfield module."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create a test markdown file
        self.test_md_content = """---
title: Test Document
author: Test Author
date: 2023-05-15
categories: [test, example, documentation]
layout: post
description: This is a test document for mdfield module testing
---

# Test Content

This is test content.
"""
        self.test_md_path = os.path.join(self.temp_dir.name, "test.md")
        with open(self.test_md_path, 'w') as f:
            f.write(self.test_md_content)
    
    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory and its contents
        self.temp_dir.cleanup()
    
    @patch('sys.argv', ['mdfield', 'title', 'test.md'])
    @patch('builtins.print')
    def test_extract_string_field_from_config(self, mock_print):
        """Test that a string field is correctly extracted from _lamd.yml."""
        # Mock Interface.from_file to return the field from config
        with patch('lamd.config.interface.Interface.from_file') as mock_interface:
            mock_interface.return_value = {'title': 'From Config'}
            
            # Call the main function
            main()
            
            # Check output
            mock_print.assert_called_once_with('From Config')
    
    @patch('sys.argv', ['mdfield', 'title', 'test.md'])
    @patch('builtins.print')
    def test_extract_string_field_from_markdown(self, mock_print):
        """Test that a string field is correctly extracted from markdown when not in config."""
        # Mock Interface.from_file to return empty dict (field not in config)
        with patch('lamd.config.interface.Interface.from_file') as mock_interface:
            mock_interface.return_value = {}
            
            # Mock talk_field to return the value from markdown
            with patch('lynguine.util.talk.talk_field', return_value='Test Document'):
                # Call the main function
                main()
                
                # Check output
                mock_print.assert_called_once_with('Test Document')
    
    @patch('sys.argv', ['mdfield', 'date', 'test.md'])
    @patch('builtins.print')
    def test_extract_date_field_from_config(self, mock_print):
        """Test that a date field is correctly extracted from _lamd.yml."""
        from datetime import date
        test_date = date(2023, 5, 15)
        
        # Mock Interface.from_file to return the field from config
        with patch('lamd.config.interface.Interface.from_file') as mock_interface:
            mock_interface.return_value = {'date': test_date}
            
            # Call the main function
            main()
            
            # Check output
            mock_print.assert_called_once_with(test_date)
    
    @patch('sys.argv', ['mdfield', 'categories', 'test.md'])
    @patch('builtins.print')
    def test_extract_list_field_from_config(self, mock_print):
        """Test that a list field is correctly extracted from _lamd.yml."""
        # Mock Interface.from_file to return the field from config
        with patch('lamd.config.interface.Interface.from_file') as mock_interface:
            mock_interface.return_value = {'categories': ['test', 'example', 'documentation']}
            
            # Call the main function
            main()
            
            # Check output
            mock_print.assert_called_once_with("['test', 'example', 'documentation']")
    
    @patch('sys.argv', ['mdfield', 'nonexistent', 'test.md'])
    @patch('builtins.print')
    def test_nonexistent_field(self, mock_print):
        """Test handling of nonexistent fields in both config and markdown."""
        # Mock Interface.from_file to return empty dict
        with patch('lamd.config.interface.Interface.from_file') as mock_interface:
            mock_interface.return_value = {}
            
            # Mock talk_field to raise a FileFormatError
            import lynguine.util.yaml as ny
            with patch('lynguine.util.talk.talk_field', side_effect=ny.FileFormatError("Field not found")):
                # Call the main function
                main()
                
                # Check that empty string was output
                mock_print.assert_called_once_with('')
    
    @patch('sys.argv', ['mdfield', 'path_field', 'test.md'])
    @patch('builtins.print')
    @patch('os.path.expandvars')
    def test_path_expansion_from_config(self, mock_expandvars, mock_print):
        """Test that environment variables in paths from config are expanded."""
        # Mock Interface.from_file to return the field from config
        with patch('lamd.config.interface.Interface.from_file') as mock_interface:
            mock_interface.return_value = {'path_field': '$HOME/test/path'}
            
            # Mock expandvars to return expanded path
            mock_expandvars.return_value = '/home/user/test/path'
            
            # Call the main function
            main()
            
            # Check output was expanded and expandvars was called
            mock_expandvars.assert_called_once_with('$HOME/test/path')
            mock_print.assert_called_once_with('/home/user/test/path')
    
    @patch('sys.argv', ['mdfield', 'nonexistent_field', 'test.md'])
    @patch('builtins.print')
    @patch('sys.stderr')
    def test_config_access_error(self, mock_stderr, mock_print):
        """Test error handling when config files can't be accessed."""
        # Mock Interface.from_file to raise an exception
        with patch('lamd.config.interface.Interface.from_file', 
                  side_effect=Exception("Could not access config file")):
            
            # Call the main function
            main()
            
            # Check that error message was written to stderr
            mock_stderr.write.assert_called_once_with("Error accessing configuration: Could not access config file\n")
            
            # Check that empty string was output
            mock_print.assert_called_once_with('') 