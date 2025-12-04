"""AsyncIO patterns: cancellation, timeouts, bounded concurrency, and retries."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from concurrent.futures import ThreadPoolExecutor
from typing import Any


async def timeout_example(delay: float, timeout: float) -> bool:
    """Return False when the delay exceeds the timeout, True otherwise."""

    try:
        await asyncio.wait_for(asyncio.sleep(delay), timeout=timeout)
    except asyncio.TimeoutError:
        return False
    return True


async def bounded_gather(
    work_items: Sequence[tuple[int, float]],
    max_concurrent: int,
) -> tuple[list[int], int]:
    """Process work items with a semaphore and track peak concurrency.

    Each work item is a tuple of (value, delay). The result list preserves input
    order while the peak concurrency reports the maximum number of simultaneous
    active tasks observed.
    """

    semaphore = asyncio.Semaphore(max_concurrent)
    in_flight = 0
    peak = 0
    lock = asyncio.Lock()

    async def worker(value: int, delay: float) -> int:
        nonlocal in_flight, peak
        async with semaphore:
            async with lock:
                in_flight += 1
                peak = max(peak, in_flight)
            try:
                await asyncio.sleep(delay)
                return value * 2
            finally:
                async with lock:
                    in_flight -= 1

    tasks = [worker(value, delay) for value, delay in work_items]
    results = await asyncio.gather(*tasks)
    return results, peak


async def stream_chunks(data: str, chunk_size: int) -> AsyncIterator[str]:
    """Async generator that yields string chunks."""

    for idx in range(0, len(data), chunk_size):
        await asyncio.sleep(0)  # allow cooperative scheduling
        yield data[idx : idx + chunk_size]


async def run_blocking(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Bridge blocking code using run_in_executor."""

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=1) as executor:
        return await loop.run_in_executor(executor, lambda: func(*args, **kwargs))


async def retry_async(
    op: Callable[[], Awaitable[Any]],
    retries: int = 3,
    base_delay: float = 0.01,
) -> Any:
    """Retry an async callable with exponential backoff."""

    attempt = 0
    delay = base_delay
    while True:
        try:
            return await op()
        except Exception:  # noqa: BLE001 - demo code, intentionally broad
            attempt += 1
            if attempt > retries:
                raise
            await asyncio.sleep(delay)
            delay *= 2


def demonstrate_async_patterns() -> None:
    """Showcase multiple asyncio patterns in one run."""

    async def _demo() -> None:
        print("\n=== AsyncIO Patterns ===")

        ok = await timeout_example(0.05, timeout=0.1)
        late = await timeout_example(0.2, timeout=0.05)
        print(f"Timeout success: {ok}, timeout exceeded: {late}")

        work = [(i, 0.05) for i in range(6)]
        results, peak = await bounded_gather(work, max_concurrent=2)
        print(f"Bounded results: {results}, peak concurrency: {peak}")

        chunks = []
        async for chunk in stream_chunks("abcdef", 2):
            chunks.append(chunk)
        print(f"Streamed chunks: {chunks}")

        result = await run_blocking(sum, [1, 2, 3])
        print(f"run_in_executor result: {result}")

        counter = {"attempts": 0}

        async def sometimes_fails() -> str:
            counter["attempts"] += 1
            if counter["attempts"] < 2:
                raise RuntimeError("flaky")
            return "ok"

        retry_result = await retry_async(sometimes_fails)
        print(f"Retry result: {retry_result} after {counter['attempts']} attempts")

    asyncio.run(_demo())


__all__ = [
    "timeout_example",
    "bounded_gather",
    "stream_chunks",
    "run_blocking",
    "retry_async",
    "demonstrate_async_patterns",
]
