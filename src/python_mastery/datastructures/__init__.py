"""
Data Structures Module
=====================

This module demonstrates Python's powerful built-in data structures and algorithms.
It covers:
- Advanced Slicing & Indexing
- List/Dict/Set Comprehensions
- Generators & Iterators
- collections module tools (Counter, defaultdict, etc.)
"""

from .builtins import (
    demonstrate_comprehensions,
    demonstrate_generators,
    demonstrate_slicing,
)
from .collections_demo import (
    demonstrate_counter,
    demonstrate_defaultdict,
    demonstrate_deque,
)

__all__ = [
    "demonstrate_slicing",
    "demonstrate_comprehensions",
    "demonstrate_generators",
    "demonstrate_counter",
    "demonstrate_defaultdict",
    "demonstrate_deque",
]
