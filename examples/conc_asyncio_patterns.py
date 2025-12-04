"""
Asyncio patterns: timeouts, cancellation control, semaphores, retries, executor
bridging, async generators, and graceful shutdown.

Use these patterns to build resilient async services handling I/O-bound work at
scale while avoiding runaway tasks.
"""

from __future__ import annotations

import asyncio
import random
import time

from python_mastery.concurrency import (  # noqa: F401
    asyncio_patterns as _library_reference,
)


async def example_wait_for_timeout() -> None:
    print("\nExample 1: asyncio.wait_for with timeout")

    async def slow():
        await asyncio.sleep(0.2)
        return "done"

    try:
        await asyncio.wait_for(slow(), timeout=0.1)
    except asyncio.TimeoutError:
        print("  timed out as expected")


async def example_shield() -> None:
    print("\nExample 2: asyncio.shield to protect critical section")

    async def critical():
        await asyncio.sleep(0.15)
        return "saved"

    task = asyncio.create_task(asyncio.shield(critical()))
    try:
        await asyncio.wait_for(task, timeout=0.05)
    except asyncio.TimeoutError:
        print("  outer timeout fired, but task continues")
    result = await task
    print("  shielded result ->", result)


async def example_semaphore_bounded() -> None:
    print("\nExample 3: Semaphore to bound concurrency")
    sem = asyncio.Semaphore(3)
    started: list[int] = []

    async def worker(i: int) -> str:
        async with sem:
            started.append(i)
            await asyncio.sleep(0.1)
            return f"task {i}"

    start = time.perf_counter()
    results = await asyncio.gather(*(worker(i) for i in range(8)))
    elapsed = time.perf_counter() - start
    print(f"  results: {results}")
    print(f"  elapsed: {elapsed:.3f}s with max 3 concurrent")


async def example_retry_backoff() -> None:
    print("\nExample 4: Retry with exponential backoff")
    attempts = 0

    async def flaky() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("temporary failure")
        return "eventually succeeds"

    delay = 0.05
    while True:
        try:
            result = await flaky()
            print("  result ->", result)
            break
        except RuntimeError as exc:
            print(f"  attempt {attempts} failed: {exc}; retrying in {delay:.2f}s")
            await asyncio.sleep(delay)
            delay *= 2


async def example_executor_bridge() -> None:
    print("\nExample 5: run_in_executor for blocking work")

    def blocking_hash(data: bytes) -> int:
        total = 0
        for b in data:
            total = (total * 31 + b) % 1_000_000_007
        time.sleep(0.05)
        return total

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, blocking_hash, b"hello world")
    print("  executor result ->", result)


async def example_async_generator() -> None:
    print("\nExample 6: async generator with async for")

    async def ticker(n: int):
        for i in range(n):
            await asyncio.sleep(0.03)
            yield f"tick {i}"

    async for item in ticker(3):
        print("  got", item)


async def example_graceful_shutdown() -> None:
    print("\nExample 7: Graceful shutdown with cancellation")
    tasks: set[asyncio.Task] = set()

    async def long_task(name: str):
        try:
            for i in range(5):
                await asyncio.sleep(0.05)
                print(f"  {name} step {i}")
        except asyncio.CancelledError:
            print(f"  {name} cancelled cleanly")
            raise

    for i in range(3):
        tasks.add(asyncio.create_task(long_task(f"job-{i}")))

    await asyncio.sleep(0.12)
    print("  initiating shutdown (cancel pending tasks)")
    for t in tasks:
        t.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    print("  shutdown complete")


async def run_all_async() -> None:
    print("=" * 70)
    print("DEMONSTRATING ASYNCIO PATTERNS")
    print("=" * 70)

    await example_wait_for_timeout()
    await example_shield()
    await example_semaphore_bounded()
    await example_retry_backoff()
    await example_executor_bridge()
    await example_async_generator()
    await example_graceful_shutdown()

    print("\nAll asyncio pattern examples completed.")


def run_all() -> None:
    asyncio.run(run_all_async())


if __name__ == "__main__":
    run_all()
