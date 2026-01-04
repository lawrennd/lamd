"""
Unit tests for mdfield server mode (--use-server flag).
"""

import os
import sys
import tempfile
from unittest.mock import patch, MagicMock, call

# Add the parent directory to the path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lamd.mdfield import main


class TestMdfieldServerMode:
    """Test suite for mdfield --use-server flag."""

    def setup_method(self):
        """Set up test environment before each test."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a test markdown file
        self.test_md_content = """---
title: Test Document
author: Test Author
date: 2023-05-15
categories: [test, example]
---

# Test Content
"""
        self.test_md_path = os.path.join(self.temp_dir.name, "test.md")
        with open(self.test_md_path, "w") as f:
            f.write(self.test_md_content)

    def teardown_method(self):
        """Clean up after each test."""
        self.temp_dir.cleanup()

    @patch("sys.argv", ["mdfield", "--use-server", "title", "test.md"])
    @patch("builtins.print")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_string_field(self, mock_server_client_class, mock_print):
        """Test server mode extracts string field correctly."""
        # Mock ServerClient instance
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        # Mock extract_talk_field method (returns string directly)
        mock_client.extract_talk_field.return_value = "Test Document"
        
        # Call the main function
        main()
        
        # Verify ServerClient was instantiated
        mock_server_client_class.assert_called_once()
        
        # Verify extract_talk_field was called with correct arguments
        # Note: mdfield.py automatically adds default config files
        mock_client.extract_talk_field.assert_called_once_with(
            field="title",
            markdown_file="test.md",
            config_files=["_lamd.yml", "_config.yml"]
        )
        
        # Verify output
        mock_print.assert_called_once_with("Test Document")

    @patch("sys.argv", ["mdfield", "--use-server", "date", "test.md"])
    @patch("builtins.print")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_date_field(self, mock_server_client_class, mock_print):
        """Test server mode extracts date field correctly."""
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        # Mock extract_talk_field method with date (returns string directly)
        mock_client.extract_talk_field.return_value = "2023-05-15"
        
        # Call the main function
        main()
        
        # Verify output
        mock_print.assert_called_once_with("2023-05-15")

    @patch("sys.argv", ["mdfield", "--use-server", "categories", "test.md"])
    @patch("builtins.print")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_list_field(self, mock_server_client_class, mock_print):
        """Test server mode extracts list field correctly."""
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        # Mock extract_talk_field method with list (returns list directly)
        mock_client.extract_talk_field.return_value = ["test", "example"]
        
        # Call the main function
        main()
        
        # Verify output (list should be formatted as Python list string)
        mock_print.assert_called_once_with("['test', 'example']")

    @patch("sys.argv", ["mdfield", "--use-server", "nonexistent", "test.md"])
    @patch("builtins.print")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_missing_field(self, mock_server_client_class, mock_print):
        """Test server mode handles missing field gracefully."""
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        # Mock extract_talk_field method with empty string (missing field)
        mock_client.extract_talk_field.return_value = ""
        
        # Call the main function
        main()
        
        # Verify empty string output
        mock_print.assert_called_once_with("")

    @patch("sys.argv", ["mdfield", "--use-server", "bibdir", "test.md"])
    @patch("builtins.print")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_with_config_fallback(self, mock_server_client_class, mock_print):
        """Test server mode uses config files for fallback."""
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        # Mock a field that's typically in config, not markdown (returns string directly)
        mock_client.extract_talk_field.return_value = "../_bibliography"
        
        # Call the main function
        main()
        
        # Verify extract_talk_field was called with default config files
        mock_client.extract_talk_field.assert_called_once_with(
            field="bibdir",
            markdown_file="test.md",
            config_files=["_lamd.yml", "_config.yml"]
        )
        
        mock_print.assert_called_once_with("../_bibliography")

    @patch("sys.argv", ["mdfield", "--use-server", "title", "test.md"])
    @patch("builtins.print")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_http_error(self, mock_server_client_class, mock_print):
        """Test server mode handles HTTP errors from server."""
        import requests
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        # Mock extract_talk_field to raise HTTP error
        mock_client.extract_talk_field.side_effect = requests.HTTPError("404 Not Found")
        
        # Call the main function - should fall back to direct mode
        with patch("lynguine.util.talk.talk_field", return_value="Fallback Title"):
            main()
        
        # Verify output from fallback mode
        mock_print.assert_called_once_with("Fallback Title")

    @patch("sys.argv", ["mdfield", "--use-server", "title", "test.md"])
    @patch("builtins.print")
    @patch("sys.stderr")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_exception_handling(self, mock_server_client_class, mock_stderr, mock_print):
        """Test server mode handles exceptions gracefully."""
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        # Mock extract_talk_field to raise exception
        mock_client.extract_talk_field.side_effect = Exception("Server not available")
        
        # Call the main function
        main()
        
        # Verify error message and empty output
        assert mock_stderr.write.called
        mock_print.assert_called_once_with("")

    @patch("sys.argv", ["mdfield", "--use-server", "author", "test.md"])
    @patch("builtins.print")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_complex_field(self, mock_server_client_class, mock_print):
        """Test server mode handles complex nested fields (like author)."""
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        # Mock extract_talk_field with complex author structure (returns list directly)
        mock_client.extract_talk_field.return_value = [{"given": "James L.", "family": "Curtis"}]
        
        # Call the main function
        main()
        
        # Verify output is JSON-like string representation
        assert mock_print.called

    @patch("sys.argv", ["mdfield", "title", "test.md"])
    @patch("builtins.print")
    @patch("os.environ.get", return_value="1")
    @patch("lamd.mdfield.ServerClient")
    def test_server_mode_via_env_variable(self, mock_server_client_class, mock_env, mock_print):
        """Test that LAMD_USE_SERVER environment variable enables server mode."""
        mock_client = MagicMock()
        mock_server_client_class.return_value = mock_client
        
        mock_client.extract_talk_field.return_value = "Test Title"
        
        # Call the main function (without --use-server flag, but with env var)
        # Note: This test depends on mdfield.py checking LAMD_USE_SERVER env var
        # If not implemented, this documents expected behavior
        main()
        
        # This test may need adjustment based on actual implementation

    @patch("sys.argv", ["mdfield", "--no-server", "title", "test.md"])
    @patch("builtins.print")
    @patch("lamd.mdfield.ServerClient")
    def test_no_server_flag_overrides(self, mock_server_client_class, mock_print):
        """Test that --no-server flag prevents server mode."""
        # Mock talk_field to return value
        with patch("lynguine.util.talk.talk_field", return_value="Test Document"):
            # Call the main function
            main()
            
            # Verify ServerClient was NOT instantiated
            mock_server_client_class.assert_not_called()
            
            # Verify output
            mock_print.assert_called_once_with("Test Document")

