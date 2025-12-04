"""
Solution: rate_limiter

Key Insights:
1. asyncio.Semaphore gates concurrency; asynccontextmanager simplifies acquire/release.
2. Using `async with` on the limiter.acquire() ensures release on exceptions.
3. Keep semaphore per limiter instance to isolate limits.

Alternative Approaches:
- Provide __aenter__/__aexit__ directly; this design exposes an acquire helper.
"""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager


# === SOLUTION ===


class rate_limiter:
    def __init__(self, max_concurrent: int):
        self._sem = asyncio.Semaphore(max_concurrent)

    @asynccontextmanager
    async def acquire(self):
        await self._sem.acquire()
        try:
            yield
        finally:
            self._sem.release()


# === VERIFICATION ===


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
    _run(test_limits_concurrency())
    print("✅ test_limits_concurrency passed")
    print("\n🎉 All tests passed!")
