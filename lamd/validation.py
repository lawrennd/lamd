#!/usr/bin/env python3
"""
Validation module for LaMD tools.

This module provides functions for validating files, paths, and arguments used in LaMD tools.
It includes custom exception classes and validation functions for various input types.
"""

import os
import sys
from typing import List, Optional, Tuple


class ValidationError(Exception):
    """Base class for validation errors in LaMD tools."""


class FileNotFoundError(ValidationError):
    """Exception raised when a required file is not found."""


class DirectoryNotFoundError(ValidationError):
    """Exception raised when a required directory is not found."""


class ArgumentValidationError(ValidationError):
    """Exception raised when command line arguments are invalid."""


def validate_file_exists(filepath: str, description: str = "file") -> None:
    """Validate that a file exists.

    :param filepath: Path to the file to validate
    :type filepath: str
    :param description: Description of the file for error messages
    :type description: str
    :raises FileNotFoundError: If the file doesn't exist
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"{description.capitalize()} not found: {filepath}")


def validate_directory_exists(dirpath: str, description: str = "directory") -> None:
    """Validate that a directory exists.

    :param dirpath: Path to the directory to validate
    :type dirpath: str
    :param description: Description of the directory for error messages
    :type description: str
    :raises DirectoryNotFoundError: If the directory doesn't exist
    """
    if not os.path.isdir(dirpath):
        raise DirectoryNotFoundError(f"{description.capitalize()} not found: {dirpath}")


def validate_include_paths(paths: Optional[str]) -> List[str]:
    """Validate include paths and return list of valid directories.

    :param paths: Colon-separated list of include paths
    :type paths: Optional[str]
    :return: List of valid include directories
    :rtype: List[str]
    :raises DirectoryNotFoundError: If any required include directory doesn't exist
    """
    if not paths:
        return []

    valid_paths = []
    for path in paths.split(":"):
        if path:  # Skip empty paths
            try:
                validate_directory_exists(path, "include directory")
                valid_paths.append(path)
            except DirectoryNotFoundError as e:
                print(f"Warning: {e}", file=sys.stderr)

    return valid_paths


def validate_output_format(format_type: str, valid_formats: List[str]) -> None:
    """Validate output format.

    :param format_type: Format to validate
    :type format_type: str
    :param valid_formats: List of valid formats
    :type valid_formats: List[str]
    :raises ArgumentValidationError: If format is invalid
    """
    if format_type not in valid_formats:
        raise ArgumentValidationError(f"Invalid format: {format_type}. Must be one of: {', '.join(valid_formats)}")


def validate_code_level(code_level: str, valid_levels: List[str]) -> None:
    """Validate code inclusion level.

    :param code_level: Code level to validate
    :type code_level: str
    :param valid_levels: List of valid code levels
    :type valid_levels: List[str]
    :raises ArgumentValidationError: If code level is invalid
    """
    if code_level not in valid_levels:
        raise ArgumentValidationError(f"Invalid code level: {code_level}. Must be one of: {', '.join(valid_levels)}")


def validate_metadata(metadata: Optional[List[str]]) -> List[Tuple[str, str]]:
    """Validate metadata key-value pairs.

    :param metadata: List of metadata strings in KEY=VALUE format
    :type metadata: Optional[List[str]]
    :return: List of (key, value) tuples
    :rtype: List[Tuple[str, str]]
    :raises ArgumentValidationError: If metadata format is invalid
    """
    if not metadata:
        return []

    valid_metadata = []
    for item in metadata:
        try:
            key, value = item.split("=", 1)
            valid_metadata.append((key.strip(), value.strip()))
        except ValueError:
            raise ArgumentValidationError(f"Invalid metadata format: {item}. Must be KEY=VALUE")

    return valid_metadata
