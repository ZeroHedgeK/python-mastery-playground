# Context Managers Examples

## Overview
Context managers ensure setup/teardown correctness, even on exceptions. These examples show class-based `__enter__/__exit__`, generator-based `@contextmanager`, and async variants for reliable resource handling.

## Prerequisites
- [ ] Familiar with `with` statement semantics
- [ ] Python docs: [contextlib](https://docs.python.org/3/library/contextlib.html)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `ctx_timer.py` | Timing contexts, class vs generator, exception propagation | ⭐ | 15-20 min |
| `ctx_state.py` | Temporary env overrides, nesting, cleanup on errors | ⭐⭐ | 25-35 min |
| `ctx_reentrant.py` | Single-use vs reusable contexts, reuse errors | ⭐⭐ | 25-35 min |
| `ctx_async.py` | Async context managers, timing concurrent tasks | ⭐⭐ | 25-35 min |

## Study Order

> **Reasoning:** Move from sync basics to reuse rules, then async contexts.

1. **Start here:** `ctx_timer.py`
   - *Goal:* Understand entry/exit guarantees and exception flow.
   - *Key insight:* `__exit__` runs even when exceptions occur.

2. **Then:** `ctx_state.py`
   - *Goal:* Manage external state safely (env vars) with nesting.
   - *Key insight:* Always restore previous state; use try/finally.

3. **Then:** `ctx_reentrant.py`
   - *Goal:* Differentiate single-use vs reusable contexts.
   - *Key insight:* Guard reuse to prevent double-entry bugs.

4. **Advanced:** `ctx_async.py`
   - *Goal:* Apply context semantics to async tasks with `async with`.
   - *Key insight:* Async managers must implement `__aenter__/__aexit__`.

## Key Concepts

### Concept 1: Exception Safety
**Where:** `ctx_timer.py`, lines ~30-80

**Pattern:**
```python
class Timer:
    def __exit__(self, exc_type, exc, tb):
        # still records time, returns False to propagate
        return False
```

**What to notice:** Returning False lets exceptions bubble while still running cleanup.

**Try this:** Raise inside the block; confirm timing still prints.

### Concept 2: Reentrancy Guards
**Where:** `ctx_reentrant.py`, lines ~10-60

**What to notice:** Single-use contexts raise on second entry; reusable tracks counts.

**Try this:** Reuse `SingleUse()` in two `with` blocks and observe the guard.

### Concept 3: Async Contexts
**Where:** `ctx_async.py`, lines ~10-60

**What to notice:** `async with AsyncTimer()` wraps awaited work; timing stays accurate across awaits.

**Try this:** Add another awaited task inside to see concurrent timing.

## Common Mistakes

### Mistake 1: Forgetting Cleanup on Exception
**Symptom:** Env vars or files left modified after failure.
**Fix:** Use try/finally in `__exit__` or generator wrappers (`ctx_state.py`).

### Mistake 2: Reusing Single-Use Contexts
**Symptom:** State corruption or silent reuse; fix by guarding as in `ctx_reentrant.py`.

## Exercises

- [ ] **Exercise 1 (⭐):** Implement `temp_directory` context that deletes on exit. Verify with file creation inside the block.
- [ ] **Exercise 2 (⭐⭐):** Build `redirect_stdout` context manually swapping `sys.stdout`; ensure restoration on exceptions.
- [ ] **Exercise 3 (⭐⭐⭐):** Write an async context that limits concurrent tasks with a semaphore and measures duration.

## Connections

| Related Module | Connection |
|----------------|------------|
| [Decorators](DECORATORS.md) | `@contextmanager` is a decorator wrapping generator-based contexts |
| [Concurrency](CONCURRENCY.md) | Async context managers coordinate coroutines safely |
| [Testing](TESTING.md) | Fixtures often use context managers for setup/teardown |

## External Resources
- [PEP 343](https://peps.python.org/pep-0343/) — The `with` statement
- [Python Docs: contextlib](https://docs.python.org/3/library/contextlib.html) — `@contextmanager`, `ExitStack`
- [Real Python: Context Managers](https://realpython.com/python-with-statement/) — Practical patterns

---
*Estimated total time: ~2 hours | Last updated: 2025-12-04*
