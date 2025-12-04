"""
Solution: memoize_async

Key Insights:
1. Caching the asyncio.Task lets concurrent callers await the same in-flight work.
2. The cache key must be deterministic; sorting kwargs ensures hashable order.
3. wraps preserves metadata; raising on non-async input prevents silent misuse.

Alternative Approaches:
- Cache raw results instead of tasks but add a lock to prevent duplicate work.
- Add TTL eviction if staleness matters.
"""

from __future__ import annotations

import asyncio
from functools import wraps
from typing import Any, Callable, Dict, Tuple


# === SOLUTION ===


def memoize_async(fn: Callable):
    if not asyncio.iscoroutinefunction(fn):
        raise TypeError("memoize_async can only wrap async functions")

    cache: Dict[Tuple[Any, ...], asyncio.Task] = {}

    @wraps(fn)
    async def wrapper(*args: Any, **kwargs: Any):
        key = args + (tuple(sorted(kwargs.items())),)
        task = cache.get(key)
        if task is None or task.done() and task.cancelled():
            task = asyncio.create_task(fn(*args, **kwargs))
            cache[key] = task
        return await task

    return wrapper


# === VERIFICATION ===


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
    _run(test_caches_result())
    print("✅ test_caches_result passed")
    _run(test_shared_inflight())
    print("✅ test_shared_inflight passed")
    print("\n🎉 All tests passed!")
