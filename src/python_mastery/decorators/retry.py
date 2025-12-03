"""
retry_decorator.py - The @retry decorator implementation.

This module contains the @retry decorator that retries failed functions.
Each line is explained in detail to help understand how decorators work.
"""

import functools
import time
from collections.abc import Callable
from typing import Any


def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    A decorator that retries a function if it fails.

    This decorator will catch exceptions and retry the function multiple times
    before giving up. It's useful for network calls, file operations, or any
    function that might fail temporarily.

    Args:
        max_attempts: Maximum number of times to try the function (default: 3)
        delay: Seconds to wait between retries (default: 1.0)

    Returns:
        A decorator that wraps the function with retry logic
    """

    # This is the actual decorator function that takes the function to wrap
    def decorator(func: Callable) -> Callable:
        """
        The decorator that wraps the function with retry logic.

        Args:
            func: The function to be decorated

        Returns:
            A wrapper function with retry capability
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that implements the retry logic.

            This function will attempt to call the original function multiple
            times, catching exceptions and retrying until success or max_attempts.
            """

            # Initialize attempt counter
            attempts = 0

            # Loop until we succeed or run out of attempts
            while attempts < max_attempts:
                attempts += 1  # Increment attempt counter

                try:
                    # Try to execute the original function
                    # If this succeeds, we return the result immediately
                    result = func(*args, **kwargs)

                    # If we get here, the function succeeded
                    if attempts > 1:
                        print(f"Function '{func.__name__}' succeeded on attempt {attempts}")

                    return result

                except Exception as e:
                    # If this is the last attempt, re-raise the exception
                    if attempts == max_attempts:
                        print(f"Function '{func.__name__}' failed after {max_attempts} attempts")
                        raise  # Re-raise the last exception

                    # Otherwise, print a message and retry
                    print(f"Function '{func.__name__}' failed on attempt {attempts}: {e}")
                    print(f"Retrying in {delay} seconds...")

                    # Wait before retrying
                    time.sleep(delay)

            # This line should never be reached due to the logic above,
            # but it's here for completeness
            raise RuntimeError(f"Failed after {max_attempts} attempts")

        return wrapper

    return decorator
