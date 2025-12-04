"""
Async context manager examples using `AsyncTimer` and `async with`.

We demonstrate basic timing, nested async contexts, and exception behavior. Each
example runs quickly with small sleeps so you can execute the file directly via
`asyncio.run` and watch the lifecycle prints.
"""

from __future__ import annotations

import asyncio

from python_mastery.context_managers import AsyncTimer


async def example_basic_async_timer() -> None:
    print("\nExample 1: Basic async timing around awaited work")
    async with AsyncTimer("basic"):
        await asyncio.sleep(0.05)
        print("  inside: finished awaited work")


async def example_nested_async_timers() -> None:
    print("\nExample 2: Nested async context managers")
    async with AsyncTimer("outer"):
        await asyncio.sleep(0.02)
        async with AsyncTimer("inner"):
            await asyncio.sleep(0.03)
            print("  inside inner async block")
        await asyncio.sleep(0.01)
        print("  back in outer async block")


async def example_exception_handling() -> None:
    print("\nExample 3: Exceptions still trigger __aexit__")
    try:
        async with AsyncTimer("failing"):
            await asyncio.sleep(0.02)
            raise RuntimeError("async failure")
    except RuntimeError as exc:
        print(f"  caught: {exc}")


async def example_real_world_pattern() -> None:
    print("\nExample 4: Wrapping concurrent tasks with a timer")

    async with AsyncTimer("gathered_tasks"):
        results = await asyncio.gather(
            asyncio.sleep(0.03, result="task-1"),
            asyncio.sleep(0.04, result="task-2"),
        )
        print(f"  gathered results: {results}")


async def run_all_async() -> None:
    print("=" * 70)
    print("DEMONSTRATING ASYNC CONTEXT MANAGERS")
    print("=" * 70)

    await example_basic_async_timer()
    await example_nested_async_timers()
    await example_exception_handling()
    await example_real_world_pattern()

    print("\nAll async context examples completed.")


def run_all() -> None:
    asyncio.run(run_all_async())


if __name__ == "__main__":
    run_all()
