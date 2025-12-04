"""
Context Managers Learning Module
===============================

This package demonstrates various context manager implementations and patterns.
Context managers provide a clean way to manage resources and handle setup/cleanup
operations automatically.

Key Concepts:
- Resource management (files, connections, locks)
- Exception handling within context blocks
- Timing and performance measurement
- Temporary state changes
- Async context managers
- Reentrancy and reusability

Available Context Managers:
- Timer: Measure execution time of code blocks
- AsyncTimer: Async version of Timer
- env_var: Temporarily set environment variables
- Reusable: Example of a reusable context manager
"""

from .async_ctx import AsyncTimer
from .reentrant import Reusable
from .state import env_var
from .timer import Timer, timer_context
from .utilities import (
    demonstrate_closing,
    demonstrate_exit_stack,
    demonstrate_nullcontext,
    demonstrate_suppress,
)

__all__ = [
    "AsyncTimer",
    "Reusable",
    "Timer",
    "demonstrate_closing",
    "demonstrate_exit_stack",
    "demonstrate_nullcontext",
    "demonstrate_suppress",
    "env_var",
    "timer_context",
]
