"""
timer_examples.py - Focused examples for the @timer decorator.

This file demonstrates the @timer decorator with clear, isolated examples.
Run this file directly to see the @timer decorator in action.
"""

import time

from decorators import timer

print("=" * 70)
print("DEMONSTRATING @timer DECORATOR")
print("=" * 70)
print()


# Example 1: A slow function that sleeps
@timer
def slow_function(duration: float = 1.0) -> str:
    """
    A function that simulates slow processing by sleeping.
    """
    print(f"  → Starting slow_function, will sleep for {duration} seconds...")
    time.sleep(duration)
    print("  → slow_function finished sleeping")
    return f"Slept for {duration} seconds"


print("Example 1: Slow function with sleep")
print("-" * 40)
result = slow_function(0.5)
print(f"Result: {result}")
print()


# Example 2: A fast function with calculations
@timer
def fast_function(numbers: list[int]) -> int:
    """
    A function that performs quick calculations.
    """
    print(f"  → Starting fast_function with numbers: {numbers}")
    total = sum(numbers)
    print(f"  → fast_function calculated sum: {total}")
    return total


print("Example 2: Fast function with list sum")
print("-" * 40)
result = fast_function([1, 2, 3, 4, 5])
print(f"Result: {result}")
print()


# Example 3: Mathematical computation
@timer
def compute_sum(n: int) -> int:
    """
    Calculate the sum of numbers from 1 to n using the formula n*(n+1)/2.
    """
    print(f"  → Starting compute_sum with n={n}")
    result = n * (n + 1) // 2
    print(f"  → compute_sum calculated: {result}")
    return result


print("Example 3: Mathematical computation")
print("-" * 40)
result = compute_sum(1000000)
print(f"Result: {result}")
print()


# Example 4: String processing
@timer
def process_text(text: str) -> dict:
    """
    Process a text string and return various statistics.
    """
    print(f"  → Starting process_text with text: '{text[:50]}...'")
    time.sleep(0.1)  # Small delay to make it measurable

    stats = {
        "length": len(text),
        "words": len(text.split()),
        "uppercase": sum(1 for c in text if c.isupper()),
        "lowercase": sum(1 for c in text if c.islower()),
        "digits": sum(1 for c in text if c.isdigit()),
    }

    print(f"  → process_text completed: {stats}")
    return stats


print("Example 4: Text processing")
print("-" * 40)
result = process_text("Hello World! This is a test string with numbers 123.")
print(f"Result: {result}")
print()


# Example 5: Function with default arguments
@timer
def greet(name: str = "World", greeting: str = "Hello") -> str:
    """
    A simple greeting function to show decorators work with defaults.
    """
    print(f"  → Starting greet with '{greeting}, {name}!'")
    message = f"{greeting}, {name}!"
    return message


print("Example 5: Function with default arguments")
print("-" * 40)
result1 = greet("Alice")
print(f"Result 1: {result1}")

result2 = greet("Bob", "Hi")
print(f"Result 2: {result2}")

result3 = greet()  # Using defaults
print(f"Result 3: {result3}")
print()


# Example 6: For comparison - function without decorator
def regular_function() -> str:
    """
    A regular function without the @timer decorator for comparison.
    """
    print("  → Starting regular_function (no decorator)")
    time.sleep(0.2)
    print("  → regular_function completed")
    return "Done"


print("Example 6: Function WITHOUT @timer decorator (for comparison)")
print("-" * 40)
result = regular_function()
print(f"Result: {result}")
print()

print("=" * 70)
print("All @timer examples completed!")
print("=" * 70)
print()
print("Key observations:")
print("  • The @timer decorator measures execution time automatically")
print("  • It works with any function regardless of arguments")
print("  • It preserves the original function's return value")
print("  • It adds timing information without changing function behavior")
