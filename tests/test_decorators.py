"""
test_decorators.py - Unit tests for the decorators.

This file contains tests to verify that our decorators work correctly.
Uses pytest with the caplog fixture to capture logging output.
"""

import logging
import re
import time

import pytest

from python_mastery.decorators import cache, rate_limit, retry, timer
from python_mastery.exceptions import RateLimitExceeded, RetryExhausted


class TestTimerDecorator:
    """Test cases for the @timer decorator."""

    def test_timer_logs_execution_time(self, caplog):
        """Test that the @timer decorator logs execution time correctly."""

        @timer
        def slow_function(duration: float = 1.0) -> str:
            time.sleep(duration)
            return f"Slept for {duration} seconds"

        with caplog.at_level(logging.INFO):
            result = slow_function(0.1)

        assert "slow_function" in caplog.text
        assert "executed in" in caplog.text
        assert "seconds" in caplog.text
        assert result == "Slept for 0.1 seconds"

    def test_timer_preserves_function_result(self):
        """Test that the @timer decorator doesn't change the function's return value."""

        @timer
        def fast_function(numbers: list[int]) -> int:
            return sum(numbers)

        @timer
        def compute_sum(n: int) -> int:
            return n * (n + 1) // 2

        @timer
        def process_text(text: str) -> dict:
            return {
                "length": len(text),
                "words": len(text.split()),
                "uppercase": sum(1 for c in text if c.isupper()),
                "lowercase": sum(1 for c in text if c.islower()),
            }

        # Test with fast_function
        numbers = [10, 20, 30]
        result = fast_function(numbers)
        assert result == sum(numbers)

        # Test with compute_sum
        n = 100
        result = compute_sum(n)
        assert result == n * (n + 1) // 2

        # Test with process_text
        text = "Hello World"
        result = process_text(text)
        assert isinstance(result, dict)
        assert result["length"] == len(text)

    def test_timer_preserves_function_metadata(self):
        """Test that @functools.wraps preserves the original function's metadata."""

        @timer
        def slow_function(duration: float = 1.0) -> str:
            """A function that simulates slow processing by sleeping."""
            time.sleep(duration)
            return f"Slept for {duration} seconds"

        @timer
        def fast_function(numbers: list[int]) -> int:
            """A function that performs quick calculations."""
            return sum(numbers)

        # Check that function name is preserved
        assert slow_function.__name__ == "slow_function"
        assert fast_function.__name__ == "fast_function"

        # Check that docstrings are preserved
        assert slow_function.__doc__ is not None
        assert "slow processing" in slow_function.__doc__
        assert fast_function.__doc__ is not None
        assert "quick calculations" in fast_function.__doc__

    def test_timer_with_different_argument_types(self):
        """Test that the @timer decorator works with different types of arguments."""

        @timer
        def greet(name: str = "World", greeting: str = "Hello") -> str:
            return f"{greeting}, {name}!"

        # Test with positional arguments
        assert greet("Alice", "Hello") == "Hello, Alice!"

        # Test with keyword arguments
        assert greet(name="Bob", greeting="Hi") == "Hi, Bob!"

        # Test with default arguments
        assert greet() == "Hello, World!"

        # Test with mixed arguments
        assert greet("Charlie") == "Hello, Charlie!"

    def test_timer_with_exception(self):
        """Test that the @timer decorator handles functions that raise exceptions."""

        @timer
        def failing_function():
            raise ValueError("This function always fails")

        with pytest.raises(ValueError, match="This function always fails"):
            failing_function()

    def test_timer_execution_time_accuracy(self, caplog):
        """Test that the timing measurement is reasonably accurate."""

        @timer
        def slow_function(duration: float = 1.0) -> str:
            time.sleep(duration)
            return f"Slept for {duration} seconds"

        sleep_duration = 0.2

        with caplog.at_level(logging.INFO):
            slow_function(sleep_duration)

        # Extract the timing from the log
        match = re.search(r"executed in ([\d.]+) seconds", caplog.text)
        assert match is not None, "Could not find timing information in log"

        measured_time = float(match.group(1))
        assert measured_time >= sleep_duration
        assert measured_time < sleep_duration + 0.1

    def test_undecorated_function_behavior(self, caplog):
        """Test that regular functions (without @timer) behave normally."""

        def regular_function() -> str:
            time.sleep(0.05)
            return "Done"

        with caplog.at_level(logging.INFO):
            result = regular_function()

        assert "executed in" not in caplog.text
        assert result == "Done"


class TestRetryDecorator:
    """Test cases for the @retry decorator."""

    def test_retry_success_on_first_attempt(self, caplog):
        """Test that @retry doesn't retry when the function succeeds immediately."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def successful_function():
            nonlocal call_count
            call_count += 1
            return "success"

        with caplog.at_level(logging.INFO):
            result = successful_function()

        assert call_count == 1
        assert result == "success"
        assert "failed on attempt" not in caplog.text

    def test_retry_eventually_succeeds(self, caplog):
        """Test that @retry eventually succeeds after some failures."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def sometimes_fails_function():
            nonlocal call_count
            call_count += 1

            if call_count < 3:
                raise ValueError(f"Simulated failure {call_count}")

            return f"success after {call_count} attempts"

        with caplog.at_level(logging.WARNING):
            result = sometimes_fails_function()

        assert call_count == 3
        assert result == "success after 3 attempts"
        assert "failed on attempt 1" in caplog.text
        assert "failed on attempt 2" in caplog.text

    def test_retry_exhausts_all_attempts(self, caplog):
        """Test that @retry gives up after max_attempts is reached."""
        call_count = 0

        @retry(max_attempts=2, delay=0.1)
        def always_fails_function():
            nonlocal call_count
            call_count += 1
            raise RuntimeError(f"Always fails (attempt {call_count})")

        with caplog.at_level(logging.WARNING):
            with pytest.raises(RetryExhausted) as exc_info:
                always_fails_function()

        assert call_count == 2
        assert exc_info.value.max_attempts == 2
        assert isinstance(exc_info.value.last_exception, RuntimeError)
        assert "failed on attempt 1" in caplog.text
        assert "failed after 2 attempts" in caplog.text

    def test_retry_with_specific_exceptions(self):
        """Test that @retry only catches specified exceptions."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1, exceptions=(ValueError,))
        def raises_type_error():
            nonlocal call_count
            call_count += 1
            raise TypeError("This should not be retried")

        # TypeError should not be caught, so it should propagate immediately
        with pytest.raises(TypeError, match="This should not be retried"):
            raises_type_error()

        assert call_count == 1  # Should only be called once

    def test_retry_with_specific_exceptions_catches_correctly(self):
        """Test that @retry catches and retries on specified exceptions."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1, exceptions=(ValueError, KeyError))
        def sometimes_fails():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First failure")
            if call_count == 2:
                raise KeyError("Second failure")
            return "success"

        result = sometimes_fails()
        assert result == "success"
        assert call_count == 3

    def test_retry_with_different_exception_types(self):
        """Test that @retry works with different types of exceptions."""
        call_count = 0

        @retry(max_attempts=2, delay=0.1)
        def value_error_function():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("First attempt fails")
            return "success"

        result = value_error_function()
        assert result == "success"
        assert call_count == 2

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
        assert result == "file found"
        assert call_count == 2

    def test_retry_preserves_function_metadata(self):
        """Test that @retry preserves function metadata using @functools.wraps."""

        @retry(max_attempts=3, delay=1.0)
        def test_function():
            """Test function docstring."""
            return "test"

        assert test_function.__name__ == "test_function"
        assert test_function.__doc__ == "Test function docstring."

    def test_retry_with_function_arguments(self):
        """Test that @retry correctly passes arguments to the decorated function."""
        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def function_with_args(a, b, c=None):
            nonlocal call_count
            call_count += 1

            if call_count == 1:
                raise ValueError("First attempt fails")

            return f"a={a}, b={b}, c={c}"

        result = function_with_args(1, 2, c=3)
        assert result == "a=1, b=2, c=3"
        assert call_count == 2

        # Reset and try with different arguments
        call_count = 0
        result = function_with_args("hello", "world")
        assert result == "a=hello, b=world, c=None"
        assert call_count == 2

    def test_retry_delay_between_attempts(self):
        """Test that @retry waits the specified delay between attempts."""
        call_count = 0

        @retry(max_attempts=2, delay=0.5)
        def delayed_function():
            nonlocal call_count
            call_count += 1

            if call_count == 1:
                raise ValueError("First attempt fails")

            return "success"

        start_time = time.time()
        result = delayed_function()
        end_time = time.time()

        assert result == "success"
        assert call_count == 2

        elapsed_time = end_time - start_time
        assert elapsed_time >= 0.5
        assert elapsed_time < 1.0


class TestRateLimitDecorator:
    """Test cases for the @rate_limit decorator."""

    def test_rate_limit_allows_calls_within_limit(self):
        """Test that @rate_limit allows calls within the specified limit."""
        call_count = 0

        @rate_limit(calls=3, period=10.0)
        def limited_function():
            nonlocal call_count
            call_count += 1
            return f"call_{call_count}"

        # Should be able to make 3 calls successfully
        for i in range(3):
            result = limited_function()
            assert result == f"call_{i + 1}"

        # 4th call should fail
        with pytest.raises(RateLimitExceeded) as exc_info:
            limited_function()

        assert exc_info.value.calls == 3
        assert "Rate limit exceeded" in str(exc_info.value)
        assert "Maximum 3 calls allowed" in str(exc_info.value)

    def test_rate_limit_blocks_excessive_calls(self):
        """Test that @rate_limit blocks calls that exceed the limit."""

        @rate_limit(calls=2, period=5.0)
        def api_endpoint():
            return "success"

        # First 2 calls should succeed
        assert api_endpoint() == "success"
        assert api_endpoint() == "success"

        # 3rd call should be blocked
        with pytest.raises(RateLimitExceeded) as exc_info:
            api_endpoint()

        error_msg = str(exc_info.value)
        assert exc_info.value.calls == 2
        assert exc_info.value.wait_time > 0
        assert "Rate limit exceeded" in error_msg
        assert "Maximum 2 calls allowed" in error_msg
        assert "Please wait" in error_msg

    def test_rate_limit_resets_after_period(self):
        """Test that @rate_limit allows calls again after the period passes."""

        @rate_limit(calls=2, period=1.0)
        def quick_function():
            return "success"

        # Use up the limit
        assert quick_function() == "success"
        assert quick_function() == "success"

        # Should be blocked now
        with pytest.raises(RateLimitExceeded):
            quick_function()

        # Wait for the period to pass
        time.sleep(1.1)

        # Should work again
        assert quick_function() == "success"

    def test_rate_limit_preserves_function_arguments(self):
        """Test that @rate_limit correctly passes arguments to the decorated function."""

        @rate_limit(calls=5, period=10.0)
        def function_with_args(a, b, c=None):
            return f"a={a}, b={b}, c={c}"

        assert function_with_args(1, 2, c=3) == "a=1, b=2, c=3"
        assert function_with_args("hello", "world") == "a=hello, b=world, c=None"
        assert function_with_args(10, 20, 30) == "a=10, b=20, c=30"

    def test_rate_limit_preserves_function_metadata(self):
        """Test that @rate_limit preserves function metadata using @functools.wraps."""

        @rate_limit(calls=3, period=60.0)
        def test_function():
            """Test function docstring."""
            return "test"

        assert test_function.__name__ == "test_function"
        assert test_function.__doc__ == "Test function docstring."

    def test_rate_limit_with_different_parameters(self):
        """Test @rate_limit with different call/period parameters."""

        @rate_limit(calls=1, period=5.0)
        def restrictive_function():
            return "success"

        assert restrictive_function() == "success"

        with pytest.raises(RateLimitExceeded):
            restrictive_function()

        @rate_limit(calls=10, period=1.0)
        def permissive_function():
            return "success"

        for _ in range(10):
            assert permissive_function() == "success"

        with pytest.raises(RateLimitExceeded):
            permissive_function()


class TestCacheDecorator:
    """Test cases for the @cache decorator."""

    def test_cache_basic_functionality(self):
        """Test basic caching functionality - same args should return cached result."""
        call_count = 0

        @cache(ttl=10.0)
        def cached_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2

        # First call should execute the function
        result1 = cached_function(5)
        assert result1 == 10
        assert call_count == 1

        # Second call with same arg should use cache
        result2 = cached_function(5)
        assert result2 == 10
        assert call_count == 1  # Should not increase

        # Call with different arg should execute function
        result3 = cached_function(10)
        assert result3 == 20
        assert call_count == 2

    def test_cache_ttl_expiration(self):
        """Test that cached results expire after TTL."""
        call_count = 0

        @cache(ttl=0.5)
        def short_ttl_function(x):
            nonlocal call_count
            call_count += 1
            return x * 3

        # First call
        result1 = short_ttl_function(5)
        assert result1 == 15
        assert call_count == 1

        # Immediate second call should use cache
        result2 = short_ttl_function(5)
        assert result2 == 15
        assert call_count == 1

        # Wait for TTL to expire
        time.sleep(0.6)

        # Should call function again
        result3 = short_ttl_function(5)
        assert result3 == 15
        assert call_count == 2

    def test_cache_with_different_arguments(self):
        """Test that cache correctly handles different function arguments."""
        call_count = 0

        @cache(ttl=10.0)
        def multi_arg_function(a, b, c=None):
            nonlocal call_count
            call_count += 1
            return f"{a}-{b}-{c}"

        # Call with different arguments
        result1 = multi_arg_function(1, 2, 3)
        assert result1 == "1-2-3"
        assert call_count == 1

        # Same args should use cache
        result2 = multi_arg_function(1, 2, 3)
        assert result2 == "1-2-3"
        assert call_count == 1

        # Different args should call function
        result3 = multi_arg_function(1, 2, 4)
        assert result3 == "1-2-4"
        assert call_count == 2

        # Same kwargs should hit cache (kwargs are treated separately from positional)
        result4 = multi_arg_function(a=1, b=2, c=3)
        assert result4 == "1-2-3"
        assert call_count == 3  # New call since kwargs differ from positional

        # But repeated kwargs should use cache
        result5 = multi_arg_function(a=1, b=2, c=3)
        assert result5 == "1-2-3"
        assert call_count == 3  # Should use cache

    def test_cache_preserves_function_metadata(self):
        """Test that @cache preserves function metadata using @functools.wraps."""

        @cache(ttl=5.0)
        def test_function():
            """Test function docstring."""
            return "test"

        assert test_function.__name__ == "test_function"
        assert test_function.__doc__ == "Test function docstring."

    def test_cache_with_mutable_arguments(self):
        """Test that cache works correctly with mutable arguments."""
        call_count = 0

        @cache(ttl=10.0)
        def function_with_list_arg(items):
            nonlocal call_count
            call_count += 1
            return sum(items)

        # Call with list
        result1 = function_with_list_arg([1, 2, 3])
        assert result1 == 6
        assert call_count == 1

        # Same list content but different list object - should hit cache
        # since lists are converted to tuples for key generation
        result2 = function_with_list_arg([1, 2, 3])
        assert result2 == 6
        assert call_count == 1  # Cache hit

        # Different list should call function
        result3 = function_with_list_arg([1, 2, 3, 4])
        assert result3 == 10
        assert call_count == 2

    def test_cache_independent_instances(self):
        """Test that different decorated functions have independent caches."""
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

        assert call_count1 == 1
        assert call_count2 == 1

        # Call again - both should use cache
        function_one(5)
        function_two(5)

        assert call_count1 == 1
        assert call_count2 == 1

    def test_cache_logs_hit_and_miss(self, caplog):
        """Test that cache logs hit and miss events."""

        @cache(ttl=10.0)
        def cached_function(x):
            return x * 2

        with caplog.at_level(logging.DEBUG):
            cached_function(5)  # Miss
            cached_function(5)  # Hit
            cached_function(10)  # Miss

        assert "Cache miss" in caplog.text
        assert "Cache hit" in caplog.text
