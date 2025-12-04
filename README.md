# Python Mastery Playground

<div align="center">

[![CI](https://github.com/ZeroHedgeK/python-mastery-playground/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ZeroHedgeK/python-mastery-playground/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![codecov](https://codecov.io/gh/ZeroHedgeK/python-mastery-playground/branch/main/graph/badge.svg)](https://codecov.io/gh/ZeroHedgeK/python-mastery-playground)

</div>

A comprehensive, hands-on repository for mastering Python. This project is structured as a series of modules, each covering a fundamental or advanced topic with implementation code, examples, and tests.

**This repository is designed for self-study.** Every file contains detailed comments explaining not just *what* the code does, but *why* it works that way.

---

## 📚 How to Study This Repository

### Prerequisites

Before diving in, you should be comfortable with:
- Basic Python syntax (variables, functions, classes, loops)
- How to use `pip` and virtual environments
- Basic command line usage

### Recommended Learning Path

We suggest studying the modules in this order, as each builds on concepts from previous ones:

| Order | Module | Time Estimate | Key Concepts |
|-------|--------|---------------|--------------|
| 1 | **Decorators** | 2-3 hours | Functions as first-class objects, closures, `@` syntax |
| 2 | **Context Managers** | 1-2 hours | `with` statement, `__enter__`/`__exit__`, resource management |
| 3 | **Data Structures** | 2-3 hours | Comprehensions, generators, `collections` module |
| 4 | **OOP** | 3-4 hours | Metaclasses, MRO, magic methods, `__slots__` |
| 5 | **Functional** | 2-3 hours | `partial`, `reduce`, immutability, pure functions |
| 6 | **Concurrency** | 3-4 hours | Threading vs multiprocessing vs asyncio |
| 7 | **Internals** | 2-3 hours | Bytecode, reference counting, garbage collection |
| 8 | **Testing Patterns** | 2-3 hours | Pytest fixtures, mocking, type safety |

### Study Method (For Each Module)

Follow this 4-step process for maximum retention:

#### Step 1: Read the Source Code
```bash
# Start with the module's __init__.py to see what's exported
cat src/python_mastery/decorators/__init__.py

# Then read each implementation file carefully
# Files are heavily commented to explain every concept
```

#### Step 2: Run the Examples
```bash
# Examples show the concepts in action
python examples/timer.py
python examples/cache.py

# Or run all demos interactively
python -m python_mastery
```

#### Step 3: Study the Tests
```bash
# Tests demonstrate expected behavior and edge cases
# Read them to understand how the code SHOULD work
cat tests/test_decorators.py

# Run tests to verify your understanding
pytest tests/test_decorators.py -v
```

#### Step 4: Experiment!
```bash
# Modify the code, break things, fix them
# Add print statements to trace execution
# Write your own tests for edge cases
```

---

## 🗂 Module Deep Dive

### Module 1: Decorators (`src/python_mastery/decorators/`)

**What you'll learn:**
- How functions are first-class objects in Python
- Closures and how they capture variables
- Writing decorators with and without arguments
- Using `functools.wraps` to preserve metadata
- Thread-safe decorator implementations

**Key files to study:**
| File | Concept | Difficulty |
|------|---------|------------|
| `timer.py` | Basic decorator without arguments | ⭐ Beginner |
| `retry.py` | Decorator with arguments, exception handling | ⭐⭐ Intermediate |
| `cache.py` | Thread-safe caching, TTL expiration, async support | ⭐⭐⭐ Advanced |
| `rate_limit.py` | Thread-safe rate limiting, custom exceptions | ⭐⭐⭐ Advanced |

**Try this exercise:** Create a `@log_calls` decorator that logs function name, arguments, and return value.

---

### Module 2: Context Managers (`src/python_mastery/context_managers/`)

**What you'll learn:**
- The `with` statement protocol (`__enter__` / `__exit__`)
- Using `@contextmanager` decorator for simpler syntax
- Resource cleanup patterns
- Async context managers

**Key files to study:**
| File | Concept | Difficulty |
|------|---------|------------|
| `timer.py` | Class-based vs decorator-based context managers | ⭐ Beginner |
| `state.py` | Temporarily modifying state | ⭐⭐ Intermediate |
| `reentrant.py` | Single-use vs reusable context managers | ⭐⭐ Intermediate |
| `async_ctx.py` | Async context managers | ⭐⭐⭐ Advanced |

**Try this exercise:** Create a context manager that temporarily changes the current working directory.

---

### Module 3: Data Structures (`src/python_mastery/datastructures/`)

**What you'll learn:**
- List/dict/set comprehensions and when to use them
- Generator expressions for memory efficiency
- `collections` module (`Counter`, `defaultdict`, `deque`, `namedtuple`)

**Key files to study:**
| File | Concept | Difficulty |
|------|---------|------------|
| `builtins.py` | Slicing, comprehensions, generators | ⭐ Beginner |
| `collections_demo.py` | Specialized container types | ⭐⭐ Intermediate |

**Try this exercise:** Rewrite a nested loop as a generator expression.

---

### Module 4: OOP (`src/python_mastery/oop/`)

**What you'll learn:**
- Method Resolution Order (MRO) and multiple inheritance
- Metaclasses: "classes that create classes"
- Magic/dunder methods for operator overloading
- `__slots__` for memory optimization

**Key files to study:**
| File | Concept | Difficulty |
|------|---------|------------|
| `inheritance.py` | MRO, mixins, `super()` | ⭐⭐ Intermediate |
| `magic_methods.py` | `__add__`, `__len__`, `__getitem__`, etc. | ⭐⭐ Intermediate |
| `advanced_classes.py` | Singleton, properties, slots | ⭐⭐⭐ Advanced |
| `metaclasses.py` | Custom class creation | ⭐⭐⭐ Advanced |

**Try this exercise:** Create a class that behaves like a dictionary but logs every access.

---

### Module 5: Concurrency (`src/python_mastery/concurrency/`)

**What you'll learn:**
- Threading for I/O-bound tasks
- Multiprocessing for CPU-bound tasks
- AsyncIO for high-concurrency I/O
- When to use each approach

**Key files to study:**
| File | Concept | Difficulty |
|------|---------|------------|
| `threading_demo.py` | Thread pools, GIL limitations | ⭐⭐ Intermediate |
| `multiprocessing_demo.py` | Process pools, avoiding GIL | ⭐⭐ Intermediate |
| `asyncio_demo.py` | Event loop, coroutines, `gather` | ⭐⭐⭐ Advanced |

**Try this exercise:** Measure the speedup of multiprocessing vs threading for a CPU-bound task.

---

### Module 6: Functional Programming (`src/python_mastery/functional/`)

**What you'll learn:**
- `functools.partial` for partial application
- `functools.reduce` for folding operations
- Immutability with frozen dataclasses
- Pure functions vs functions with side effects

**Key files to study:**
| File | Concept | Difficulty |
|------|---------|------------|
| `functional_tools.py` | `partial`, `reduce`, `itertools` | ⭐⭐ Intermediate |
| `immutability.py` | Frozen dataclasses, pure functions | ⭐⭐ Intermediate |

**Try this exercise:** Rewrite an imperative loop using `reduce`.

---

### Module 7: Python Internals (`src/python_mastery/internals/`)

**What you'll learn:**
- How Python compiles code to bytecode
- Reference counting and garbage collection
- Memory management and optimization

**Key files to study:**
| File | Concept | Difficulty |
|------|---------|------------|
| `bytecode_inspector.py` | `dis` module, bytecode analysis | ⭐⭐⭐ Advanced |
| `memory_management.py` | `sys.getrefcount`, `gc` module | ⭐⭐⭐ Advanced |

**Try this exercise:** Use `dis.dis()` to compare the bytecode of a list comprehension vs a for loop.

---

### Module 8: Testing Patterns (`src/python_mastery/testing_patterns/`)

**What you'll learn:**
- Writing effective pytest tests
- Fixtures for test setup/teardown
- Mocking external dependencies
- Type hints with `Protocol` and generics

**Key files to study:**
| File | Concept | Difficulty |
|------|---------|------------|
| `type_safety.py` | Generics, Protocol, TypedDict | ⭐⭐ Intermediate |
| `external_services.py` | Dependency injection for testability | ⭐⭐ Intermediate |
| `tests/conftest.py` | Shared fixtures | ⭐⭐ Intermediate |

**Try this exercise:** Write a test that mocks `time.sleep` to run instantly.

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/ZeroHedgeK/python-mastery-playground.git
cd python-mastery-playground

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Running Examples

```bash
# Interactive module selector
python -m python_mastery

# Or run specific examples
python examples/timer.py
python examples/cache.py
python examples/rate_limit.py
python examples/context_manager_examples.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests for a specific module
pytest tests/test_decorators.py -v

# Run with coverage report
pytest --cov=python_mastery --cov-report=html
```

### Code Quality Commands

```bash
make format    # Format code with black + isort
make lint      # Run ruff + mypy
make test      # Run test suite
make clean     # Remove build artifacts
```

---

## 📁 Project Structure

```
python-mastery-playground/
├── src/python_mastery/       # Main package (study these!)
│   ├── decorators/           # @timer, @retry, @cache, @rate_limit
│   ├── context_managers/     # with statement patterns
│   ├── datastructures/       # comprehensions, generators, collections
│   ├── oop/                  # metaclasses, MRO, magic methods
│   ├── functional/           # partial, reduce, immutability
│   ├── concurrency/          # threading, multiprocessing, asyncio
│   ├── internals/            # bytecode, memory, GC
│   ├── testing_patterns/     # pytest patterns, mocking
│   └── exceptions.py         # Custom exception hierarchy
├── examples/                 # Runnable example scripts
├── tests/                    # Test suite (also great for learning!)
├── docs/                     # Additional documentation
├── pyproject.toml           # Project configuration
└── Makefile                 # Common commands
```

---

## 🤝 Contributing

Found a bug? Have a suggestion? Contributions are welcome!

Please see our [Contributing Guide](CONTRIBUTING.md) for detailed information on:

- Setting up your development environment
- Coding standards and best practices  
- How to submit pull requests
- Running tests and quality checks

For bug reports, feature requests, or questions, please use our [issue templates](.github/ISSUE_TEMPLATE/).

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`make test`) and linting (`make lint`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

---

## 🔒 Security

For security vulnerabilities, please see our [Security Policy](SECURITY.md) for responsible disclosure guidelines.

---

## 📋 Requirements

- **Python 3.10+** (uses modern type hint syntax)
- **No runtime dependencies** (uses only standard library)
- **Dev dependencies:** `pytest`, `pytest-asyncio`, `pytest-cov`, `mypy`, `black`, `ruff`, `isort`

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📖 Citation

If you use this project for academic purposes, please cite it using the information in [CITATION.cff](CITATION.cff).

---

## ⭐ Support

If this repository helped you learn Python, please consider:

- ⭐ Starring the repository on GitHub
- 📢 Sharing it with others who are learning Python
- 🐛 Reporting bugs or suggesting improvements
- 🤝 Contributing to the project

---

## 📬 Connect

- **Issues**: [GitHub Issues](https://github.com/ZeroHedgeK/python-mastery-playground/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ZeroHedgeK/python-mastery-playground/discussions)
- **Security**: See [SECURITY.md](SECURITY.md)

---

<div align="center">

**Made with ❤️ for Python learners**

[![GitHub stars](https://img.shields.io/github/stars/ZeroHedgeK/python-mastery-playground?style=social)](https://github.com/ZeroHedgeK/python-mastery-playground/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/ZeroHedgeK/python-mastery-playground?style=social)](https://github.com/ZeroHedgeK/python-mastery-playground/network/members)

</div>
