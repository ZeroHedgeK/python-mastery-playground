"""
cache_examples.py - Focused examples for the @cache decorator.

This file demonstrates the @cache decorator with clear, isolated examples.
Run this file directly to see the @cache decorator in action.
"""

import time

from decorators import cache

print("=" * 70)
print("DEMONSTRATING @cache DECORATOR")
print("=" * 70)
print()


# Example 1: Basic caching functionality
@cache(ttl=10.0)
def expensive_computation(n: int) -> int:
    """
    Simulates an expensive computation that takes time.
    """
    print(f"  → Computing for n={n} (this takes time)...")
    time.sleep(1)  # Simulate expensive operation
    result = n * n * n
    print(f"  → Computation complete: {n}³ = {result}")
    return result


print("Example 1: Basic caching functionality")
print("-" * 40)
print("First call (should compute):")
result1 = expensive_computation(5)
print(f"Result: {result1}\n")

print("Second call with same argument (should use cache):")
result2 = expensive_computation(5)
print(f"Result: {result2}\n")

print("Call with different argument (should compute):")
result3 = expensive_computation(10)
print(f"Result: {result3}\n")

print("Third call with original argument (should use cache again):")
result4 = expensive_computation(5)
print(f"Result: {result4}")
print()


# Example 2: Cache expiration (TTL)
@cache(ttl=2.0)  # Very short TTL for demonstration
def short_cache_function(x: int) -> str:
    """
    A function with short TTL to demonstrate expiration.
    """
    print(f"  → Executing function for x={x}")
    return f"Result for {x} at {time.time():.1f}"


print("Example 2: Cache expiration (TTL = 2 seconds)")
print("-" * 40)
print("First call:")
result1 = short_cache_function(42)
print(f"Result: {result1}\n")

print("Second call immediately (should use cache):")
result2 = short_cache_function(42)
print(f"Result: {result2}\n")

print("Waiting 2.5 seconds for cache to expire...")
time.sleep(2.5)

print("\nThird call after expiration (should recompute):")
result3 = short_cache_function(42)
print(f"Result: {result3}")
print()


# Example 3: Function with multiple arguments
@cache(ttl=10.0)
def multi_arg_function(a: int, b: int, c: str = "default") -> str:
    """
    A function with multiple arguments to test cache key generation.
    """
    print(f"  → Processing: a={a}, b={b}, c='{c}'")
    return f"Result: {a + b} - {c.upper()}"


print("Example 3: Function with multiple arguments")
print("-" * 40)
print("Call with positional arguments:")
result1 = multi_arg_function(1, 2, "hello")
print(f"Result: {result1}\n")

print("Same call again (should use cache):")
result2 = multi_arg_function(1, 2, "hello")
print(f"Result: {result2}\n")

print("Call with different arguments:")
result3 = multi_arg_function(1, 2, "world")
print(f"Result: {result3}\n")

print("Call with keyword arguments (different order):")
result4 = multi_arg_function(a=1, b=2, c="hello")
print(f"Result: {result4}\n")

print("Call with mixed arguments:")
result5 = multi_arg_function(1, 2, c="hello")
print(f"Result: {result5}")
print()


# Example 4: Mathematical function with caching
@cache(ttl=5.0)
def fibonacci(n: int) -> int:
    """
    Calculate Fibonacci number (with caching to speed up repeated calls).
    """
    print(f"  → Calculating Fibonacci({n})")
    if n <= 1:
        return n

    # This would be slow without caching for repeated calls
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b

    return b


print("Example 4: Fibonacci with caching")
print("-" * 40)
print("Calculating Fibonacci numbers:")
fib_sequence = [5, 8, 5, 10, 8, 5]  # Some repeats to show caching
for num in fib_sequence:
    result = fibonacci(num)
    print(f"Fibonacci({num}) = {result}")
print()

# Example 5: API simulation with caching
api_call_count = 0


@cache(ttl=8.0)
def simulate_api_call(endpoint: str, params: dict = None):
    """
    Simulates an API call that benefits from caching.
    """
    global api_call_count
    api_call_count += 1

    print(f"  → API Call #{api_call_count} to {endpoint}")
    time.sleep(0.5)  # Simulate network delay

    if params:
        return f"Data from {endpoint} with {params}"
    else:
        return f"Data from {endpoint}"


print("Example 5: API simulation with caching")
print("-" * 40)
print("Making API calls (some will be cached):")
result1 = simulate_api_call("/users/123")
print(f"Result 1: {result1}\n")

result2 = simulate_api_call("/users/123")  # Same endpoint, should cache
print(f"Result 2: {result2}\n")

result3 = simulate_api_call("/users/456")  # Different endpoint
print(f"Result 3: {result3}\n")

result4 = simulate_api_call("/users/123", {"details": "full"})  # Different params
print(f"Result 4: {result4}\n")

result5 = simulate_api_call("/users/123")  # Should use cache again
print(f"Result 5: {result5}")
print()

print("=" * 70)
print("All @cache examples completed!")
print("=" * 70)
print()
print("Key observations:")
print("  • The @cache decorator stores function results based on arguments")
print("  • Repeated calls with same args return cached results instantly")
print("  • Cache expires after the specified TTL (time-to-live)")
print("  • Perfect for expensive computations, API calls, or database queries")
print("  • Each function has its own independent cache")
print("  • Cache hit/miss messages show when caching is working")
