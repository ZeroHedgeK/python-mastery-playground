"""
Python Mastery Playground
========================

A comprehensive collection of advanced Python concepts and patterns.
"""

from python_mastery.exceptions import (
    CacheError,
    CacheKeyError,
    ContextManagerError,
    PythonMasteryError,
    RateLimitExceeded,
    ResourceAcquisitionError,
    RetryError,
    RetryExhausted,
    TimerError,
)

__version__ = "2.0.0"

__all__ = [
    "PythonMasteryError",
    "RateLimitExceeded",
    "CacheError",
    "CacheKeyError",
    "RetryError",
    "RetryExhausted",
    "TimerError",
    "ContextManagerError",
    "ResourceAcquisitionError",
]
