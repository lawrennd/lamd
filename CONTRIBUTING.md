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

3. Install pre-commit hooks (recommended):
   ```bash
   poetry run pre-commit install --install-hooks
   ```
   This runs `black` and `isort` before each commit, and `mypy` before each push,
   using the same tools and versions as CI (`poetry install --with dev`).

4. Install the GPP preprocessor:
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

We follow PEP 8 coding standards. Lint tools are Poetry dev dependencies; CI uses
`poetry install --with dev` so local and CI versions stay aligned.

With pre-commit hooks installed (see Development Setup), formatting and import sorting
run automatically on commit, and mypy runs on push.

To run checks manually:

```bash
poetry run black --check .
poetry run isort --check-only .
poetry run flake8 .
poetry run mypy --strict --ignore-missing-imports --disallow-untyped-defs --disallow-incomplete-defs lamd/
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