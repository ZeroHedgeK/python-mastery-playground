# Concurrency Learning Guide

## Overview

Python offers three main approaches to concurrent execution, each suited for different types of workloads:

| Approach            | Best For             | GIL Impact          | Memory   |
| ------------------- | -------------------- | ------------------- | -------- |
| **Threading**       | I/O-bound tasks      | Limited by GIL      | Shared   |
| **Multiprocessing** | CPU-bound tasks      | Bypasses GIL        | Separate |
| **AsyncIO**         | High-concurrency I/O | N/A (single thread) | Shared   |

## Core Concepts & Examples

1. **Threading** (`src/python_mastery/concurrency/threading_demo.py`)
2. **Multiprocessing** (`src/python_mastery/concurrency/multiprocessing_demo.py`)
3. **AsyncIO** (`src/python_mastery/concurrency/asyncio_demo.py`)

---

## Understanding the GIL

The **Global Interpreter Lock (GIL)** is a mutex that protects access to Python objects. Only one thread can execute Python bytecode at a time.

```
Thread 1: [====]      [====]      [====]
Thread 2:      [====]      [====]
GIL:      ^----^----^----^----^----^----^
```

**Implications**:

- CPU-bound tasks don't benefit from threading
- I/O-bound tasks do benefit (GIL is released during I/O wait)
- Use multiprocessing for true parallelism

---

## 1. Threading (I/O-Bound Tasks)

Threads are lightweight and share memory. Ideal for tasks that wait on external resources.

### Modern Approach: ThreadPoolExecutor

```python
import concurrent.futures
import time

def download_file(file_id: int) -> str:
    """Simulates downloading a file (I/O bound task)."""
    print(f"Thread-{file_id}: Starting download...")
    time.sleep(0.5)  # Simulate network latency
    print(f"Thread-{file_id}: Download complete!")
    return f"file_{file_id}.dat"

def main() -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks
        results = list(executor.map(download_file, range(5)))

    print(f"Results: {results}")

# 5 tasks * 0.5s = 2.5s sequential
# With 3 workers: ~1.0s (2 batches)
```

### When to Use Threading

- Network requests (HTTP APIs, web scraping)
- File I/O operations
- Database queries
- User input handling

### Common Patterns

```python
# Pattern 1: executor.map() for simple cases
results = list(executor.map(func, items))

# Pattern 2: executor.submit() for complex cases
futures = [executor.submit(func, item) for item in items]
for future in concurrent.futures.as_completed(futures):
    result = future.result()

# Pattern 3: With timeout
future = executor.submit(slow_function)
try:
    result = future.result(timeout=5.0)
except concurrent.futures.TimeoutError:
    print("Task timed out")
```

---

## 2. Multiprocessing (CPU-Bound Tasks)

Processes run in separate memory spaces with their own GIL. True parallelism on multi-core CPUs.

### Modern Approach: multiprocessing.Pool

```python
import multiprocessing
import os

def heavy_computation(num: int) -> int:
    """CPU-intensive task."""
    print(f"Process-{os.getpid()}: Computing factorial of {num}...")
    result = 1
    for i in range(1, num + 1):
        result *= i
    return result

def main() -> None:
    cpu_count = multiprocessing.cpu_count()
    print(f"System has {cpu_count} CPUs")

    with multiprocessing.Pool(processes=cpu_count) as pool:
        numbers = [50000, 50000, 50000, 50000]
        results = pool.map(heavy_computation, numbers)

    print(f"Results computed across {cpu_count} processes")

# 4 tasks running in parallel on 4 cores: ~1x time
# vs sequential: ~4x time
```

### When to Use Multiprocessing

- Mathematical computations
- Image/video processing
- Data transformation pipelines
- Machine learning training

### Data Sharing Between Processes

```python
from multiprocessing import Manager

def worker(shared_dict, key, value):
    shared_dict[key] = value

with Manager() as manager:
    shared_dict = manager.dict()

    p1 = multiprocessing.Process(target=worker, args=(shared_dict, "a", 1))
    p2 = multiprocessing.Process(target=worker, args=(shared_dict, "b", 2))

    p1.start(); p2.start()
    p1.join(); p2.join()

    print(dict(shared_dict))  # {"a": 1, "b": 2}
```

### Considerations

- Process creation has overhead (~0.1s per process)
- Data must be pickled/unpickled (serialization cost)
- Memory is not shared by default
- Use `if __name__ == "__main__":` guard on Windows

---

## 3. AsyncIO (High-Concurrency I/O)

AsyncIO uses cooperative multitasking with a single thread. Coroutines yield control during `await`.

### Basic Pattern

```python
import asyncio
from typing import Any

async def fetch_data(source_id: int) -> dict[str, Any]:
    """A coroutine that simulates fetching data."""
    print(f"Task-{source_id}: Sending request...")
    await asyncio.sleep(0.5)  # Yields control to event loop
    print(f"Task-{source_id}: Data received!")
    return {"id": source_id, "data": "chunk"}

async def main() -> None:
    # Create 10 concurrent tasks
    tasks = [fetch_data(i) for i in range(10)]

    # Run all concurrently
    results = await asyncio.gather(*tasks)

    print(f"Fetched {len(results)} items")

# 10 * 0.5s = 5.0s sequential
# AsyncIO: ~0.5s total (all wait in parallel)

asyncio.run(main())
```

### Key Concepts

```python
# async def - defines a coroutine
async def my_coroutine():
    pass

# await - yields control, waits for result
result = await some_async_function()

# asyncio.gather - run multiple coroutines concurrently
results = await asyncio.gather(coro1(), coro2(), coro3())

# asyncio.create_task - schedule without waiting
task = asyncio.create_task(some_coroutine())
# ... do other work ...
result = await task
```

### When to Use AsyncIO

- Web servers (FastAPI, aiohttp)
- API clients making many requests
- WebSocket connections
- Database drivers (asyncpg, motor)

### Common Patterns

```python
# Pattern 1: Concurrent requests with gather
async def fetch_all(urls: list[str]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Pattern 2: Rate-limited requests
semaphore = asyncio.Semaphore(10)  # Max 10 concurrent

async def fetch_with_limit(url: str) -> dict:
    async with semaphore:
        return await fetch_url(url)

# Pattern 3: Timeout handling
try:
    result = await asyncio.wait_for(slow_operation(), timeout=5.0)
except asyncio.TimeoutError:
    print("Operation timed out")
```

---

## Choosing the Right Approach

```
                    ┌─────────────────┐
                    │   What type     │
                    │   of workload?  │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     ┌──────────┐     ┌──────────┐     ┌──────────┐
     │ CPU-bound │     │ I/O-bound│     │ I/O-bound│
     │ (compute) │     │  (few)   │     │  (many)  │
     └─────┬─────┘     └─────┬────┘     └─────┬────┘
           │                 │                 │
           ▼                 ▼                 ▼
    ┌─────────────┐   ┌──────────┐     ┌───────────┐
    │Multiprocess-│   │ Threading│     │  AsyncIO  │
    │    ing      │   │          │     │           │
    └─────────────┘   └──────────┘     └───────────┘
```

### Decision Matrix

| Scenario                   | Recommendation  |
| -------------------------- | --------------- |
| Download 5 files           | Threading       |
| Download 1000 files        | AsyncIO         |
| Process 100 images         | Multiprocessing |
| Web scraping               | AsyncIO         |
| Number crunching           | Multiprocessing |
| Database queries (few)     | Threading       |
| Database queries (many)    | AsyncIO         |
| Real-time WebSocket server | AsyncIO         |

---

## Running Examples

```bash
# Run individual demonstrations
python -m python_mastery.concurrency.threading_demo
python -m python_mastery.concurrency.multiprocessing_demo
python -m python_mastery.concurrency.asyncio_demo

# Or use the interactive CLI
python -m python_mastery
# Select: 4. Concurrency
```

---

## Best Practices

1. **Start simple** - Use threading before considering multiprocessing
2. **Use executors** - `ThreadPoolExecutor` and `Pool` are safer than raw threads/processes
3. **Limit concurrency** - Too many workers can overwhelm resources
4. **Handle exceptions** - Concurrent code needs robust error handling
5. **Test thoroughly** - Race conditions are hard to debug
6. **Prefer AsyncIO** for new high-concurrency I/O projects
7. **Use `if __name__ == "__main__":`** guard for multiprocessing on Windows
