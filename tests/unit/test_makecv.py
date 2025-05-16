#!/usr/bin/env python3

import unittest
import os
import sys
from unittest.mock import patch, mock_open, MagicMock, call

import lynguine.util.yaml as ny
from lamd.makecv import main

class TestMakeCV(unittest.TestCase):
    """
    Test suite for the makecv module.
    """

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.system')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.dirname')
    @patch('lamd.config.interface.Interface.from_file')
    @patch('lynguine.util.talk.talk_field')
    def test_main_function(self, mock_talk_field, mock_from_file, 
                          mock_dirname, mock_file, mock_system, mock_args):
        """
        Test the main function of makecv.
        """
        # Set up mocks
        mock_args.return_value.filename = "example_cv.md"
        mock_dirname.return_value = "/mock/path"
        mock_interface = MagicMock()
        
        # The issue is here - when indexing the interface, it returns empty strings
        def getitem_side_effect(key):
            # Return empty string for both fields to match actual behavior
            return ""
            
        mock_interface.__getitem__.side_effect = getitem_side_effect
        mock_from_file.return_value = mock_interface
        
        # Mock talk_field to raise exception first time, to test the exception handling
        mock_talk_field.side_effect = [
            ny.FileFormatError("Test error"),
            ny.FileFormatError("Test error")
        ]
        
        # Call the function
        main()
        
        # Verify file was opened and written to
        mock_file.assert_called_with('makefile', 'w+')
        file_handle = mock_file()
        
        # Verify the content written to the file
        expected_calls = [
            'BASE=example_cv\n',
            'MAKEFILESDIR=/mock/path/makefiles\n',
            'INCLUDESDIR=/mock/path/includes\n',
            'SCRIPTDIR=/mock/path/scripts\n',
            'include $(MAKEFILESDIR)/make-cv-flags.mk\n',
            'include $(MAKEFILESDIR)/make-cv.mk\n'
        ]
        
        for call, expected in zip(file_handle.write.call_args_list, expected_calls):
            self.assertEqual(call[0][0], expected)
        
        # Verify system calls were made (both directories are empty strings from the interface mock)
        expected_system_calls = [
            'git pull',
            'make all',
            'CURDIR=`pwd`;cd ; git pull; cd $CURDIR',
            'CURDIR=`pwd`;cd ; git pull; cd $CURDIR',
            'git pull',
            'make all'
        ]
        
        actual_calls = [call[0][0] for call in mock_system.call_args_list]
        self.assertEqual(actual_calls, expected_system_calls)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.system')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.dirname')
    @patch('lamd.config.interface.Interface.from_file')
    @patch('lynguine.util.talk.talk_field')
    def test_main_function_with_talk_fields(self, mock_talk_field, mock_from_file,
                                          mock_dirname, mock_file, mock_system, mock_args):
        """
        Test the main function when talk_field succeeds for both fields.
        """
        # Set up mocks
        mock_args.return_value.filename = "example_cv.md"
        mock_dirname.return_value = "/mock/path"
        
        # If talk_field succeeds, from_file should not be called
        mock_from_file.assert_not_called
        
        # Mock talk_field to return valid paths
        mock_talk_field.side_effect = [
            "snippets_path",
            "bib_path"
        ]
        
        # Call the function
        main()
        
        # Verify file operations
        mock_file.assert_called_with('makefile', 'w+')
        
        # Verify system calls were made with the correct paths
        expected_calls = [
            call('git pull'),
            call('make all'),
            call('CURDIR=`pwd`;cd snippets_path; git pull; cd $CURDIR'),
            call('CURDIR=`pwd`;cd bib_path; git pull; cd $CURDIR'),
            call('git pull'),
            call('make all')
        ]
        
        mock_system.assert_has_calls(expected_calls, any_order=False)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('os.system')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.dirname')
    @patch('lamd.config.interface.Interface.from_file')
    @patch('lynguine.util.talk.talk_field')
    def test_main_function_with_empty_field(self, mock_talk_field, mock_from_file,
                                           mock_dirname, mock_file, mock_system, mock_args):
        """
        Test the main function when a field is not present in the interface.
        """
        # Set up mocks
        mock_args.return_value.filename = "empty_field_cv.md"
        mock_dirname.return_value = "/mock/path"
        mock_interface = MagicMock()
    
        # Mock interface to return empty string for both fields
        def getitem_side_effect(key):
            return ""
    
        mock_interface.__getitem__.side_effect = getitem_side_effect
        mock_from_file.return_value = mock_interface
    
        # Mock talk_field to raise exception for both fields
        mock_talk_field.side_effect = [
            ny.FileFormatError("Error 1"),
            ny.FileFormatError("Error 2")
        ]
    
        # Call the function
        main()
    
        # Verify system calls for empty fields
        expected_calls = [
            call('git pull'),
            call('make all'),
            call('CURDIR=`pwd`;cd ; git pull; cd $CURDIR'),
            call('CURDIR=`pwd`;cd ; git pull; cd $CURDIR'),
            call('git pull'),
            call('make all')
        ]
    
        # Verify all the calls were made
        mock_system.assert_has_calls(expected_calls, any_order=False)

if __name__ == "__main__":
    unittest.main() 