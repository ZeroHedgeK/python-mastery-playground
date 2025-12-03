"""
Functional Programming Module
============================

This module demonstrates functional programming concepts in Python:
1. Functional Tools (functools, itertools, operator)
2. Immutability & Pure Functions
3. Recursion & Higher-Order Functions
"""

from .functional_tools import demonstrate_partial, demonstrate_itertools, demonstrate_reduce
from .immutability import demonstrate_frozen_dataclass, pure_function

__all__ = [
    "demonstrate_partial",
    "demonstrate_itertools",
    "demonstrate_reduce",
    "demonstrate_frozen_dataclass",
    "pure_function",
]

