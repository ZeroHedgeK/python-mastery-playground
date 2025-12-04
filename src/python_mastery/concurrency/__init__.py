"""
Concurrency Module
=================

This module explores Python's three main approaches to concurrent execution:
1. Threading (I/O bound tasks)
2. Multiprocessing (CPU bound tasks)
3. AsyncIO (Event-loop based concurrency)

It also contains higher-level asyncio patterns such as cancellation, bounded
concurrency, async streams, and bridging to blocking code.
"""

from .asyncio_demo import demonstrate_asyncio
from .asyncio_patterns import demonstrate_async_patterns
from .multiprocessing_demo import demonstrate_multiprocessing
from .threading_demo import demonstrate_threading

__all__ = [
    "demonstrate_threading",
    "demonstrate_multiprocessing",
    "demonstrate_asyncio",
    "demonstrate_async_patterns",
]
