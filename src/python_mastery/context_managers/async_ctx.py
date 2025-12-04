"""
Async Context Managers
=====================

Demonstrates how to create context managers for 'async with' statements.
These are fundamental for asyncio, database connections, and network sessions.
"""

import asyncio
import time


class AsyncTimer:
    """
    An async version of the Timer.
    Uses __aenter__ and __aexit__.
    """

    def __init__(self, name):
        self.name = name
        self.start = None

    async def __aenter__(self):
        # Can await things here (e.g., db connection)
        print(f"[{self.name}] Starting async operation...")
        self.start = time.perf_counter()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Can await cleanup here (e.g., closing connection)
        elapsed = time.perf_counter() - self.start
        print(f"[{self.name}] Finished in {elapsed:.4f}s")
        # Like sync __exit__, return True to suppress exceptions


async def main():
    print("--- Async Context Manager ---")

    async with AsyncTimer("DataFetch"):
        print("   ... Simulating network I/O (await sleep)")
        await asyncio.sleep(0.1)

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
