# Context Managers Learning Guide

## Overview

Context managers provide a clean way to manage resources and handle setup/cleanup operations automatically. They are typically used with the `with` statement and ensure that resources are properly released even if errors occur.

## Core Concepts & Examples

This repository covers the following fundamental topics:

1.  **Basic Implementation**: Class-based vs Generator-based (`timer.py`)
2.  **Standard Utilities**: Built-in tools in `contextlib` (`utilities.py`)
3.  **Async Contexts**: Using `async with` (`async_ctx.py`)
4.  **State Management**: Managing global state safely (`state.py`)
5.  **Reusability**: Single-use vs Reentrant context managers (`reentrant.py`)

### 1. Two Approaches to Creating Context Managers

#### A. Class-Based Approach (`__enter__`/`__exit__`)

**Implementation:**

```python
class Timer:
    def __init__(self, name=None):
        self.name = name
        self.start_time = None
        self.elapsed = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self  # Return self to allow access to attributes

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
        print(f"Timer: {self.elapsed:.4f} seconds")
        return False  # Propagate exceptions
```

**When to Use:** Complex resource management, state maintenance, need for access during execution.

#### B. `@contextmanager` Decorator Approach

**Implementation:**

```python
@contextmanager
def timer_context(name=None):
    start_time = time.perf_counter()
    try:
        yield  # Yield control to the code block
    finally:
        elapsed = time.perf_counter() - start_time
        print(f"Timer: {elapsed:.4f} seconds")
```

**When to Use:** Simple setup/cleanup, quick scripting, no need for complex state.

### 2. Essential `contextlib` Utilities (`utilities.py`)

Python's standard library provides powerful tools that you should know before writing your own:

- **`suppress(FileNotFoundError)`**: Cleaner than `try/except pass`.
- **`closing(thing)`**: Wraps objects that have `.close()` but no context manager support.
- **`nullcontext()`**: A no-op context manager, perfect for conditional contexts.
- **`ExitStack()`**: The "Swiss Army Knife". Allows you to enter a dynamic number of contexts (e.g., opening a list of 10 files).

### 3. Async Context Managers (`async_ctx.py`)

For modern async applications (FastAPI, asyncio), you use `__aenter__` and `__aexit__`:

```python
class AsyncConnection:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
```

Usage:

```python
async with AsyncConnection() as conn:
    await conn.query()
```

### 4. State Management (`state.py`)

A common pattern for testing or temporary configuration changes. Sets a value on enter, and restores the _original_ value on exit (even if it was None).

### 5. Reentrancy (`reentrant.py`)

- **Single-use**: Standard file objects or network connections. Can only be used in one `with` block.
- **Reentrant**: Can be reused or nested (e.g., locks, database transaction pools).

## Running the Examples

Run the individual modules to see the concepts in action:

```bash
# 1. Basic Timer (Class vs Decorator)
python context_managers/timer.py

# 2. Standard Library Utilities
python context_managers/utilities.py

# 3. Async Context Managers
python context_managers/async_ctx.py

# 4. State Management (Environment Variables)
python context_managers/state.py

# 5. Reusability Demonstration
python context_managers/reentrant.py
```

## Best Practices

1.  **Prefer `contextlib` tools** (like `suppress`) over writing custom logic.
2.  **Use `ExitStack`** when you don't know how many resources you need to manage until runtime.
3.  **Always use `try/finally`** in generator-based context managers to guarantee cleanup.
4.  **Be explicit about exception handling**. If you return `True` from `__exit__`, you are swallowing the exception. Document this clearly.
