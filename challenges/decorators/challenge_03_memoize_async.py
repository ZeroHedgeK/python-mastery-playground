"""
Challenge: memoize_async
Difficulty: ⭐⭐⭐
Time Estimate: 20-25 minutes
Concepts: async functions, decorators, caching, asyncio

Problem:
Implement an async-aware memoization decorator `memoize_async` that caches results
of async functions based on their arguments. Subsequent awaits with the same
arguments should return the cached result without re-running the coroutine.

Requirements:
1. Cache by (args, tuple(sorted(kwargs.items()))).
2. Ensure only one underlying call runs when multiple awaits for the same key happen concurrently.
3. Preserve function metadata with functools.wraps.

Hints:
- Store asyncio.Tasks in the cache to share in-flight work.
- Use asyncio.iscoroutinefunction to validate input.

Run tests:
    python challenges/decorators/challenge_03_memoize_async.py
"""

from __future__ import annotations

import asyncio
from functools import wraps


# === YOUR CODE HERE ===


def memoize_async(fn):
    if not asyncio.iscoroutinefunction(fn):
        raise TypeError("memoize_async can only wrap async functions")

    cache = {}

    @wraps(fn)
    async def wrapper(*args, **kwargs):
        raise NotImplementedError("Your implementation here")

    return wrapper


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


async def _slow(x):
    await asyncio.sleep(0.05)
    return x * 2


async def test_caches_result():
    calls = {"count": 0}

    @memoize_async
    async def twice(x):
        calls["count"] += 1
        return await _slow(x)

    first = await twice(3)
    second = await twice(3)
    assert first == 6
    assert second == 6
    assert calls["count"] == 1


async def test_shared_inflight():
    calls = {"count": 0}

    @memoize_async
    async def slow_id(x):
        calls["count"] += 1
        await asyncio.sleep(0.05)
        return x

    results = await asyncio.gather(*(slow_id(5) for _ in range(3)))
    assert results == [5, 5, 5]
    assert calls["count"] == 1


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


if __name__ == "__main__":
    import sys

    try:
        _run(test_caches_result())
        print("✅ test_caches_result passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_caches_result failed: {e}")
        sys.exit(1)

    try:
        _run(test_shared_inflight())
        print("✅ test_shared_inflight passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_shared_inflight failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
