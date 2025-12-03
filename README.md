# Python Mastery Playground

A comprehensive, hands-on repository for mastering "everything" about Python. This project is structured as a series of modules, each covering a fundamental or advanced topic with implementation code, examples, and tests.

## 🗺️ Roadmap

See [ROADMAP.md](ROADMAP.md) for the full learning path.

## 📚 Current Modules

### 1. Decorators (`decorators/`)

- **Concepts**: Closures, `functools.wraps`, Higher-order functions.
- **Implementations**: `@timer`, `@retry`, `@rate_limit`, `@cache`.

### 2. Context Managers (`context_managers/`)

- **Concepts**: `with` statement, `__enter__`/`__exit__`, `contextlib`.
- **Implementations**: Timer context, Async context, State management, Reentrancy.

## 🚀 How to Use

### Interactive Menu

Run the main script to see available examples:

```bash
python main.py
```

### Running Specific Examples

```bash
# Decorators
python examples/timer.py
python examples/retry.py

# Context Managers
python context_managers/utilities.py
python context_managers/async_ctx.py
```

### Running Tests

```bash
pytest tests/
```

## 🔧 Requirements

- Python 3.10+
- No external dependencies (uses standard library for core modules)

## 📄 License

Educational purposes. MIT License.
