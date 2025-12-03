"""
cache_decorator.py - The @cache decorator implementation.

This module contains the @cache decorator that caches function results with TTL expiration.
Each line is explained in detail to help understand how decorators work.
"""

import functools
import time
from collections.abc import Callable
from typing import Any


def cache(ttl: float = 300.0):
    """
    A decorator that caches function results with time-to-live expiration.

    This decorator stores function results and returns the cached value
    for subsequent calls with the same arguments, until the TTL expires.
    It's useful for expensive computations, API calls, or database queries.

    Args:
        ttl: Time-to-live in seconds (default: 300.0 = 5 minutes)

    Returns:
        A decorator that caches function results
    """

    def decorator(func: Callable) -> Callable:
        """
        The decorator that wraps the function with caching logic.

        Args:
            func: The function to be decorated

        Returns:
            A wrapper function with caching capability
        """

        # Dictionary to store cached results
        # Key: arguments tuple, Value: (result, timestamp)
        cache_store = {}

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that implements caching logic.

            This function checks if we have a valid cached result for the given
            arguments. If so, it returns the cached value. Otherwise, it calls
            the original function, caches the result, and returns it.
            """

            # Create a key from the arguments
            # We convert kwargs to a sorted tuple to ensure consistent keys
            key = (args, tuple(sorted(kwargs.items())))

            # Get current time
            current_time = time.time()

            # Check if we have a cached result that hasn't expired
            if key in cache_store:
                cached_result, timestamp = cache_store[key]

                # Check if the cached result is still valid (within TTL)
                if current_time - timestamp < ttl:
                    print(f"Cache hit for {func.__name__}{args}, {kwargs}")
                    return cached_result
                else:
                    # Cache expired, remove it
                    print(f"Cache expired for {func.__name__}{args}, {kwargs}")
                    del cache_store[key]

            # Cache miss or expired - call the original function
            print(f"Cache miss for {func.__name__}{args}, {kwargs}")
            result = func(*args, **kwargs)

            # Store the result in cache with current timestamp
            cache_store[key] = (result, current_time)

            return result

        return wrapper

    return decorator
