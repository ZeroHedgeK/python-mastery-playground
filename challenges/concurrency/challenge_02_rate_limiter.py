"""
Challenge: rate_limiter
Difficulty: ⭐⭐
Time Estimate: 20 minutes
Concepts: asyncio, semaphore, rate limiting

Problem:
Implement an async context manager `rate_limiter(max_concurrent)` that provides
an acquire() coroutine to limit concurrent operations. Using it should allow at
most max_concurrent tasks to run at once.

Requirements:
1. Use asyncio.Semaphore under the hood.
2. rate_limiter should be usable with `async with limiter.acquire(): ...`.
3. Ensure semaphore is released even if block raises.

Hints:
- Define an inner async contextmanager using asynccontextmanager.

Run tests:
    python challenges/concurrency/challenge_02_rate_limiter.py
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager


# === YOUR CODE HERE ===


class rate_limiter:
    def __init__(self, max_concurrent: int):
        raise NotImplementedError("Your implementation here")

    @asynccontextmanager
    async def acquire(self):
        raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


async def test_limits_concurrency():
    limiter = rate_limiter(2)
    running = 0
    max_seen = 0

    async def worker():
        nonlocal running, max_seen
        async with limiter.acquire():
            running += 1
            max_seen = max(max_seen, running)
            await asyncio.sleep(0.02)
            running -= 1

    await asyncio.gather(*(worker() for _ in range(5)))
    assert max_seen <= 2


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


if __name__ == "__main__":
    import sys

    try:
        _run(test_limits_concurrency())
        print("✅ test_limits_concurrency passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_limits_concurrency failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
