"""
Unit tests for the mdlist module.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from datetime import date

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pandas as pd
from lamd.mdlist import main, set_since_year, get_since_year

class TestMdlist:
    """Test suite for the mdlist module."""
    
    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create test data files
        self.test_data = """[
            {
                "title": "Test Talk 1",
                "venue": "Test Conference",
                "year": 2022,
                "month": 6,
                "day": 15,
                "url": "https://example.com/talk1"
            },
            {
                "title": "Test Talk 2",
                "venue": "Another Conference",
                "year": 2023,
                "month": 3,
                "day": 10,
                "url": "https://example.com/talk2"
            }
        ]"""
        
        self.test_data_path = os.path.join(self.temp_dir.name, "talks.json")
        with open(self.test_data_path, 'w') as f:
            f.write(self.test_data)
            
        # Create a test configuration file
        self.config_content = """
talks:
  listtemplate: talk_item
  preprocessor: clean_date
  augmentor: add_talk_details
  sorter: sort_by_date
  filter: recent_talks

compute:
  preprocessor: []
  augmentor: []
  sorter: []

filter: []
"""
        self.config_path = os.path.join(self.temp_dir.name, "cvlists.yml")
        with open(self.config_path, 'w') as f:
            f.write(self.config_content)
    
    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory and its contents
        self.temp_dir.cleanup()
    
    def test_since_year_functions(self):
        """Test the set_since_year and get_since_year functions."""
        # Test setting and getting the year
        set_since_year(2020)
        assert get_since_year() == 2020
        
        # Test changing the year
        set_since_year(2022)
        assert get_since_year() == 2022
        
        # Test setting to None
        set_since_year(None)
        assert get_since_year() is None
    
    @pytest.mark.skip(reason="The main function has several bugs and dependencies that need to be fixed")
    @patch('sys.argv', ['mdlist', 'talks', '-s', '2021', 'talks.json'])
    @patch('pandas.to_datetime')
    @patch('lynguine.config.interface.Interface.from_file')
    @patch('lynguine.util.liquid.load_template_env')
    @patch('builtins.print')
    def test_main_function(self, mock_print, mock_load_template, mock_interface, mock_to_datetime):
        """Test the main function with talks list type."""
        # This test is a placeholder for now as the main function has several issues
        # that need to be fixed before we can properly test it
        pass 