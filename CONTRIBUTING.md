# Contributing to Python Mastery Playground

Thank you for your interest in contributing to Python Mastery Playground! We welcome contributions from developers of all skill levels.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Types of Contributions

We appreciate all kinds of contributions:

- 🐛 **Bug fixes**: Help us squash bugs
- ✨ **New features**: Add new examples, modules, or demonstrations
- 📝 **Documentation**: Improve or add documentation, comments, or examples
- 🧪 **Tests**: Add or improve test coverage
- 🎨 **Code quality**: Refactor code, improve performance, or enhance type hints

### Good First Issues

Look for issues labeled `good first issue` for beginner-friendly tasks.

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Basic familiarity with virtual environments

### Setup Instructions

1. **Fork the repository** on GitHub

2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/python-mastery-playground.git
   cd python-mastery-playground
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

5. **Install pre-commit hooks** (optional but recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

6. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Coding Standards

### Code Style

We follow industry-standard Python conventions:

- **PEP 8**: Python code style guide
- **Black**: Automatic code formatting (line length: 88)
- **isort**: Import sorting with black profile
- **Type hints**: Use type hints for all public APIs

### Running Code Quality Tools

Format your code:
```bash
make format
```

Run linters:
```bash
make lint
```

Run tests:
```bash
make test
```

Run tests with coverage:
```bash
make test-cov
```

### Code Quality Requirements

All contributions must:

- ✅ Pass all existing tests
- ✅ Have test coverage for new code (minimum 80% coverage)
- ✅ Pass black formatting check
- ✅ Pass ruff linting
- ✅ Pass mypy type checking
- ✅ Include docstrings for all public functions/classes
- ✅ Include comments explaining complex logic

### Documentation Style

- Use **Google-style docstrings**
- Include **examples** in docstrings when helpful
- Add **inline comments** to explain non-obvious code
- Update **README.md** if adding new modules

Example docstring:
```python
def example_function(param: str, count: int) -> list[str]:
    """
    Brief one-line description.

    Longer description explaining what the function does,
    when to use it, and any important details.

    Args:
        param: Description of param
        count: Description of count

    Returns:
        Description of return value

    Raises:
        ValueError: When count is negative

    Example:
        >>> example_function("hello", 3)
        ['hello', 'hello', 'hello']
    """
```

## Submitting Changes

### Before Submitting

1. **Run all tests**:
   ```bash
   make test
   ```

2. **Run code quality checks**:
   ```bash
   make format
   make lint
   ```

3. **Update documentation** if needed

4. **Add tests** for your changes

5. **Commit your changes** with clear messages:
   ```bash
   git add .
   git commit -m "Add feature: brief description

   Detailed explanation of what changed and why."
   ```

### Pull Request Process

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to any related issues
   - Screenshots (if applicable)

3. **Wait for review**:
   - Maintainers will review your PR
   - Address any feedback
   - Once approved, it will be merged

### Pull Request Template

When opening a PR, please include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Test improvement

## Testing
- [ ] All tests pass
- [ ] Added new tests for changes
- [ ] Manually tested changes

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented if necessary)
```

## Reporting Bugs

### Before Reporting

- Check if the bug has already been reported in [Issues](https://github.com/ZeroHedgeK/python-mastery-playground/issues)
- Try to reproduce the bug with the latest version
- Collect relevant information (Python version, OS, error messages)

### Bug Report Template

When reporting bugs, include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Exact steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - Python version
   - Operating system
   - Package version
6. **Additional Context**: Any other relevant information

## Suggesting Enhancements

We welcome suggestions for new features or improvements!

### Enhancement Request Template

1. **Is your feature request related to a problem?**
   - Describe the problem

2. **Describe the solution you'd like**
   - Clear description of what you want

3. **Describe alternatives you've considered**
   - Other solutions you've thought about

4. **Additional context**
   - Any other relevant information

## Questions?

If you have questions about contributing:

- Open a [Discussion](https://github.com/ZeroHedgeK/python-mastery-playground/discussions)
- Review existing issues and PRs
- Read the [README.md](README.md)

## Recognition

All contributors will be recognized in our repository. Thank you for helping make Python Mastery Playground better!

---

**Happy Contributing! 🎉**
