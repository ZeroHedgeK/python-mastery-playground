"""
Asyncio basics: coroutines, tasks, gather, as_completed, and common mistakes.

Use asyncio for high-concurrency I/O-bound workflows. Demonstrates non-blocking
sleep, concurrent tasks, and processing results as they arrive.
"""

from __future__ import annotations

import asyncio
import time

from python_mastery.concurrency import asyncio_demo as _library_reference  # noqa: F401


async def simulate_io(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} finished after {delay:.2f}s"


async def example_sequential_vs_gather() -> None:
    print("\nExample 1: Sequential await vs asyncio.gather")
    start = time.perf_counter()
    a = await simulate_io("A", 0.3)
    b = await simulate_io("B", 0.3)
    seq_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    a2, b2 = await asyncio.gather(simulate_io("A", 0.3), simulate_io("B", 0.3))
    par_elapsed = time.perf_counter() - start

    print(f"  sequential {seq_elapsed:.3f}s -> {[a, b]}")
    print(f"  gather    {par_elapsed:.3f}s -> {[a2, b2]}")


async def example_create_task() -> None:
    print("\nExample 2: create_task fire-and-forget (await later)")
    task = asyncio.create_task(simulate_io("background", 0.2))
    print("  doing other work while task runs...")
    await asyncio.sleep(0.05)
    result = await task
    print("  task result ->", result)


async def example_as_completed() -> None:
    print("\nExample 3: as_completed processes fastest first")
    coros = [
        simulate_io("fast", 0.1),
        simulate_io("slow", 0.25),
        simulate_io("mid", 0.18),
    ]
    for future in asyncio.as_completed(coros):
        result = await future
        print("  got:", result)


async def example_mix_fast_and_slow() -> None:
    print("\nExample 4: Mixing fast/slow shows non-blocking behavior")
    start = time.perf_counter()
    results = await asyncio.gather(simulate_io("fast", 0.1), simulate_io("slow", 0.4))
    elapsed = time.perf_counter() - start
    print(f"  results: {results}")
    print(f"  elapsed: {elapsed:.3f}s (faster than slow + fast sequential)")


async def example_forgetting_await() -> None:
    print("\nExample 5: Common mistake — forgetting await")
    coro = simulate_io("oops", 0.05)
    print("  without await ->", coro)
    result = await coro
    print("  with await ->", result)


async def run_all_async() -> None:
    print("=" * 70)
    print("DEMONSTRATING ASYNCIO BASICS")
    print("=" * 70)

    await example_sequential_vs_gather()
    await example_create_task()
    await example_as_completed()
    await example_mix_fast_and_slow()
    await example_forgetting_await()

    print("\nAll asyncio basic examples completed.")


def run_all() -> None:
    asyncio.run(run_all_async())


if __name__ == "__main__":
    run_all()
