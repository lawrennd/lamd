# LAMD Tests

This directory contains the test suite for the LAMD (Lynguine Academic Markdown) project.

## Directory Structure

```
tests/
├── unit/           # Unit tests
│   └── test_mdpp.py # Tests for the mdpp module
├── integration/    # Integration tests (future)
└── README.md       # This file
```

## Running Tests

You can run the tests using pytest:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests for a specific module
pytest tests/unit/test_mdpp.py

# Run a specific test
pytest tests/unit/test_mdpp.py::TestMdpp::test_help_flag

# Run tests with coverage reporting
pytest --cov=lamd

# Run tests with detailed coverage reporting
pytest --cov=lamd --cov-report=term-missing
```

## Writing New Tests

When writing new tests, follow these guidelines:

1. **Test Organization**:
   - Create unit tests in the `unit/` directory
   - Name test files as `test_<module>.py`
   - Name test classes as `Test<ModuleName>`
   - Name test methods as `test_<functionality>`

2. **Mocking**:
   - Use `unittest.mock` for mocking dependencies
   - Mock external system calls to avoid side effects
   - Use `@patch` decorators to mock functions and classes

3. **Test Coverage**:
   - Aim for at least 80% test coverage
   - Focus on testing edge cases and error handling
   - Check the coverage report to identify untested code

4. **Test Setup**:
   - Use `setup_method` and `teardown_method` for test setup and cleanup
   - Create temporary files and directories for testing file operations

## Test Dependencies

The test suite requires the following dependencies:

- pytest
- pytest-cov

These are specified in the project's `pyproject.toml` file under `tool.poetry.dev-dependencies`.

## Documentation

For more detailed information about testing in LAMD, see [docs/testing.md](../docs/testing.md). 