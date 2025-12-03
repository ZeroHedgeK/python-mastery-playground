# Python Mastery Playground

A comprehensive, hands-on repository for mastering Python. This project is structured as a series of modules, each covering a fundamental or advanced topic with implementation code, examples, and tests.

## Modules

| Module | Description |
|--------|-------------|
| **1. Advanced Patterns** | Decorators, Context Managers, Closures |
| **2. Data Structures** | Comprehensions, Generators, `collections` |
| **3. OOP** | Metaclasses, MRO, Magic Methods, Slots |
| **4. Concurrency** | AsyncIO, Multiprocessing, Threading |
| **5. Testing & Quality** | Pytest Fixtures, Mocking, Type Safety |
| **6. Functional** | Partial, Reduce, Immutability, Recursion |
| **7. Internals** | Bytecode Disassembly, Memory Management, GC |

## Project Structure

```
python-mastery-playground/
├── src/
│   └── python_mastery/      # Main package
│       ├── concurrency/
│       ├── context_managers/
│       ├── datastructures/
│       ├── decorators/
│       ├── functional/
│       ├── internals/
│       ├── oop/
│       └── testing_patterns/
├── examples/                 # Runnable example scripts
├── tests/                    # Test suite
├── pyproject.toml           # Project configuration
└── Makefile                 # Common commands
```

## Quick Start

### Installation

```bash
# Install in development mode
pip install -e ".[dev]"
```

### Running Examples

```bash
# Decorator examples
python examples/timer.py
python examples/cache.py
python examples/rate_limit.py

# Context manager examples
python examples/context_manager_examples.py

# Run the package directly
python -m python_mastery
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific module tests
pytest tests/test_decorators.py
pytest tests/test_concurrency.py

# Run with verbose output
make test
```

### Code Quality

```bash
# Format code
make format

# Run linters
make lint

# Clean build artifacts
make clean
```

## Requirements

- Python 3.10+
- No external runtime dependencies (uses standard library)
- Dev dependencies: `pytest`, `pytest-asyncio`, `mypy`, `black`, `flake8`, `isort`

## License

MIT License
