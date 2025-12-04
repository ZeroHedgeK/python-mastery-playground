# Decorators Examples

## Overview
Decorators show how to wrap behavior (timing, retry, caching, rate limiting) while preserving function contracts. These patterns matter in production for observability, resilience, and performance without altering call sites.

## Prerequisites
- [ ] Comfortable with first-class functions and closures
- [ ] Python docs: [functools.wraps](https://docs.python.org/3/library/functools.html#functools.wraps)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `decorator_timer.py` | Timing decorator that preserves return values and metadata | ⭐ | 15-20 min |
| `decorator_retry.py` | Backoff, exception filtering, and max-attempt control | ⭐⭐ | 25-35 min |
| `decorator_cache.py` | TTL cache, stable keys for mutable args | ⭐⭐ | 25-35 min |
| `decorator_rate_limit.py` | Token-bucket style limiter with error signaling | ⭐⭐ | 25-35 min |

## Study Order

> **Reasoning:** Build from simple wrapping to resilience and performance.

1. **Start here:** `decorator_timer.py`
   - *Goal:* Understand `@wraps` and transparent timing.
   - *Key insight:* Wrapping must not swallow return values.

2. **Then:** `decorator_retry.py`
   - *Goal:* Add controlled retries with delays and exception filters.
   - *Key insight:* Backoff and exception tuples prevent runaway retries.

3. **Then:** `decorator_cache.py`
   - *Goal:* Normalize keys and handle TTL expiry.
   - *Key insight:* Stable keys require sorting kwargs and copying mutables.

4. **Advanced:** `decorator_rate_limit.py`
   - *Goal:* Enforce call budgets with clear signals.
   - *Key insight:* Separate limiters per function to avoid shared state races.

## Key Concepts

### Concept 1: Preserving Metadata
**Where:** `decorator_timer.py`, lines ~1-40

**Pattern:**
```python
def decorator(fn):
    @wraps(fn)
    def wrapper(*a, **kw):
        return fn(*a, **kw)
    return wrapper
```

**What to notice:** Without `@wraps`, `__name__` and `__doc__` break; tooling and tests fail.

**Try this:** Remove `@wraps` and run; doctests and log messages will show the wrong function name.

### Concept 2: Retry with Filters
**Where:** `decorator_retry.py`, lines ~10-80

**What to notice:** Only retry on specific exception types; backoff doubles delay to avoid hammering services.

**Try this:** Change the exceptions tuple to include `ValueError` and observe broader retry behavior.

### Concept 3: Stable Cache Keys
**Where:** `decorator_cache.py`, lines ~40-120

**What to notice:** Sorting kwargs and copying mutable inputs prevents cache misses caused by ordering.

**Try this:** Pass kwargs in different orders and see cache hits remain stable.

## Common Mistakes

### Mistake 1: Missing `@wraps`
**Symptom:** Introspection shows `wrapper` name; tests relying on `__name__` fail.

**Wrong:**
```python
def deco(fn):
    def wrapper(*a, **k):
        return fn(*a, **k)
    return wrapper
```

**Right:** Use `@wraps(fn)` as shown in `decorator_timer.py`.

### Mistake 2: Caching Mutable Inputs by Reference
**Symptom:** Mutating a list after call corrupts cached result.

**Right:** Copy or normalize inputs before keying, as in `decorator_cache.py`.

## Exercises

- [ ] **Exercise 1 (⭐):** Write `@log_calls` that prints name/args/kwargs before calling. Verify by running on a simple add function.
- [ ] **Exercise 2 (⭐⭐):** Build `@validate_types` that raises `TypeError` when args don't match expected types. Hint: use `inspect.signature` like `decorator_retry.py` uses exception filtering logic.
- [ ] **Exercise 3 (⭐⭐⭐):** Create a thread-safe `@memoize` that normalizes kwargs and supports TTL. Verify by calling from multiple threads and ensuring no duplicate work.

## Connections

| Related Module | Connection |
|----------------|------------|
| [Context Managers](CONTEXT_MANAGERS.md) | `@contextmanager` uses decorator mechanics and generator cleanup |
| [Concurrency](CONCURRENCY.md) | Decorating thread/async functions requires careful locking/awaiting |
| [Testing](TESTING.md) | `@wraps` keeps test double verification accurate |

## External Resources
- [PEP 318](https://peps.python.org/pep-0318/) — Decorators for functions and methods
- [Python Docs: functools](https://docs.python.org/3/library/functools.html) — `wraps`, `lru_cache`
- [Real Python: Python Decorators](https://realpython.com/primer-on-python-decorators/) — Practical patterns

---
*Estimated total time: ~2 hours | Last updated: 2025-12-04*
