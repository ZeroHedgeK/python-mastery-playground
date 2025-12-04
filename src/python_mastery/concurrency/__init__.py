"""
Concurrency Module
=================

This module explores Python's three main approaches to concurrent execution:
1. Threading (I/O bound tasks)
2. Multiprocessing (CPU bound tasks)
3. AsyncIO (Event-loop based concurrency)
"""

from .asyncio_demo import demonstrate_asyncio
from .multiprocessing_demo import demonstrate_multiprocessing
from .threading_demo import demonstrate_threading

__all__ = [
    "demonstrate_threading",
    "demonstrate_multiprocessing",
    "demonstrate_asyncio",
]
