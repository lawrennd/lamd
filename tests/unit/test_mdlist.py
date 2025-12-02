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

        # Verify the function calls - should use path to config/cvlists.yml
        # Get the expected path
        import lamd.mdlist as mdlist_module
        lamd_dir = os.path.dirname(os.path.abspath(mdlist_module.__file__))
        config_dir = os.path.join(lamd_dir, "config")
        expected_cvlists_path = os.path.join(config_dir, "cvlists.yml")
        mock_interface.assert_called_once_with(user_file=expected_cvlists_path)
        mock_load_template.assert_called_once_with(ext=".md")
        mock_custom_df.assert_called_once()
        mock_custom_df_instance.preprocess.assert_called_once()

        # Verify the output
        expected_output = "- Test Talk\n\n- Test Talk\n\n"
        mock_print.assert_called_once_with(expected_output)

    def test_cvlists_path_construction(self):
        """Test that cvlists.yml path is constructed correctly from package location."""
        import lamd.mdlist as mdlist_module
        
        # Get the actual path construction logic
        lamd_dir = os.path.dirname(os.path.abspath(mdlist_module.__file__))
        config_dir = os.path.join(lamd_dir, "config")
        cvlists_path = os.path.join(config_dir, "cvlists.yml")
        
        # Verify the path points to the config directory
        assert config_dir.endswith("lamd/config")
        assert cvlists_path.endswith("lamd/config/cvlists.yml")
        assert os.path.basename(config_dir) == "config"
        
    @patch("sys.argv", ["mdlist", "talks", "-s", "2021", "talks.json"])
    @patch("pandas.to_datetime")
    @patch("lynguine.config.interface.Interface.from_file")
    @patch("builtins.print")
    @patch("referia.assess.data.CustomDataFrame.from_flow")
    @patch("lamd.mdlist.load_template_env")
    @patch("os.getcwd")
    def test_cvlists_path_independent_of_cwd(self, mock_getcwd, mock_load_template, mock_custom_df, mock_print, mock_interface, mock_to_datetime):
        """Test that cvlists.yml is found regardless of current working directory."""
        # Mock different working directories
        mock_getcwd.return_value = "/some/random/directory"
        
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
                "title": ["Test Talk 1"],
                "venue": ["Test Conference"],
                "year": [2022],
            }
        )
        mock_custom_df_instance = MagicMock()
        mock_custom_df_instance.df = mock_df
        mock_custom_df_instance.preprocess = MagicMock()
        mock_custom_df.return_value = mock_custom_df_instance

        # Run the main function
        main()

        # Verify that the path used is from the package, not the current directory
        assert mock_interface.called, "Interface.from_file should have been called"
        call_args = mock_interface.call_args
        
        # Get user_file from kwargs (it's a keyword argument)
        if call_args.kwargs:
            called_path = call_args.kwargs.get("user_file")
        else:
            # If no kwargs, check positional args
            called_path = call_args[0][0] if call_args[0] else None
        
        # The path should be an absolute path to the config directory
        assert called_path is not None, f"user_file should have been provided. Call args: {call_args}"
        assert os.path.isabs(called_path), f"Path should be absolute, got {called_path}"
        assert called_path.endswith("lamd/config/cvlists.yml"), f"Path should end with lamd/config/cvlists.yml, got {called_path}"
        assert "config" in called_path, f"Path should include config directory, got {called_path}"

    @patch("sys.argv", ["mdlist", "publications", "test1.md", "test2.md"])
    @patch("pandas.to_datetime")
    @patch("lynguine.config.interface.Interface.from_file")
    @patch("builtins.print")
    @patch("referia.assess.data.CustomDataFrame.from_flow")
    @patch("lamd.mdlist.load_template_env")
    def test_index_field_set_in_interface(self, mock_load_template, mock_custom_df, mock_print, mock_interface, mock_to_datetime):
        """Test that the index field is set to 'filename' in the interface input configuration."""
        # Mock the current date
        mock_now = pd.Timestamp("2024-03-15")
        mock_to_datetime.return_value = mock_now

        # Create a mock interface that tracks changes to the input configuration
        class InterfaceDict(dict):
            def __contains__(self, key):
                return dict.__contains__(self, key)

            def __getitem__(self, key):
                return dict.__getitem__(self, key)

        class PublicationsDict(dict):
            def __contains__(self, key):
                return key in ["listtemplate", "compute", "input", "publications"]

            def __getitem__(self, key):
                if key == "publications":
                    return self
                return dict.__getitem__(self, key)

        publications_dict = PublicationsDict(
            {
                "listtemplate": "listpaper",
                "compute": {
                    "preprocessor": [],
                    "augmentor": [],
                    "sorter": [],
                },
                "input": {},
            }
        )
        interface_dict = InterfaceDict({"publications": publications_dict})
        mock_interface.return_value = interface_dict

        # Mock the template environment
        mock_env = MagicMock()
        mock_template = MagicMock()
        mock_template.render.return_value = "- Test Publication\n"
        mock_env.get_template.return_value = mock_template
        mock_load_template.return_value = mock_env

        # Mock the CustomDataFrame
        mock_df = pd.DataFrame(
            {
                "title": ["Test Publication 1", "Test Publication 2"],
                "year": [2022, 2023],
            }
        )
        mock_custom_df_instance = MagicMock()
        mock_custom_df_instance.df = mock_df
        mock_custom_df_instance.preprocess = MagicMock()
        mock_custom_df.return_value = mock_custom_df_instance

        # Create test files in temp directory
        test_file1 = os.path.join(self.temp_dir.name, "test1.md")
        test_file2 = os.path.join(self.temp_dir.name, "test2.md")
        with open(test_file1, "w") as f:
            f.write("# Test 1\n")
        with open(test_file2, "w") as f:
            f.write("# Test 2\n")

        # Update sys.argv to use the test files
        import sys
        original_argv = sys.argv
        sys.argv = ["mdlist", "publications", test_file1, test_file2]

        try:
            # Run the main function
            main()
        finally:
            sys.argv = original_argv

        # Verify that CustomDataFrame.from_flow was called
        assert mock_custom_df.called, "CustomDataFrame.from_flow should have been called"

        # Get the interface that was passed to CustomDataFrame.from_flow
        call_args = mock_custom_df.call_args
        passed_interface = call_args[0][0] if call_args[0] else None

        # Verify the interface has the index field set
        assert passed_interface is not None, "Interface should have been passed to CustomDataFrame.from_flow"
        assert "input" in passed_interface, "Interface should have an 'input' key"
        assert "index" in passed_interface["input"], "Interface input should have an 'index' field"
        assert passed_interface["input"]["index"] == "filename", (
            f"Index field should be set to 'filename', got '{passed_interface['input']['index']}'"
        )

    @patch("sys.argv", ["mdlist", "talks", "talk1.md"])
    @patch("pandas.to_datetime")
    @patch("lynguine.config.interface.Interface.from_file")
    @patch("builtins.print")
    @patch("referia.assess.data.CustomDataFrame.from_flow")
    @patch("lamd.mdlist.load_template_env")
    def test_index_field_set_for_single_file(self, mock_load_template, mock_custom_df, mock_print, mock_interface, mock_to_datetime):
        """Test that the index field is set correctly when processing a single file."""
        # Mock the current date
        mock_now = pd.Timestamp("2024-03-15")
        mock_to_datetime.return_value = mock_now

        # Create a mock interface
        class InterfaceDict(dict):
            def __contains__(self, key):
                return dict.__contains__(self, key)

            def __getitem__(self, key):
                return dict.__getitem__(self, key)

        class TalksDict(dict):
            def __contains__(self, key):
                return key in ["listtemplate", "compute", "input", "talks"]

            def __getitem__(self, key):
                if key == "talks":
                    return self
                return dict.__getitem__(self, key)

        talks_dict = TalksDict(
            {
                "listtemplate": "listtalk",
                "compute": {
                    "preprocessor": [],
                    "augmentor": [],
                    "sorter": [],
                },
                "input": {},
            }
        )
        interface_dict = InterfaceDict({"talks": talks_dict})
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
                "title": ["Test Talk"],
                "venue": ["Test Conference"],
                "year": [2022],
            }
        )
        mock_custom_df_instance = MagicMock()
        mock_custom_df_instance.df = mock_df
        mock_custom_df_instance.preprocess = MagicMock()
        mock_custom_df.return_value = mock_custom_df_instance

        # Create test file in temp directory
        test_file = os.path.join(self.temp_dir.name, "talk1.md")
        with open(test_file, "w") as f:
            f.write("# Test Talk\n")

        # Update sys.argv to use the test file
        import sys
        original_argv = sys.argv
        sys.argv = ["mdlist", "talks", test_file]

        try:
            # Run the main function
            main()
        finally:
            sys.argv = original_argv

        # Verify that CustomDataFrame.from_flow was called
        assert mock_custom_df.called, "CustomDataFrame.from_flow should have been called"

        # Get the interface that was passed to CustomDataFrame.from_flow
        call_args = mock_custom_df.call_args
        passed_interface = call_args[0][0] if call_args[0] else None

        # Verify the interface has the index field set
        assert passed_interface is not None, "Interface should have been passed to CustomDataFrame.from_flow"
        assert "input" in passed_interface, "Interface should have an 'input' key"
        assert "index" in passed_interface["input"], "Interface input should have an 'index' field"
        assert passed_interface["input"]["index"] == "filename", (
            f"Index field should be set to 'filename', got '{passed_interface['input']['index']}'"
        )
