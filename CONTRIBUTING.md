# Contributing to LAMD

Thank you for your interest in contributing to LAMD! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/lawrennd/lamd.git
   cd lamd
   ```

2. Install development dependencies using Poetry:
   ```bash
   poetry install --with dev
   ```

3. Install the GPP preprocessor:
   - On macOS: `brew install gpp`
   - On Linux: `apt-get install gpp`
   - On Windows: See [https://github.com/logological/gpp](https://github.com/logological/gpp)

## Testing

We use pytest for testing. All tests should be placed in the `tests/` directory:
- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with verbose output
poetry run pytest -v

# Run tests with coverage report
poetry run pytest --cov=lamd

# Run tests with detailed coverage report
poetry run pytest --cov=lamd --cov-report=term-missing
```

### Writing Tests

When writing new tests:
1. Follow the pattern in existing tests
2. Use `unittest.mock` to mock external dependencies
3. Create appropriate fixtures for test data
4. Aim for at least 80% code coverage
5. Use descriptive test names that explain what functionality is being tested

See the [Testing Documentation](docs/testing.md) for more details.

## Code Style

We follow PEP 8 coding standards. Before submitting code:

1. Run linters to check code quality:
   ```bash
   # Install linting tools
   poetry run pip install flake8 mypy

   # Run flake8
   poetry run flake8 lamd/

   # Run mypy for type checking
   poetry run mypy --ignore-missing-imports lamd/
   ```

2. Format your code:
   ```bash
   poetry run pip install black
   poetry run black lamd/
   ```

## Pull Request Process

1. Fork the repository and create a feature branch
2. Add or update tests for any new functionality
3. Ensure all tests pass and code is well-formatted
4. Submit a pull request with a clear description of the changes
5. Update documentation as needed

## Documentation

Documentation is written in Markdown and built with Sphinx. Update documentation for any new features or changes:

1. Add appropriate docstrings to code
2. Update documentation files in the `docs/` directory
3. Build and check documentation locally:
   ```bash
   cd docs
   make html
   # Check output in _build/html/
   ```

## CI/CD Pipeline

This repository uses GitHub Actions for continuous integration:

1. Tests run automatically on every push and pull request
2. Lint checks ensure code quality
3. Documentation is built and published automatically

The CI pipeline includes:
- Running unit and integration tests
- Code coverage reporting
- Linting and type checking
- Building documentation

## License

By contributing to this project, you agree that your contributions will be licensed under the project's license. 