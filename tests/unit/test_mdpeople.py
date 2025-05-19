"""
Unit tests for the mdpeople module.
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lamd.mdpeople import create_circle_head_macro, create_person_macro, generate_macros_file, main


class TestMdpeople:
    """Test suite for the mdpeople module."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a test YAML file with people data
        self.test_yaml_content = """
- given: Jane
  family: Doe
  image: people/jane-doe.jpg
  url: https://example.com/jane
  title: Professor

- given: John
  family: Smith
  image: people/john-smith.jpg
  crop:
    llx: 0
    lly: 0
    urx: 100
    ury: 100
"""
        self.test_yaml_path = os.path.join(self.temp_dir.name, "people.yaml")
        with open(self.test_yaml_path, "w") as f:
            f.write(self.test_yaml_content)

    def teardown_method(self):
        """Clean up after each test."""
        # Remove temporary directory and its contents
        self.temp_dir.cleanup()

    def test_create_circle_head_macro(self):
        """Test the creation of the base circleHead macro."""
        macro = create_circle_head_macro()
        assert r"\define{\circleHead{filename}{alttext}{width}{circleurl}}" in macro
        # Checking for clipPath element but accounting for escape characters
        assert '<clipPath id="clip\\urlCount">' in macro
        assert '<circle cx="100" cy="100" r="100"/>' in macro

    def test_create_person_macro_basic(self):
        """Test creating a person macro with basic information."""
        macro = create_person_macro(given="Jane", family="Doe", image_path="people/jane-doe.jpg", title="Professor")
        assert "\\\\defeval{\\\\janeDoePicture" in macro
        assert "\\diagramsDir/people/jane-doe.jpg" in macro
        assert "{Professor}" in macro

    def test_create_person_macro_with_url(self):
        """Test creating a person macro with a URL."""
        macro = create_person_macro(
            given="Jane", family="Doe", image_path="people/jane-doe.jpg", url="https://example.com/jane", title="Professor"
        )
        assert "\\\\defeval{\\\\janeDoePicture" in macro
        assert "\\diagramsDir/people/jane-doe.jpg" in macro
        assert "{Professor}" in macro
        assert "{https://example.com/jane}" in macro

    def test_create_person_macro_with_crop(self):
        """Test creating a person macro with crop coordinates."""
        macro = create_person_macro(
            given="John", family="Smith", image_path="people/john-smith.jpg", crop={"llx": 0, "lly": 0, "urx": 100, "ury": 100}
        )
        assert "\\\\defeval{\\\\johnSmithPicture" in macro
        assert "\\includeimgclip{\\diagramsDir/people/john-smith.jpg}" in macro
        assert "{0}{0}{100}{100}" in macro

    def test_generate_macros_file(self):
        """Test generating a complete macros file."""
        import yaml

        output_path = os.path.join(self.temp_dir.name, "output.gpp")

        with open(self.test_yaml_path, "r") as f:
            people = yaml.safe_load(f)

        generate_macros_file(people, output_path)

        # Check if the file was created
        assert os.path.exists(output_path)

        # Check file contents
        with open(output_path, "r") as f:
            content = f.read()
            assert "\\ifndef{talkPeople}" in content
            assert "\\define{talkPeople}" in content
            assert "\\\\defeval{\\\\janeDoePicture" in content
            assert "\\\\defeval{\\\\johnSmithPicture" in content
            assert "\\endif" in content

    @patch("argparse.ArgumentParser.parse_args")
    @patch("builtins.open")
    @patch("yaml.safe_load")
    @patch("lamd.mdpeople.generate_macros_file")
    def test_main_function(self, mock_generate, mock_yaml_load, mock_open, mock_args):
        """Test the main function."""
        # Setup mocks
        mock_args.return_value = MagicMock(input="people.yaml", output="output.gpp")
        mock_yaml_load.return_value = [{"given": "Jane", "family": "Doe", "image": "people/jane-doe.jpg"}]

        # Call the main function
        main()

        # Verify the calls
        mock_open.assert_called()
        mock_yaml_load.assert_called_once()
        mock_generate.assert_called_once_with(
            [{"given": "Jane", "family": "Doe", "image": "people/jane-doe.jpg"}], "output.gpp"
        )
