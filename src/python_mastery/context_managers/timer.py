"""
Timer Context Manager
====================

This module demonstrates two approaches to creating a context manager for timing code execution:
1. Class-based approach using __enter__ and __exit__ methods
2. Generator-based approach using the @contextmanager decorator

Both approaches achieve the same goal but have different implementation styles and use cases.
"""

import time
from contextlib import contextmanager


class Timer:
    """
    Class-based timer context manager.

    This approach provides more control and is better suited for complex
    resource management scenarios where you need to maintain state.

    Usage:
        with Timer() as timer:
            # Your code here
            print(f"Elapsed time: {timer.elapsed:.4f} seconds")
    """

    def __init__(self, name: str | None = None):
        """
        Initialize the timer.

        Args:
            name: Optional name for the timer (useful for identification)
        """
        self.name = name
        self.start_time: float | None = None
        self.end_time: float | None = None

    def __enter__(self):
        """
        Enter the runtime context.

        Returns:
            self: The timer instance, allowing access to elapsed time
        """
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context.

        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred

        Returns:
            bool: False to propagate exceptions, True to suppress them
        """
        self.end_time = time.perf_counter()
        assert self.start_time is not None, "Timer was not started"
        elapsed = self.end_time - self.start_time

        # Print timing information
        timer_name = f" '{self.name}'" if self.name else ""
        print(f"Timer{timer_name}: {elapsed:.4f} seconds")

        # Return False to propagate any exceptions that occurred
        return False

    @property
    def elapsed(self) -> float | None:
        """
        Get the elapsed time in seconds.

        Returns:
            float: Elapsed time if timer has started, None otherwise
        """
        if self.start_time is None:
            return None
        if self.end_time is None:
            # Timer is still running, calculate current elapsed time
            return time.perf_counter() - self.start_time
        # Timer has finished, use the calculated end time
        return self.end_time - self.start_time


@contextmanager
def timer_context(name: str | None = None):
    """
    Generator-based timer context manager using @contextmanager decorator.

    This approach is more concise and Pythonic for simple resource management.
    It's ideal when you don't need to maintain complex state or provide
    additional methods on the context manager.

    Usage:
        with timer_context("my_operation"):
            # Your code here
            # Time will be printed automatically on exit

    Args:
        name: Optional name for the timer (useful for identification)

    Yields:
        None: This context manager doesn't provide access to timing data
    """
    start_time = time.perf_counter()

    try:
        # Yield control to the code block within the 'with' statement
        yield

    finally:
        # This block always executes, even if an exception occurs
        end_time = time.perf_counter()
        elapsed = end_time - start_time

        # Print timing information
        timer_name = f" '{name}'" if name else ""
        print(f"Timer{timer_name}: {elapsed:.4f} seconds")


# Example usage and comparison
if __name__ == "__main__":
    print("=== Class-based Timer Example ===")

    # Example 1: Basic usage
    with Timer() as timer:
        # Simulate some work
        time.sleep(0.1)
        print(f"Work completed in {timer.elapsed:.4f} seconds (so far)")

    # Example 2: Named timer
    with Timer("database_query"):
        time.sleep(0.05)
        # Access elapsed time after the block
        # Note: elapsed will be None until __exit__ is called
        print("Query executed")

    print("\n=== @contextmanager Timer Example ===")

    # Example 3: Using the decorator approach
    with timer_context("file_processing"):
        time.sleep(0.075)
        print("File processed")

    print("\n=== Exception Handling Example ===")

    # Example 4: Exception handling with class-based timer
    try:
        with Timer("exception_test") as timer:
            time.sleep(0.02)
            raise ValueError("Something went wrong!")
    except ValueError as e:
        print(f"Caught exception: {e}")
        print(f"Timer still recorded: {timer.elapsed:.4f} seconds")

    # Example 5: Exception handling with decorator approach
    try:
        with timer_context("exception_test2"):
            time.sleep(0.02)
            raise ValueError("Another error!")
    except ValueError as e:
        print(f"Caught exception: {e}")
        # Note: We can't access elapsed time with this approach
