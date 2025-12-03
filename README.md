# Python Mastery Playground

A comprehensive, hands-on repository for mastering "everything" about Python. This project is structured as a series of modules, each covering a fundamental or advanced topic with implementation code, examples, and tests.

## 🗺️ Roadmap & Progress

See [ROADMAP.md](ROADMAP.md) for detailed learning objectives.

| Module | Status | Description |
|--------|--------|-------------|
| **1. Advanced Patterns** | ✅ Done | Decorators, Context Managers, Closures |
| **2. Data Structures** | ✅ Done | Comprehensions, Generators, `collections` |
| **3. OOP** | ✅ Done | Metaclasses, MRO, Magic Methods, Slots |
| **4. Concurrency** | ✅ Done | AsyncIO, Multiprocessing, Threading |
| **5. Testing & Quality** | ✅ Done | Pytest Fixtures, Mocking, Type Safety |
| **6. Functional** | ✅ Done | Partial, Reduce, Immutability, Recursion |
| **7. Internals** | ✅ Done | Bytecode Disassembly, Memory Management, GC |

## 🚀 How to Use

### 1. Interactive Demos
Run specific modules to see concepts in action:

```bash
# Module 1: Decorators
python examples/timer.py

# Module 2: Data Structures
python datastructures/builtins.py

# Module 3: OOP (Metaclasses)
python oop/metaclasses.py

# Module 4: Concurrency (AsyncIO)
python concurrency/asyncio_demo.py

# Module 7: Internals (Bytecode)
python internals/bytecode_inspector.py
```

### 2. Running Tests
We have a comprehensive test suite covering all modules.
```bash
# Run all tests
pytest tests/

# Run specific module tests
pytest tests/test_concurrency.py
```

## 🔧 Requirements
- Python 3.10+
- No external runtime dependencies (uses standard library)
- Dev dependencies: `pytest`, `pytest-asyncio`, `mypy`, `black`, `flake8`

## 📄 License
Educational purposes. MIT License.
