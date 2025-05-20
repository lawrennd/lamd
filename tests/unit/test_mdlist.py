"""
Unit tests for the mdlist module.
"""

import os
import sys
import tempfile
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import pandas as pd

from lamd.mdlist import main
from lamd.util import get_since_year, set_since_year


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
        with open(self.test_data_path, "w") as f:
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
        with open(self.config_path, "w") as f:
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

    @patch("sys.argv", ["mdlist", "talks", "-s", "2021", "talks.json"])
    @patch("pandas.to_datetime")
    @patch("lynguine.config.interface.Interface.from_file")
    @patch("builtins.print")
    @patch("referia.assess.data.CustomDataFrame.from_flow")
    @patch("lamd.mdlist.load_template_env")
    def test_main_function(self, mock_load_template, mock_custom_df, mock_print, mock_interface, mock_to_datetime):
        """Test the main function with talks list type."""
        # Mock the current date
        mock_now = pd.Timestamp("2024-03-15")
        mock_to_datetime.return_value = mock_now

        # Mock the interface configuration
        class InterfaceDict(dict):
            def __contains__(self, key):
                return dict.__contains__(self, key)

            def __getitem__(self, key):
                return dict.__getitem__(self, key)

        class TalksDict(dict):
            def __contains__(self, key):
                return key in ["listtemplate", "preprocessor", "augmentor", "sorter", "filter", "input", "talks"]

            def __getitem__(self, key):
                if key == "talks":
                    return self
                return dict.__getitem__(self, key)

        talks_dict = TalksDict(
            {
                "listtemplate": "talk_item",
                "preprocessor": "clean_date",
                "augmentor": "add_talk_details",
                "sorter": "sort_by_date",
                "filter": "recent_talks",
                "input": {},
            }
        )
        interface_dict = InterfaceDict({"talks": talks_dict, "lists": {"talks": talks_dict}})
        mock_interface.return_value = interface_dict

        # Mock the template environment
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "- Test Talk\n"
        mock_env.get_template.return_value = mock_template
        mock_load_template.return_value = mock_env

        # Mock the CustomDataFrame
        mock_df = pd.DataFrame(
            {
                "title": ["Test Talk 1", "Test Talk 2"],
                "venue": ["Test Conference", "Another Conference"],
                "year": [2022, 2023],
                "month": [6, 3],
                "day": [15, 10],
                "url": ["https://example.com/talk1", "https://example.com/talk2"],
            }
        )
        mock_custom_df_instance = MagicMock()
        mock_custom_df_instance.df = mock_df
        mock_custom_df_instance.preprocess = MagicMock()
        mock_custom_df.return_value = mock_custom_df_instance

        # Run the main function
        main()

        # Verify the function calls
        mock_interface.assert_called_once_with(user_file="cvlists.yml")
        mock_load_template.assert_called_once_with(ext=".md")
        mock_custom_df.assert_called_once()
        mock_custom_df_instance.preprocess.assert_called_once()

        # Verify the output
        expected_output = "- Test Talk\n\n- Test Talk\n\n"
        mock_print.assert_called_once_with(expected_output)
