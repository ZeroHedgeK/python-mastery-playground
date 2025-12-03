"""
timer_decorator.py - The @timer decorator implementation.

This module contains the @timer decorator that logs execution time of functions.
Each line is explained in detail to help understand how decorators work.
"""

import functools
import time
from collections.abc import Callable
from typing import Any


def timer(func: Callable) -> Callable:
    """
    A decorator that logs the execution time of a function.

    This is our first decorator - it measures how long a function takes to run
    and prints the execution time. We'll break down every line to understand
    how decorators work.

    Args:
        func: The function to be decorated (the function we're wrapping)

    Returns:
        A wrapper function that adds timing functionality
    """

    # This is the wrapper function that will replace our original function
    # The *args and **kwargs allow this wrapper to accept any arguments
    # that the original function might need
    @functools.wraps(func)  # This preserves the original function's metadata
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """
        The wrapper function that adds timing logic around the original function.

        *args: Accepts any positional arguments
        **kwargs: Accepts any keyword arguments
        """

        # Record the start time before calling the original function
        # time.perf_counter() is preferred for timing as it's more precise
        start_time = time.perf_counter()

        # Call the original function with all its arguments and store the result
        # This is where the actual work happens
        result = func(*args, **kwargs)

        # Record the end time after the function completes
        end_time = time.perf_counter()

        # Calculate how long the function took to run
        execution_time = end_time - start_time

        # Print the timing information
        # We use func.__name__ to get the original function's name
        print(f"Function '{func.__name__}' executed in {execution_time:.12f} seconds")

        # Return the original function's result
        # This is crucial - decorators should be transparent to the caller
        return result

    # Return the wrapper function
    # This is what replaces the original function when we use @timer
    return wrapper


# Example usage of the @timer decorator:
# @timer
# def my_function():
#     # function code here
#     pass
