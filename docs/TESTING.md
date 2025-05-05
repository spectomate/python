---
title: "Spectomate Testing Guide"
description: "Comprehensive guide to testing tools and workflows for the Spectomate package"
author: "Spectomate Team"
keywords: "spectomate, testing, python, pytest, code quality, CI/CD, GitHub Actions, unit testing"
lang: "en"
---

# Spectomate Testing Guide

This document describes the testing tools and workflows available in the Spectomate package.

## Testing Features

- **Command-line interface**: Run tests directly using the Spectomate CLI
- **Automated code quality checks**: Run black, isort, flake8, and mypy
- **Unit testing**: Run pytest with coverage reporting
- **GitHub Actions integration**: Automated testing on multiple Python versions
- **Local testing script**: Convenient script for running all tests locally

## Using the CLI for Testing

Spectomate includes a built-in test command group that makes it easy to run various code quality checks and tests.

### Basic Commands

```bash
# Format code with black
spectomate test black spectomate tests

# Sort imports with isort
spectomate test isort spectomate tests

# Run flake8 linting
spectomate test flake8 spectomate

# Run pytest unit tests
spectomate test pytest tests

# Run all tests and code quality checks
spectomate test all
```

### Command Details

#### Black Command

The `black` command formats your code using the Black code formatter:

```bash
spectomate test black [PATHS] [OPTIONS]
```

Options:
- `--check`: Only check formatting without modifying files
- `--verbose, -v`: Show verbose output

#### Isort Command

The `isort` command sorts imports in your Python files:

```bash
spectomate test isort [PATHS] [OPTIONS]
```

Options:
- `--check`: Only check import sorting without modifying files
- `--verbose, -v`: Show verbose output

#### Flake8 Command

The `flake8` command runs linting checks on your code:

```bash
spectomate test flake8 [PATHS] [OPTIONS]
```

Options:
- `--verbose, -v`: Show verbose output

#### Pytest Command

The `pytest` command runs unit tests:

```bash
spectomate test pytest [PATHS] [OPTIONS]
```

Options:
- `--verbose, -v`: Show verbose output
- `--coverage, -c`: Run with coverage report

#### All Command

The `all` command runs all tests and code quality checks:

```bash
spectomate test all [PATHS] [OPTIONS]
```

Options:
- `--fix`: Fix issues automatically where possible
- `--skip-lint`: Skip linting checks
- `--skip-tests`: Skip unit tests
- `--skip-mypy`: Skip mypy type checking
- `--verbose, -v`: Show verbose output

## Local Testing Script

For convenience, Spectomate includes a script to run all tests locally:

```bash
# Run all tests
python scripts/run_tests.py

# Run tests with automatic fixing
python scripts/run_tests.py --fix

# Run tests with verbose output
python scripts/run_tests.py --verbose

# Skip certain checks
python scripts/run_tests.py --skip-mypy
```

## GitHub Actions Workflow

Spectomate includes a GitHub Actions workflow that automatically runs tests on multiple Python versions (3.8-3.12) whenever code is pushed to the main/master branch or when a pull request is created.

The workflow runs the following checks:
- Flake8 linting
- Black code formatting
- Isort import sorting
- Mypy type checking
- Pytest unit tests with coverage reporting

### Workflow Configuration

The workflow is defined in `.github/workflows/python-tests.yml`. You can customize this file to change the testing behavior.

## Best Practices for Testing

1. **Run tests locally before pushing**: Use the CLI or testing script to run tests locally before pushing changes
2. **Keep test coverage high**: Aim for high test coverage to ensure code quality
3. **Fix linting issues**: Address linting issues to maintain code quality
4. **Use type annotations**: Add type annotations to make code more maintainable
5. **Automate formatting**: Use the `--fix` option to automatically format code

## Continuous Integration

The GitHub Actions workflow provides continuous integration for the Spectomate package. It ensures that all tests pass on multiple Python versions before code is merged.

To view the test results, go to the "Actions" tab in your GitHub repository.

## Adding New Tests

When adding new features to Spectomate, be sure to add corresponding tests:

1. Add unit tests in the `tests/` directory
2. Run the tests locally to ensure they pass
3. Push your changes to trigger the GitHub Actions workflow
