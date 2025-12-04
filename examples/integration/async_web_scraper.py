"""
Async web scraper integration: asyncio + context managers + decorators (retry, rate
limit) working together for resilient concurrent fetching.

Why this combination: asyncio provides concurrency for many I/O-bound fetches,
decorators add resilience (retry + throttling), and context managers guarantee
resource cleanup (session lifecycle + timing) even on failure.
"""

from __future__ import annotations

import asyncio
import random
import time
from typing import Iterable

# [ASYNCIO] reference import to align with library patterns
from python_mastery.concurrency import (  # noqa: F401
    asyncio_patterns as _async_reference,
)

# [CONTEXT MANAGER] AsyncTimer wraps async blocks for lifecycle and timing
from python_mastery.context_managers import AsyncTimer

# [DECORATOR] retry/rate_limit layer resilience and throttling
from python_mastery.decorators import rate_limit, retry


class FakeSession:
    """
    Minimal async session to demonstrate proper setup/teardown.
    """

    def __init__(self) -> None:
        self.closed = False

    async def __aenter__(self):  # [CONTEXT MANAGER]
        print("  [session] opening connection pool")
        return self

    async def __aexit__(self, exc_type, exc, tb):  # [CONTEXT MANAGER]
        self.closed = True
        print("  [session] closing connection pool (closed=%s)" % self.closed)


# [DECORATOR] Throttle + retry sync work executed in threads
@rate_limit(calls=3, period=0.5)
@retry(max_attempts=3, delay=0.05)
def fetch_sync(session: FakeSession, url: str) -> str:
    """Simulated HTTP GET with flaky failures."""

    # Introduce a small random failure to exercise retry
    if random.random() < 0.3:
        raise RuntimeError(f"transient error on {url}")

    time.sleep(0.05)  # simulate network latency
    return f"body-for-{url}"


async def fetch_with_semaphore(
    session: FakeSession, url: str, sem: asyncio.Semaphore
) -> str:
    # [ASYNCIO] semaphore bounds concurrency; [CONTEXT MANAGER] AsyncTimer measures block
    async with sem:
        async with AsyncTimer(f"fetch {url}"):
            # offload decorated sync work to a thread; decorators still apply
            return await asyncio.to_thread(fetch_sync, session, url)


async def naive_scrape(urls: Iterable[str]) -> None:
    """
    Failure-first version: no throttling, no retry, no cleanup guard.
    Expect: random failures bubble, noisy unhandled errors.
    """

    print("\n[naive] starting without semaphore/retry")

    async def unprotected_fetch(url: str) -> str:
        # No retry/rate_limit: simulate immediate failure
        if random.random() < 0.5:
            raise RuntimeError(f"naive failure on {url}")
        await asyncio.sleep(0.02)
        return f"raw-{url}"

    try:
        results = await asyncio.gather(*(unprotected_fetch(u) for u in urls))
        print("[naive] results:", results)
    except Exception as exc:  # [ERROR HANDLING]
        print("[naive] blew up:", exc)


async def composed_scrape(urls: Iterable[str]) -> None:
    """Full solution: context-managed session + throttled, retried fetches."""

    print("\n[composed] starting with retry + rate limit + context mgmt")
    async with FakeSession() as session:  # [CONTEXT MANAGER]
        sem = asyncio.Semaphore(2)
        results = await asyncio.gather(
            *(fetch_with_semaphore(session, u, sem) for u in urls)
        )
        print("[composed] fetched bodies:", results)


def explain_synergy() -> None:
    print("\nWhy this combination matters:")
    print(
        "  • asyncio handles many URLs concurrently without threads for I/O-bound work"
    )
    print("  • @rate_limit + @retry keep noisy endpoints stable under load")
    print("  • async context managers guarantee session cleanup and timed visibility")
    print("  • semaphore prevents runaway concurrency that would break rate limits")


def run_demo() -> None:
    urls = [f"https://example.com/{i}" for i in range(6)]
    asyncio.run(naive_scrape(urls))
    asyncio.run(composed_scrape(urls))
    explain_synergy()


if __name__ == "__main__":
    run_demo()
