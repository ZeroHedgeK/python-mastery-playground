# Examples Directory

## Purpose
Demonstration scripts that show how concepts in `python_mastery` behave in practice. Unlike `src/`, these files are runnable, verbose, and teaching-first.

## Quick Start
```bash
# Run any example
python examples/<filename>.py

# Run with verbose output (where applicable)
python examples/<filename>.py -v
```

## Learning Paths

### Path A: Core Python (recommended first)
1. [Decorators](DECORATORS.md) → 2. [Context Managers](CONTEXT_MANAGERS.md) → 3. [Data Structures](DATA_STRUCTURES.md)

### Path B: Object-Oriented Mastery
4. [OOP](OOP.md) → 5. [Testing Patterns](TESTING.md)

### Path C: Performance & Scale
6. [Concurrency](CONCURRENCY.md) → 7. [Internals](INTERNALS.md)

### Path D: Modern Python
8. [Control Flow](CONTROL_FLOW.md) → 9. [Functional](FUNCTIONAL.md)

## All Files Reference

| File | Module | Concepts | Difficulty |
|------|--------|----------|------------|
| `decorator_timer.py` | Decorators | timing decorator, `functools.wraps` | ⭐ |
| `decorator_retry.py` | Decorators | retry/backoff, exception filtering | ⭐⭐ |
| `decorator_cache.py` | Decorators | caching, TTL, key normalization | ⭐⭐ |
| `decorator_rate_limit.py` | Decorators | rate limiting, backoff signals | ⭐⭐ |
| `ctx_timer.py` | Context Managers | class vs generator contexts, exceptions | ⭐ |
| `ctx_state.py` | Context Managers | env state swap, nesting, cleanup | ⭐⭐ |
| `ctx_reentrant.py` | Context Managers | single-use vs reusable contexts | ⭐⭐ |
| `ctx_async.py` | Context Managers | async context managers, `AsyncTimer` | ⭐⭐ |
| `ds_comprehensions.py` | Data Structures | declarative vs imperative, filtering | ⭐ |
| `ds_generators.py` | Data Structures | lazy pipelines, send(), memory | ⭐⭐ |
| `ds_slicing.py` | Data Structures | slicing patterns, custom `__getitem__` | ⭐⭐ |
| `ds_collections.py` | Data Structures | Counter/defaultdict/deque, ChainMap | ⭐⭐ |
| `oop_inheritance.py` | OOP | MRO, diamond, cooperative `super()` | ⭐⭐ |
| `oop_magic_methods.py` | OOP | dunder arithmetic, container protocol | ⭐⭐ |
| `oop_advanced_classes.py` | OOP | descriptors, slots, `__init_subclass__` | ⭐⭐⭐ |
| `oop_metaclasses.py` | OOP | metaclass hooks, validation, registries | ⭐⭐⭐ |
| `conc_threading.py` | Concurrency | GIL proof, races, locks, events | ⭐⭐ |
| `conc_multiprocessing.py` | Concurrency | CPU-bound speedup, IPC, pickling | ⭐⭐ |
| `conc_asyncio_basics.py` | Concurrency | gather, tasks, as_completed | ⭐⭐ |
| `conc_asyncio_patterns.py` | Concurrency | timeouts, shield, semaphores, shutdown | ⭐⭐⭐ |
| `flow_pattern_matching.py` | Control Flow | match/case patterns, guards | ⭐⭐ |
| `flow_pipelines.py` | Control Flow | generator pipelines, yield from | ⭐⭐ |
| `flow_loops.py` | Control Flow | for/else, while/else, break/continue | ⭐ |
| `func_partial.py` | Functional | partials, compose, handler config | ⭐⭐ |
| `func_reduce.py` | Functional | reduce vs loops, folds, composition | ⭐⭐ |
| `func_itertools.py` | Functional | lazy iterators, grouping, combinatorics | ⭐⭐ |
| `func_immutability.py` | Functional | purity vs mutation, frozen dataclasses | ⭐⭐ |
| `internals_bytecode.py` | Internals | disassembly, LOAD_FAST vs GLOBAL | ⭐⭐ |
| `internals_refcount.py` | Internals | refcount +1, weakref, caching | ⭐⭐ |
| `internals_gc.py` | Internals | GC generations, cycles, callbacks | ⭐⭐ |
| `internals_memory.py` | Internals | getsizeof, slots, tracemalloc | ⭐⭐ |
| `test_fixtures.py` | Testing | pytest fixtures scope/params/async | ⭐⭐ |
| `test_mocking.py` | Testing | patch location, MagicMock, DI vs patch | ⭐⭐ |
| `test_type_safety.py` | Testing | Protocols, TypedDict, Literal | ⭐⭐ |
| `test_strategies.py` | Testing | AAA, markers, invariants | ⭐⭐ |

## Cross-Module Connections
- Decorators → Context Managers: `@contextmanager` relies on decorator patterns.
- OOP → Testing: `Protocol` interfaces enable safe fakes and mocks.
- Functional → Data Structures: generators are lazy iterators powering pipelines.
- Concurrency → Decorators: thread-safe decorators (e.g., caching) need locks.

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| `ModuleNotFoundError: python_mastery` | Package not installed | `pip install -e .` from repo root |
| `SyntaxError` on `match/case` | Python < 3.10 | Upgrade Python or skip `flow_pattern_matching.py` |
| Async examples hang | Missing `asyncio.run()` | Use the provided `if __name__ == "__main__"` entrypoints |
| Multiprocessing spawns endlessly on Windows | Missing `if __name__ == "__main__"` | Run via `python conc_multiprocessing.py` only |
