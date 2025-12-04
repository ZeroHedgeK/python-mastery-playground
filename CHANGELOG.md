# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- GitHub Actions CI workflow with Python 3.10, 3.11, 3.12 matrix
- Pre-commit hooks for black, isort, ruff, and mypy
- Test coverage for context_managers module
- Test coverage for testing_patterns module
- Shared pytest fixtures in conftest.py
- MIT LICENSE file
- This CHANGELOG file

### Changed

- Moved context_managers documentation to docs/ folder

## [2.0.0] - 2024-12-01

### Added

- Complete restructure as `python_mastery` package
- Modular organization: concurrency, context_managers, datastructures, decorators, functional, internals, oop, testing_patterns
- Interactive CLI via `python -m python_mastery`
- Comprehensive examples/ directory with standalone demos
- Full test suite with pytest and pytest-asyncio
- Type hints throughout codebase
- Development tooling: black, flake8, mypy, isort

### Changed

- Migrated to `src/` layout for proper packaging
- Updated to pyproject.toml-based configuration
- Minimum Python version: 3.10+

## [1.0.0] - 2024-01-01

### Added

- Initial release with basic decorator and context manager examples
