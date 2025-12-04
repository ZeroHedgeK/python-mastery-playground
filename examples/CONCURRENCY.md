# Concurrency Examples

## Overview
Demonstrates when to use threads, processes, or asyncio. Covers the GIL, race conditions, CPU vs I/O workloads, and graceful shutdown patterns.

## Prerequisites
- [ ] Python threading basics and async/await syntax
- [ ] Python docs: [asyncio](https://docs.python.org/3/library/asyncio.html), [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `conc_threading.py` | I/O vs CPU with GIL, locks, events, daemon threads | ⭐⭐ | 25-35 min |
| `conc_multiprocessing.py` | CPU-bound speedups, IPC via Queue/Value, pickling pitfalls | ⭐⭐ | 25-35 min |
| `conc_asyncio_basics.py` | gather, create_task, as_completed, forgetting await | ⭐⭐ | 25-35 min |
| `conc_asyncio_patterns.py` | timeouts, shield, semaphores, graceful shutdown | ⭐⭐⭐ | 45-60 min |

## Study Order

> **Reasoning:** Pick the right model (threads vs processes vs asyncio) before advanced patterns.

1. **Start here:** `conc_threading.py`
   - *Goal:* See GIL limits and race conditions.
   - *Key insight:* Threads help I/O, not CPU; locks fix races.

2. **Then:** `conc_multiprocessing.py`
   - *Goal:* Bypass GIL for CPU-bound tasks.
   - *Key insight:* Pickleability and `if __name__ == "__main__"` matter.

3. **Then:** `conc_asyncio_basics.py`
   - *Goal:* Non-blocking I/O with gather/tasks.
   - *Key insight:* Forgetting `await` yields coroutines, not results.

4. **Advanced:** `conc_asyncio_patterns.py`
   - *Goal:* Harden async code with timeouts, shields, semaphores, cancellation.
   - *Key insight:* Graceful shutdown cancels tasks and awaits their completion.

## Key Concepts

### Concept 1: GIL Proof
**Where:** `conc_threading.py`, lines ~30-90
**What to notice:** CPU tasks see no speedup with threads; demonstrates GIL constraints.

### Concept 2: Pickling Gotchas
**Where:** `conc_multiprocessing.py`, lines ~40-90
**What to notice:** Lambdas/closures fail in process pools; need top-level callables.

### Concept 3: Timeout & Shield
**Where:** `conc_asyncio_patterns.py`, lines ~10-80
**What to notice:** `wait_for` enforces deadlines; `shield` keeps critical sections alive.

## Common Mistakes

### Mistake 1: Awaiting in Sync Context
**Symptom:** `RuntimeWarning: coroutine was never awaited`.
**Fix:** Use `asyncio.run` entrypoints; ensure `await` on coroutines.

### Mistake 2: No Main Guard with multiprocessing
**Symptom:** Recursive process spawning on Windows.
**Fix:** Wrap execution in `if __name__ == "__main__"` as shown in `conc_multiprocessing.py`.

## Exercises

- [ ] **Exercise 1 (⭐):** Implement `parallel_map` with ThreadPoolExecutor preserving order.
- [ ] **Exercise 2 (⭐⭐):** Build an async rate limiter using `asyncio.Semaphore` and measure max concurrency.
- [ ] **Exercise 3 (⭐⭐⭐):** Create a producer-consumer pipeline with `asyncio.Queue` and graceful cancellation.

## Connections

| Related Module | Connection |
|----------------|------------|
| [Decorators](DECORATORS.md) | Thread-safe decorators need locking to avoid races |
| [Internals](INTERNALS.md) | GIL behavior and bytecode execution explain threading limits |
| [Functional](FUNCTIONAL.md) | Async/iter pipelines mirror generator pipelines |

## External Resources
- [Python Docs: asyncio](https://docs.python.org/3/library/asyncio.html) — Event loop APIs
- [Python Docs: concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) — Thread/Process pools
- [Real Python: AsyncIO](https://realpython.com/async-io-python/) — Practical async patterns

---
*Estimated total time: ~3 hours | Last updated: 2025-12-04*
