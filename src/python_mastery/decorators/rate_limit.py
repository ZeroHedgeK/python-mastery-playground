"""
rate_limit_decorator.py - The @rate_limit decorator implementation.

This module contains the @rate_limit decorator that limits function call frequency.
Thread-safe implementation with async function support.
"""

import asyncio
import functools
import logging
import threading
import time
from collections.abc import Callable
from typing import Any

from python_mastery.exceptions import RateLimitExceeded

logger = logging.getLogger(__name__)


def rate_limit(calls: int = 5, period: float = 60.0):
    """
    A decorator that limits how many times a function can be called within a time period.

    This decorator prevents functions from being called too frequently. It's useful for:
    - API rate limiting
    - Preventing server overload
    - Controlling resource usage

    Features:
        - Thread-safe using threading.Lock
        - Supports both sync and async functions
        - Raises RateLimitExceeded with detailed information

    Args:
        calls: Maximum number of calls allowed (default: 5)
        period: Time period in seconds (default: 60.0)

    Returns:
        A decorator that enforces rate limiting

    Raises:
        RateLimitExceeded: When the rate limit is exceeded
    """

    def decorator(func: Callable) -> Callable:
        """
        The decorator that wraps the function with rate limiting logic.

        Args:
            func: The function to be decorated

        Returns:
            A wrapper function with rate limiting
        """

        # Create a lock for thread-safe access to call timestamps
        lock = threading.Lock()

        # List to store timestamps of recent calls
        call_times: list[float] = []

        def _check_rate_limit() -> None:
            """
            Check and enforce rate limit. Must be called with lock held.
            Raises RateLimitExceeded if limit is exceeded.
            """
            nonlocal call_times

            current_time = time.time()

            # Remove timestamps that are older than the period
            call_times = [t for t in call_times if current_time - t < period]

            # Check if we've exceeded the rate limit
            if len(call_times) >= calls:
                oldest_call = min(call_times)
                wait_time = period - (current_time - oldest_call)
                raise RateLimitExceeded(calls, period, wait_time)

            # Record this call's timestamp
            call_times.append(current_time)

            logger.debug(
                "Rate limit: %d/%d calls used in current period",
                len(call_times),
                calls,
            )

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                """Async wrapper with rate limiting."""
                with lock:
                    _check_rate_limit()
                return await func(*args, **kwargs)

            return async_wrapper
        else:

            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                """Sync wrapper with rate limiting."""
                with lock:
                    _check_rate_limit()
                return func(*args, **kwargs)

            return wrapper

    return decorator
