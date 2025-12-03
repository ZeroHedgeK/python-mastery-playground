"""
rate_limit_decorator.py - The @rate_limit decorator implementation.

This module contains the @rate_limit decorator that limits function call frequency.
Each line is explained in detail to help understand how decorators work.
"""

import functools
import threading
import time
from collections.abc import Callable
from typing import Any


def rate_limit(calls: int = 5, period: float = 60.0):
    """
    A decorator that limits how many times a function can be called within a time period.

    This decorator prevents functions from being called too frequently. It's useful for:
    - API rate limiting
    - Preventing server overload
    - Controlling resource usage

    Args:
        calls: Maximum number of calls allowed (default: 5)
        period: Time period in seconds (default: 60.0)

    Returns:
        A decorator that enforces rate limiting
    """

    # Create a lock for thread-safe access to call timestamps
    lock = threading.Lock()

    # List to store timestamps of recent calls
    call_times = []

    def decorator(func: Callable) -> Callable:
        """
        The decorator that wraps the function with rate limiting logic.

        Args:
            func: The function to be decorated

        Returns:
            A wrapper function with rate limiting
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that implements rate limiting.

            This function tracks call times and either allows the call to proceed
            or raises an exception if the rate limit has been exceeded.
            """

            nonlocal call_times  # Access the outer call_times list

            with lock:  # Acquire lock for thread-safe operations
                # Get current time
                current_time = time.time()

                # Remove timestamps that are older than the period
                # This keeps only recent calls within our time window
                call_times = [t for t in call_times if current_time - t < period]

                # Check if we've exceeded the rate limit
                if len(call_times) >= calls:
                    # Calculate when the next call would be allowed
                    oldest_call = min(call_times)
                    wait_time = period - (current_time - oldest_call)

                    raise RuntimeError(
                        f"Rate limit exceeded. Maximum {calls} calls allowed per {period} seconds. "
                        f"Please wait {wait_time:.1f} seconds before trying again."
                    )

                # Record this call's timestamp
                call_times.append(current_time)

                # Log the current rate limit status
                print(f"Rate limit: {len(call_times)}/{calls} calls used in current period")

            # Call the original function
            return func(*args, **kwargs)

        return wrapper

    return decorator
