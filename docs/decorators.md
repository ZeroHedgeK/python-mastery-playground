# Decorators Learning Guide

## Overview

Decorators are a powerful Python feature that allows you to modify or enhance functions and classes without changing their source code. They follow the "open/closed principle" - open for extension, closed for modification.

## Core Concepts & Examples

This repository covers the following decorator patterns:

1. **Timer** (`src/python_mastery/decorators/timer.py`) - Measure execution time
2. **Cache** (`src/python_mastery/decorators/cache.py`) - Cache results with TTL
3. **Retry** (`src/python_mastery/decorators/retry.py`) - Retry on failure
4. **Rate Limit** (`src/python_mastery/decorators/rate_limit.py`) - Limit call frequency

---

## 1. Timer Decorator

The simplest decorator pattern - wraps a function to measure execution time.

### Implementation

```python
import functools
import logging
import time

logger = logging.getLogger(__name__)

def timer(func):
    @functools.wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info("Function '%s' executed in %.6f seconds", func.__name__, elapsed)
        return result
    return wrapper
```

### Usage

```python
@timer
def process_data(data):
    # ... expensive operation ...
    return result
```

### Key Takeaways

- `@functools.wraps(func)` preserves the original function's `__name__`, `__doc__`, etc.
- `time.perf_counter()` is preferred over `time.time()` for benchmarking
- Use logging instead of print for production code

---

## 2. Cache Decorator (with TTL)

Caches function results with time-based expiration.

### Implementation

```python
def cache(ttl: float = 300.0):
    def decorator(func):
        cache_store = {}  # Closure variable

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            current_time = time.time()

            if key in cache_store:
                result, timestamp = cache_store[key]
                if current_time - timestamp < ttl:
                    return result  # Cache hit
                del cache_store[key]  # Expired

            result = func(*args, **kwargs)
            cache_store[key] = (result, current_time)
            return result

        return wrapper
    return decorator
```

### Usage

```python
@cache(ttl=60.0)  # Cache for 60 seconds
def fetch_user(user_id: int) -> dict:
    return database.query(user_id)
```

### When to Use

- Expensive computations (e.g., complex calculations)
- External API calls (reduce rate limiting issues)
- Database queries (reduce load)

### Considerations

- Memory usage grows with unique argument combinations
- Not thread-safe by default (consider `functools.lru_cache` for production)
- For production, consider Redis-based caching

---

## 3. Retry Decorator

Automatically retries failed functions with configurable backoff.

### Implementation

```python
def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    logger.warning("Attempt %d failed: %s", attempt, e)
                    time.sleep(delay)
        return wrapper
    return decorator
```

### Usage

```python
@retry(max_attempts=3, delay=2.0, exceptions=(ConnectionError, TimeoutError))
def call_external_api():
    return requests.get("https://api.example.com/data")
```

### Best Practices

- Only catch specific, recoverable exceptions
- Use exponential backoff for production: `delay * (2 ** attempt)`
- Set reasonable max_attempts to avoid infinite loops
- Log each retry for debugging

---

## 4. Rate Limit Decorator

Limits how often a function can be called within a time window.

### Implementation

```python
def rate_limit(calls: int = 5, period: float = 60.0):
    lock = threading.Lock()
    call_times = []

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_times

            with lock:
                now = time.time()
                call_times = [t for t in call_times if now - t < period]

                if len(call_times) >= calls:
                    raise RuntimeError(f"Rate limit exceeded: {calls} calls per {period}s")

                call_times.append(now)

            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Usage

```python
@rate_limit(calls=10, period=60.0)  # Max 10 calls per minute
def send_notification(user_id: int, message: str):
    notification_service.send(user_id, message)
```

### Use Cases

- Preventing API abuse
- Protecting external service quotas
- Implementing fair usage policies

---

## Decorator Patterns Summary

| Decorator          | Purpose                | Parameters                            |
| ------------------ | ---------------------- | ------------------------------------- |
| `@timer`           | Measure execution time | None                                  |
| `@cache(ttl=N)`    | Cache results          | `ttl`: seconds                        |
| `@retry(...)`      | Retry on failure       | `max_attempts`, `delay`, `exceptions` |
| `@rate_limit(...)` | Limit call frequency   | `calls`, `period`                     |

---

## Running Examples

```bash
# Run individual decorator examples
python examples/timer.py
python examples/cache.py
python examples/rate_limit.py

# Run tests
pytest tests/test_decorators.py -v
```

---

## Best Practices

1. **Always use `@functools.wraps`** to preserve function metadata
2. **Use logging** instead of print statements
3. **Handle edge cases** (empty args, None values)
4. **Make decorators configurable** with sensible defaults
5. **Consider thread safety** when using shared state
6. **Document the decorator's behavior** clearly
