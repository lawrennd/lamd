#!/usr/bin/env python3
"""
Validation module for LaMD tools.

This module provides functions for validating files, paths, and arguments used in LaMD tools.
It includes custom exception classes and validation functions for various input types.
"""

import os
import sys
import subprocess
import shutil
from typing import List, Optional, Tuple, Dict, Any


class ValidationError(Exception):
    """Base class for validation errors in LaMD tools."""


class FileNotFoundError(ValidationError):
    """Exception raised when a required file is not found."""


class DirectoryNotFoundError(ValidationError):
    """Exception raised when a required directory is not found."""


class ArgumentValidationError(ValidationError):
    """Exception raised when command line arguments are invalid."""


class DependencyError(ValidationError):
    """Exception raised when a dependency is missing or incompatible."""


def check_dependency(dependency_name: str) -> bool:
    """Check if a dependency is installed and accessible.

    :param dependency_name: Name of the dependency to check
    :type dependency_name: str
    :return: True if the dependency is available, False otherwise
    :rtype: bool
    """
    return shutil.which(dependency_name) is not None


def check_version(dependency_name: str, required_version: str) -> bool:
    """Check if a dependency meets the required version.

    :param dependency_name: Name of the dependency to check
    :type dependency_name: str
    :param required_version: Required version of the dependency
    :type required_version: str
    :return: True if the dependency version is compatible, False otherwise
    :rtype: bool
    """
    try:
        result = subprocess.run([dependency_name, "--version"], capture_output=True, text=True)
        installed_version = result.stdout.strip()
        return installed_version >= required_version
    except subprocess.CalledProcessError:
        return False


def resolve_dependencies(dependencies: Dict[str, str], auto_install: bool = False) -> None:
    """Resolve and optionally install dependencies using Poetry.

    :param dependencies: Dictionary of dependency names and required versions
    :type dependencies: Dict[str, str]
    :param auto_install: Whether to automatically install missing dependencies
    :type auto_install: bool
    :raises DependencyError: If dependencies cannot be resolved
    """
    try:
        # Check if poetry is installed
        if not check_dependency("poetry"):
            raise DependencyError("Poetry is required for dependency management")

        # Check if we're in a poetry project
        if not os.path.exists("pyproject.toml"):
            raise DependencyError("Not in a Poetry project (pyproject.toml not found)")

        if auto_install:
            # Add dependencies to pyproject.toml
            for dep, version in dependencies.items():
                try:
                    subprocess.run(["poetry", "add", f"{dep}=={version}"], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as e:
                    raise DependencyError(f"Failed to add dependency {dep}: {e.stderr}")

            # Install dependencies
            try:
                subprocess.run(["poetry", "install"], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                raise DependencyError(f"Failed to install dependencies: {e.stderr}")
        else:
            # Just check if dependencies are installed
            try:
                result = subprocess.run(["poetry", "show"], check=True, capture_output=True, text=True)
                installed_deps = {line.split()[0]: line.split()[1] for line in result.stdout.splitlines() if line.strip()}

                missing_deps = [
                    dep for dep, version in dependencies.items() if dep not in installed_deps or installed_deps[dep] < version
                ]
                if missing_deps:
                    raise DependencyError(
                        f"Missing or outdated dependencies: {', '.join(missing_deps)}. "
                        "Run with --auto-install to install them."
                    )
            except subprocess.CalledProcessError as e:
                raise DependencyError(f"Failed to check dependencies: {e.stderr}")
    except Exception as e:
        raise DependencyError(f"Failed to resolve dependencies: {str(e)}")


def install_dependency(dependency_name: str, version: Optional[str] = None) -> None:
    """Install a dependency using Poetry.

    :param dependency_name: Name of the dependency to install
    :type dependency_name: str
    :param version: Optional version to install
    :type version: Optional[str]
    :raises DependencyError: If installation fails
    """
    if not check_dependency("poetry"):
        raise DependencyError("Poetry is required for dependency management")

    try:
        cmd = ["poetry", "add"]
        if version:
            cmd.append(f"{dependency_name}=={version}")
        else:
            cmd.append(dependency_name)

        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise DependencyError(f"Failed to install {dependency_name}: {e.stderr}")


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
