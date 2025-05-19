#!/usr/bin/env python3

import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock, call
import builtins

import lynguine.util.yaml as ny
from lamd.makecv import main


class TestMakeCV(unittest.TestCase):
    """
    Test suite for the makecv module.
    """

    @patch("argparse.ArgumentParser.parse_args")
    @patch("os.system")
    @patch("os.path.dirname")
    @patch("lamd.config.interface.Interface.from_file")
    @patch("lynguine.util.talk.talk_field")
    @patch("os.path.exists")
    def test_main_function(self, mock_exists, mock_talk_field, mock_from_file, mock_dirname, mock_system, mock_args):
        """
        Test the main function of makecv.
        """
        # Set up mocks
        mock_args.return_value.filename = "example_cv.md"
        mock_dirname.return_value = "/mock/path"
        mock_exists.return_value = True
        mock_interface = MagicMock()

        def getitem_side_effect(key):
            if key == "snippetsdir":
                return "../_snippets"
            elif key == "bibdir":
                return "../_bib"
            return ""
        mock_interface.__getitem__.side_effect = getitem_side_effect
        mock_from_file.return_value = mock_interface
        mock_talk_field.side_effect = [ny.FileFormatError("Test error"), ny.FileFormatError("Test error")]

        real_open = builtins.open
        def open_side_effect(file, mode="r", *args, **kwargs):
            if file == "makefile":
                return mock_open()(file, mode, *args, **kwargs)
            return real_open(file, mode, *args, **kwargs)

        with patch("builtins.open", side_effect=open_side_effect):
            with self.assertRaises(SystemExit):
                main()

    @patch("argparse.ArgumentParser.parse_args")
    @patch("os.system")
    @patch("os.path.dirname")
    @patch("lamd.config.interface.Interface.from_file")
    @patch("lynguine.util.talk.talk_field")
    @patch("os.path.exists")
    def test_main_function_with_talk_fields(self, mock_exists, mock_talk_field, mock_from_file, mock_dirname, mock_system, mock_args):
        """
        Test the main function when talk_field succeeds for both fields.
        """
        mock_args.return_value.filename = "example_cv.md"
        mock_dirname.return_value = "/mock/path"
        mock_exists.return_value = True
        mock_interface = MagicMock()
        def getitem_side_effect(key):
            if key == "snippetsdir":
                return "../_snippets"
            elif key == "bibdir":
                return "../_bib"
            return ""
        mock_interface.__getitem__.side_effect = getitem_side_effect
        mock_from_file.return_value = mock_interface
        mock_talk_field.side_effect = ["snippets_path", "bib_path"]
        real_open = builtins.open
        def open_side_effect(file, mode="r", *args, **kwargs):
            if file == "makefile":
                return mock_open()(file, mode, *args, **kwargs)
            return real_open(file, mode, *args, **kwargs)
        with patch("builtins.open", side_effect=open_side_effect):
            with self.assertRaises(SystemExit):
                main()

    @patch("argparse.ArgumentParser.parse_args")
    @patch("os.system")
    @patch("os.path.dirname")
    @patch("lamd.config.interface.Interface.from_file")
    @patch("lynguine.util.talk.talk_field")
    @patch("os.path.exists")
    def test_main_function_with_empty_field(self, mock_exists, mock_talk_field, mock_from_file, mock_dirname, mock_system, mock_args):
        """
        Test the main function when a field is not present in the interface.
        """
        mock_args.return_value.filename = "empty_field_cv.md"
        mock_dirname.return_value = "/mock/path"
        mock_exists.return_value = True
        mock_interface = MagicMock()
        def getitem_side_effect(key):
            if key == "snippetsdir":
                return "../_snippets"
            elif key == "bibdir":
                return "../_bib"
            return ""
        mock_interface.__getitem__.side_effect = getitem_side_effect
        mock_from_file.return_value = mock_interface
        mock_talk_field.side_effect = [ny.FileFormatError("Error 1"), ny.FileFormatError("Error 2")]
        real_open = builtins.open
        def open_side_effect(file, mode="r", *args, **kwargs):
            if file == "makefile":
                return mock_open()(file, mode, *args, **kwargs)
            return real_open(file, mode, *args, **kwargs)
        with patch("builtins.open", side_effect=open_side_effect):
            with self.assertRaises(SystemExit):
                main()


if __name__ == "__main__":
    unittest.main()
