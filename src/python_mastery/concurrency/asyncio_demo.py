"""
AsyncIO Demo (Event Loop)
========================

AsyncIO uses cooperative multitasking. Functions (coroutines) yield control
back to the event loop when they are waiting (await), allowing other tasks to run.
Very efficient for high-concurrency I/O.
"""

import asyncio
import time
from typing import Any


async def fetch_data(source_id: int) -> dict[str, Any]:
    """A coroutine that simulates fetching data asynchronously."""
    print(f"Task-{source_id}: Sending request...")
    # await passes control back to the loop while waiting
    await asyncio.sleep(0.5)
    print(f"Task-{source_id}: Data received!")
    return {"id": source_id, "data": "chunk"}


async def main() -> None:
    """Main async entry point demonstrating concurrent task execution."""
    print("\n=== AsyncIO (Event Loop) ===")
    start_time = time.perf_counter()

    # Create 10 concurrent tasks
    tasks = [fetch_data(i) for i in range(10)]

    print(f"Scheduling {len(tasks)} requests concurrently...")

    # gather runs them all at the same time
    results = await asyncio.gather(*tasks)

    elapsed = time.perf_counter() - start_time
    print(f"All {len(results)} requests finished in {elapsed:.2f}s")

    # Note: 10 * 0.5s = 5.0s sequential.
    # AsyncIO does it in ~0.5s total because they wait in parallel.


def demonstrate_asyncio() -> None:
    """Entry point for running the async main function."""
    asyncio.run(main())


if __name__ == "__main__":
    demonstrate_asyncio()
