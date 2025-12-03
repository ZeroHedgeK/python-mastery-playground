"""
decorators - A collection of useful Python decorators for learning purposes.

This package provides four practical decorators with detailed implementations:

- timer: Logs execution time of functions
- retry: Retries failed functions with configurable attempts
- rate_limit: Throttles function calls to prevent rate limit violations
- cache: Caches function results with time-to-live expiration

Each decorator is implemented in its own module with detailed explanations
to help understand how decorators work in Python.
"""

from .cache import cache
from .rate_limit import rate_limit
from .retry import retry
from .timer import timer

__all__ = ["cache", "rate_limit", "retry", "timer"]
