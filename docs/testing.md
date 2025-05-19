# Testing Documentation for LAMD

This document outlines the testing approach and coverage for the LAMD (Lynguine Academic Markdown) project.

## Test Framework

LAMD uses pytest as its primary testing framework. Tests are organized as follows:

- Unit tests in `tests/unit/`
- Integration tests (future) in `tests/integration/`

## Running Tests

Tests can be run using the following commands:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage reporting
pytest --cov=lamd

# Run tests with detailed coverage reporting
pytest --cov=lamd --cov-report=term-missing
```

## Current Test Coverage

As of the latest update, the test coverage for the `mdpp.py` module is:

```
Name           Stmts   Miss  Cover
----------------------------------
lamd/mdpp.py     156     31    80%
----------------------------------
TOTAL            156     31    80%
```

### Test Coverage Details

The following parts of `mdpp.py` are currently tested:

1. Command-line argument handling via the parser
2. Core functionality including format and to flags processing
3. Code inclusion options
4. Directory configuration options 
5. Include and snippets paths handling
6. No-header mode operation
7. Error handling for missing configuration files

### Areas for Further Testing

The following areas could benefit from additional test coverage:

1. More file operation scenarios (e.g., include_before_body and include_after_body)
2. Exercises and assignment flag handling
3. Meta data handling
4. Extract material functionality
5. Replacement notation handling
6. Integration tests with the actual external gpp preprocessor

## Test Dependencies

Testing requires the following dependencies:

- pytest
- pytest-cov

These are specified in the project's `pyproject.toml` file under `tool.poetry.dev-dependencies`. 