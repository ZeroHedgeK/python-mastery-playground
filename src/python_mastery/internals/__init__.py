"""
Python Internals Module
======================

This module explores the low-level details of CPython:
1. Bytecode Analysis (dis)
2. Memory Management (Reference Counting, GC)
"""

from .bytecode_inspector import inspect_function
from .memory_management import demonstrate_garbage_collection, demonstrate_ref_counting

__all__ = [
    "inspect_function",
    "demonstrate_ref_counting",
    "demonstrate_garbage_collection",
]
