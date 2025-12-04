"""
Custom Exceptions for Python Mastery Playground.

This module defines a hierarchy of custom exceptions used throughout the library.
Custom exceptions provide better error handling, clearer error messages, and allow
callers to catch specific error types.
"""


class PythonMasteryError(Exception):
    """
    Base exception for all Python Mastery library errors.

    All custom exceptions in this library inherit from this class,
    allowing callers to catch all library-specific errors with a single except clause.
    """


class RateLimitExceeded(PythonMasteryError):
    """
    Raised when a rate-limited function exceeds its allowed call frequency.

    Attributes:
        calls: Maximum number of calls allowed in the period.
        period: Time period in seconds.
        wait_time: Seconds to wait before the next call is allowed.
    """

    def __init__(self, calls: int, period: float, wait_time: float) -> None:
        self.calls = calls
        self.period = period
        self.wait_time = wait_time
        super().__init__(
            f"Rate limit exceeded. Maximum {calls} calls allowed per {period} seconds. "
            f"Please wait {wait_time:.1f} seconds before trying again."
        )


class CacheError(PythonMasteryError):
    """Base exception for cache-related errors."""


class CacheKeyError(CacheError):
    """
    Raised when cache key generation fails.

    This typically happens when function arguments cannot be hashed
    or converted to a consistent cache key.
    """

    def __init__(self, func_name: str, reason: str) -> None:
        self.func_name = func_name
        self.reason = reason
        super().__init__(f"Failed to generate cache key for '{func_name}': {reason}")


class RetryError(PythonMasteryError):
    """Base exception for retry-related errors."""


class RetryExhausted(RetryError):
    """
    Raised when all retry attempts have been exhausted.

    Attributes:
        func_name: Name of the function that failed.
        max_attempts: Total number of attempts made.
        last_exception: The last exception that caused the final failure.
    """

    def __init__(
        self, func_name: str, max_attempts: int, last_exception: Exception
    ) -> None:
        self.func_name = func_name
        self.max_attempts = max_attempts
        self.last_exception = last_exception
        super().__init__(
            f"Function '{func_name}' failed after {max_attempts} attempts. "
            f"Last error: {last_exception}"
        )


class TimerError(PythonMasteryError):
    """
    Raised when timer operations fail.

    For example, accessing elapsed time before the timer has started.
    """


class ContextManagerError(PythonMasteryError):
    """Base exception for context manager related errors."""


class ResourceAcquisitionError(ContextManagerError):
    """Raised when a context manager fails to acquire a resource."""

    def __init__(self, resource_name: str, reason: str) -> None:
        self.resource_name = resource_name
        self.reason = reason
        super().__init__(f"Failed to acquire resource '{resource_name}': {reason}")
