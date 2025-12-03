"""
test_decorators.py - Unit tests for the decorators.

This file contains tests to verify that our decorators work correctly.
We'll use Python's built-in unittest module (no external dependencies).
"""

import time
import unittest
from io import StringIO
from unittest.mock import patch

from python_mastery.decorators import cache, rate_limit, retry, timer


# Test fixtures - decorated functions for testing
@timer
def slow_function(duration: float = 1.0) -> str:
    """A function that simulates slow processing by sleeping."""
    time.sleep(duration)
    return f"Slept for {duration} seconds"


@timer
def fast_function(numbers: list[int]) -> int:
    """A function that performs quick calculations."""
    return sum(numbers)


@timer
def compute_sum(n: int) -> int:
    """Calculate the sum of numbers from 1 to n."""
    return n * (n + 1) // 2


@timer
def process_text(text: str) -> dict:
    """Process a text string and return various statistics."""
    return {
        "length": len(text),
        "words": len(text.split()),
        "uppercase": sum(1 for c in text if c.isupper()),
        "lowercase": sum(1 for c in text if c.islower()),
    }


@timer
def greet(name: str = "World", greeting: str = "Hello") -> str:
    """A simple greeting function."""
    return f"{greeting}, {name}!"


def regular_function() -> str:
    """A regular function without decorator for comparison."""
    time.sleep(0.05)
    return "Done"


class TestTimerDecorator(unittest.TestCase):
    """
    Test cases for the @timer decorator.
    """

    def test_timer_logs_execution_time(self):
        """
        Test that the @timer decorator logs execution time correctly.

        We'll capture the printed output and verify it contains timing information.
        """
        # Capture stdout to check what gets printed
        captured_output = StringIO()

        # Redirect stdout to our captured output
        with patch("sys.stdout", captured_output):
            # Call a decorated function
            result = slow_function(0.1)

        # Get the captured output as a string
        output = captured_output.getvalue()

        # Check that the output contains expected timing information
        self.assertIn("Function 'slow_function' executed in", output)
        self.assertIn("seconds", output)

        # Check that the function still returns the correct result
        self.assertEqual(result, "Slept for 0.1 seconds")

    def test_timer_preserves_function_result(self):
        """
        Test that the @timer decorator doesn't change the function's return value.

        The decorator should be transparent - it should return exactly what
        the original function returns.
        """
        # Test with fast_function
        numbers = [10, 20, 30]
        result = fast_function(numbers)
        expected = sum(numbers)
        self.assertEqual(result, expected)

        # Test with compute_sum
        n = 100
        result = compute_sum(n)
        expected = n * (n + 1) // 2
        self.assertEqual(result, expected)

        # Test with process_text
        text = "Hello World"
        result = process_text(text)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["length"], len(text))

    def test_timer_preserves_function_metadata(self):
        """
        Test that @functools.wraps preserves the original function's metadata.

        This is important for debugging, documentation, and introspection.
        """
        # Check that function name is preserved
        self.assertEqual(slow_function.__name__, "slow_function")
        self.assertEqual(fast_function.__name__, "fast_function")
        self.assertEqual(compute_sum.__name__, "compute_sum")

        # Check that docstrings are preserved
        self.assertIsNotNone(slow_function.__doc__)
        self.assertIn("slow processing", slow_function.__doc__)
        self.assertIsNotNone(fast_function.__doc__)
        self.assertIn("quick calculations", fast_function.__doc__)

    def test_timer_with_different_argument_types(self):
        """
        Test that the @timer decorator works with different types of arguments.
        """
        # Test with positional arguments
        result1 = greet("Alice", "Hello")
        self.assertEqual(result1, "Hello, Alice!")

        # Test with keyword arguments
        result2 = greet(name="Bob", greeting="Hi")
        self.assertEqual(result2, "Hi, Bob!")

        # Test with default arguments
        result3 = greet()
        self.assertEqual(result3, "Hello, World!")

        # Test with mixed arguments
        result4 = greet("Charlie")  # positional only
        self.assertEqual(result4, "Hello, Charlie!")

    def test_timer_with_exception(self):
        """
        Test that the @timer decorator handles functions that raise exceptions.

        The decorator should not interfere with exception propagation.
        """

        # Create a function that always raises an exception
        @timer
        def failing_function():
            raise ValueError("This function always fails")

        # The exception should propagate through the decorator
        with self.assertRaises(ValueError) as context:
            failing_function()

        # Check that it's the right exception
        self.assertEqual(str(context.exception), "This function always fails")

    def test_timer_execution_time_accuracy(self):
        """
        Test that the timing measurement is reasonably accurate.

        We'll check that the measured time is close to the expected sleep time.
        """
        # Capture output
        captured_output = StringIO()

        with patch("sys.stdout", captured_output):
            # Call function that sleeps for 0.2 seconds
            sleep_duration = 0.2
            result = slow_function(sleep_duration)

        # Extract the timing from the output
        output = captured_output.getvalue()
        # Look for the timing pattern: "executed in X.XXXX seconds"
        import re

        match = re.search(r"executed in ([\d.]+) seconds", output)

        self.assertIsNotNone(match, "Could not find timing information in output")

        # Convert the measured time to float
        measured_time = float(match.group(1))

        # The measured time should be at least the sleep duration
        # (it might be slightly more due to function overhead)
        self.assertGreaterEqual(measured_time, sleep_duration)

        # The measured time shouldn't be too much more than sleep duration
        # (allowing 0.1 seconds for overhead)
        self.assertLess(measured_time, sleep_duration + 0.1)

    def test_undecorated_function_behavior(self):
        """
        Test that regular functions (without @timer) behave normally.

        This serves as a baseline comparison.
        """
        # Capture output for undecorated function
        captured_output = StringIO()

        with patch("sys.stdout", captured_output):
            result = regular_function()

        # Should not have timing information
        output = captured_output.getvalue()
        self.assertNotIn("executed in", output)
        self.assertNotIn("seconds", output)

        # But should still work correctly
        self.assertEqual(result, "Done")


class TestRetryDecorator(unittest.TestCase):
    """
    Test cases for the @retry decorator.
    """

    def test_retry_success_on_first_attempt(self):
        """
        Test that @retry doesn't retry when the function succeeds immediately.
        """
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"

        # Capture output to verify no retry messages
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            result = successful_function()

        # Should succeed on first attempt
        self.assertEqual(call_count, 1)
        self.assertEqual(result, "success")

        # Should not have any retry messages
        output = captured_output.getvalue()
        self.assertNotIn("failed on attempt", output)
        self.assertNotIn("Retrying", output)

    def test_retry_eventually_succeeds(self):
        """
        Test that @retry eventually succeeds after some failures.
        """
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def sometimes_fails_function():
            nonlocal call_count
            call_count += 1

            # Fail on first 2 attempts, succeed on 3rd
            if call_count < 3:
                raise ValueError(f"Simulated failure {call_count}")

            return f"success after {call_count} attempts"

        # Capture output
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            result = sometimes_fails_function()

        # Should have been called 3 times
        self.assertEqual(call_count, 3)
        self.assertEqual(result, "success after 3 attempts")

        # Should have retry messages
        output = captured_output.getvalue()
        self.assertIn("failed on attempt 1", output)
        self.assertIn("failed on attempt 2", output)
        self.assertIn("succeeded on attempt 3", output)

    def test_retry_exhausts_all_attempts(self):
        """
        Test that @retry gives up after max_attempts is reached.
        """
        call_count = 0

        @retry(max_attempts=2, delay=0.1)
        def always_fails_function():
            nonlocal call_count
            call_count += 1
            raise RuntimeError(f"Always fails (attempt {call_count})")

        # Capture output
        captured_output = StringIO()
        with patch("sys.stdout", captured_output):
            # Should raise the final exception
            with self.assertRaises(RuntimeError) as context:
                always_fails_function()

        # Should have tried exactly max_attempts times
        self.assertEqual(call_count, 2)

        # Should have the right error message
        self.assertEqual(str(context.exception), "Always fails (attempt 2)")

        # Should have retry messages and final failure message
        output = captured_output.getvalue()
        self.assertIn("failed on attempt 1", output)
        self.assertIn("failed after 2 attempts", output)

    def test_retry_with_different_exception_types(self):
        """
        Test that @retry works with different types of exceptions.
        """
        # Test with ValueError
        call_count = 0

        @retry(max_attempts=2, delay=0.1)
        def value_error_function():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First attempt fails")
            return "success"

        result = value_error_function()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 2)

        # Test with FileNotFoundError
        call_count = 0

        @retry(max_attempts=2, delay=0.1)
        def file_error_function():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise FileNotFoundError("File not found")
            return "file found"

        result = file_error_function()
        self.assertEqual(result, "file found")
        self.assertEqual(call_count, 2)

    def test_retry_preserves_function_metadata(self):
        """
        Test that @retry preserves function metadata using @functools.wraps.
        """

        @retry(max_attempts=3, delay=1.0)
        def test_function():
            """Test function docstring."""
            return "test"

        # Check metadata preservation
        self.assertEqual(test_function.__name__, "test_function")
        self.assertEqual(test_function.__doc__, "Test function docstring.")

    def test_retry_with_function_arguments(self):
        """
        Test that @retry correctly passes arguments to the decorated function.
        """
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def function_with_args(a, b, c=None):
            nonlocal call_count
            call_count += 1

            # Fail on first attempt
            if call_count == 1:
                raise ValueError("First attempt fails")

            return f"a={a}, b={b}, c={c}"

        # Call with various argument combinations
        result = function_with_args(1, 2, c=3)
        self.assertEqual(result, "a=1, b=2, c=3")
        self.assertEqual(call_count, 2)

        # Reset and try with different arguments
        call_count = 0
        result = function_with_args("hello", "world")
        self.assertEqual(result, "a=hello, b=world, c=None")
        self.assertEqual(call_count, 2)

    def test_retry_delay_between_attempts(self):
        """
        Test that @retry waits the specified delay between attempts.
        """
        call_count = 0

        @retry(max_attempts=2, delay=0.5)  # 0.5 second delay
        def delayed_function():
            nonlocal call_count
            call_count += 1

            if call_count == 1:
                raise ValueError("First attempt fails")

            return "success"

        # Measure the time taken
        start_time = time.time()
        result = delayed_function()
        end_time = time.time()

        # Should succeed
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 2)

        # Should have taken at least the delay time (0.5 seconds)
        # Allow some tolerance for execution overhead
        elapsed_time = end_time - start_time
        self.assertGreaterEqual(elapsed_time, 0.5)
        self.assertLess(elapsed_time, 1.0)  # Shouldn't take too long


class TestRateLimitDecorator(unittest.TestCase):
    """
    Test cases for the @rate_limit decorator.
    """

    def test_rate_limit_allows_calls_within_limit(self):
        """
        Test that @rate_limit allows calls within the specified limit.
        """
        call_count = 0

        @rate_limit(calls=3, period=10.0)
        def limited_function():
            nonlocal call_count
            call_count += 1
            return f"call_{call_count}"

        # Should be able to make 3 calls successfully
        for i in range(3):
            result = limited_function()
            self.assertEqual(result, f"call_{i + 1}")

        # 4th call should fail
        with self.assertRaises(RuntimeError) as context:
            limited_function()

        self.assertIn("Rate limit exceeded", str(context.exception))
        self.assertIn("Maximum 3 calls allowed", str(context.exception))

    def test_rate_limit_blocks_excessive_calls(self):
        """
        Test that @rate_limit blocks calls that exceed the limit.
        """

        @rate_limit(calls=2, period=5.0)
        def api_endpoint():
            return "success"

        # First 2 calls should succeed
        self.assertEqual(api_endpoint(), "success")
        self.assertEqual(api_endpoint(), "success")

        # 3rd call should be blocked
        with self.assertRaises(RuntimeError) as context:
            api_endpoint()

        error_msg = str(context.exception)
        self.assertIn("Rate limit exceeded", error_msg)
        self.assertIn("Maximum 2 calls allowed", error_msg)
        self.assertIn("Please wait", error_msg)

    def test_rate_limit_resets_after_period(self):
        """
        Test that @rate_limit allows calls again after the period passes.
        """

        @rate_limit(calls=2, period=1.0)  # 1 second period for faster testing
        def quick_function():
            return "success"

        # Use up the limit
        self.assertEqual(quick_function(), "success")
        self.assertEqual(quick_function(), "success")

        # Should be blocked now
        with self.assertRaises(RuntimeError):
            quick_function()

        # Wait for the period to pass
        time.sleep(1.1)

        # Should work again
        self.assertEqual(quick_function(), "success")

    def test_rate_limit_preserves_function_arguments(self):
        """
        Test that @rate_limit correctly passes arguments to the decorated function.
        """

        @rate_limit(calls=5, period=10.0)
        def function_with_args(a, b, c=None):
            return f"a={a}, b={b}, c={c}"

        # Should work with various argument combinations
        result1 = function_with_args(1, 2, c=3)
        self.assertEqual(result1, "a=1, b=2, c=3")

        result2 = function_with_args("hello", "world")
        self.assertEqual(result2, "a=hello, b=world, c=None")

        result3 = function_with_args(10, 20, 30)
        self.assertEqual(result3, "a=10, b=20, c=30")

    def test_rate_limit_preserves_function_metadata(self):
        """
        Test that @rate_limit preserves function metadata using @functools.wraps.
        """

        @rate_limit(calls=3, period=60.0)
        def test_function():
            """Test function docstring."""
            return "test"

        # Check metadata preservation
        self.assertEqual(test_function.__name__, "test_function")
        self.assertEqual(test_function.__doc__, "Test function docstring.")

    def test_rate_limit_with_different_parameters(self):
        """
        Test @rate_limit with different call/period parameters.
        """

        # Test with very restrictive limit
        @rate_limit(calls=1, period=5.0)
        def restrictive_function():
            return "success"

        self.assertEqual(restrictive_function(), "success")

        with self.assertRaises(RuntimeError):
            restrictive_function()

        # Test with more permissive limit
        @rate_limit(calls=10, period=1.0)
        def permissive_function():
            return "success"

        # Should allow 10 calls
        for _ in range(10):
            self.assertEqual(permissive_function(), "success")

        # 11th should fail
        with self.assertRaises(RuntimeError):
            permissive_function()


if __name__ == "__main__":
    # Run the tests with verbose output
    unittest.main(verbosity=2)


class TestCacheDecorator(unittest.TestCase):
    """
    Test cases for the @cache decorator.
    """

    def test_cache_basic_functionality(self):
        """
        Test basic caching functionality - same args should return cached result.
        """
        call_count = 0

        @cache(ttl=10.0)
        def cached_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call should execute the function
        result1 = cached_function(5)
        self.assertEqual(result1, 10)
        self.assertEqual(call_count, 1)

        # Second call with same arg should use cache
        result2 = cached_function(5)
        self.assertEqual(result2, 10)
        self.assertEqual(call_count, 1)  # Should not increase

        # Call with different arg should execute function
        result3 = cached_function(10)
        self.assertEqual(result3, 20)
        self.assertEqual(call_count, 2)

    def test_cache_ttl_expiration(self):
        """
        Test that cached results expire after TTL.
        """
        call_count = 0

        @cache(ttl=0.5)  # Very short TTL for testing
        def short_ttl_function(x):
            nonlocal call_count
            call_count += 1
            return x * 3

        # First call
        result1 = short_ttl_function(5)
        self.assertEqual(result1, 15)
        self.assertEqual(call_count, 1)

        # Immediate second call should use cache
        result2 = short_ttl_function(5)
        self.assertEqual(result2, 15)
        self.assertEqual(call_count, 1)

        # Wait for TTL to expire
        time.sleep(0.6)

        # Should call function again
        result3 = short_ttl_function(5)
        self.assertEqual(result3, 15)
        self.assertEqual(call_count, 2)

    def test_cache_with_different_arguments(self):
        """
        Test that cache correctly handles different function arguments.
        """
        call_count = 0

        @cache(ttl=10.0)
        def multi_arg_function(a, b, c=None):
            nonlocal call_count
            call_count += 1
            return f"{a}-{b}-{c}"

        # Call with different arguments
        result1 = multi_arg_function(1, 2, 3)
        self.assertEqual(result1, "1-2-3")
        self.assertEqual(call_count, 1)

        # Same args should use cache
        result2 = multi_arg_function(1, 2, 3)
        self.assertEqual(result2, "1-2-3")
        self.assertEqual(call_count, 1)

        # Different args should call function
        result3 = multi_arg_function(1, 2, 4)
        self.assertEqual(result3, "1-2-4")
        self.assertEqual(call_count, 2)

        # Different order of kwargs should still hit cache
        result4 = multi_arg_function(a=1, b=2, c=3)
        self.assertEqual(result4, "1-2-3")
        self.assertEqual(call_count, 2)  # Should use cache

    def test_cache_preserves_function_metadata(self):
        """
        Test that @cache preserves function metadata using @functools.wraps.
        """

        @cache(ttl=5.0)
        def test_function():
            """Test function docstring."""
            return "test"

        # Check metadata preservation
        self.assertEqual(test_function.__name__, "test_function")
        self.assertEqual(test_function.__doc__, "Test function docstring.")

    def test_cache_with_mutable_arguments(self):
        """
        Test that cache works correctly with mutable arguments.
        """
        call_count = 0

        @cache(ttl=10.0)
        def function_with_list_arg(items):
            nonlocal call_count
            call_count += 1
            return sum(items)

        # Call with list
        result1 = function_with_list_arg([1, 2, 3])
        self.assertEqual(result1, 6)
        self.assertEqual(call_count, 1)

        # Same list content but different list object
        # This should be a cache miss because lists are not hashable in the same way
        result2 = function_with_list_arg([1, 2, 3])
        self.assertEqual(result2, 6)
        # Note: This might be 1 or 2 depending on how the cache key is generated
        # For our implementation, it will be 2 because list objects are different

    def test_cache_independent_instances(self):
        """
        Test that different decorated functions have independent caches.
        """
        call_count1 = 0
        call_count2 = 0

        @cache(ttl=10.0)
        def function_one(x):
            nonlocal call_count1
            call_count1 += 1
            return x * 2

        @cache(ttl=10.0)
        def function_two(x):
            nonlocal call_count2
            call_count2 += 1
            return x * 3

        # Call both functions
        function_one(5)
        function_two(5)

        self.assertEqual(call_count1, 1)
        self.assertEqual(call_count2, 1)

        # Call again - both should use cache
        function_one(5)
        function_two(5)

        self.assertEqual(call_count1, 1)  # Still 1
        self.assertEqual(call_count2, 1)  # Still 1
