"""
rate_limit_examples.py - Focused examples for the @rate_limit decorator.

This file demonstrates the @rate_limit decorator with clear, isolated examples.
Run this file directly to see the @rate_limit decorator in action.
"""

import time

from python_mastery.decorators import rate_limit

print("=" * 70)
print("DEMONSTRATING @rate_limit DECORATOR")
print("=" * 70)
print()


# Example 1: API calls with rate limiting
@rate_limit(calls=3, period=10.0)
def api_call(endpoint: str):
    """
    Simulates an API call with rate limiting.
    """
    print(f"  → Calling API endpoint: {endpoint}")
    time.sleep(0.1)  # Simulate network delay
    return f"Response from {endpoint}"


print("Example 1: API calls with rate limit (3 calls per 10 seconds)")
print("-" * 55)
for i in range(5):
    try:
        print(f"\n--- API Call #{i + 1} ---")
        result = api_call(f"/api/endpoint/{i + 1}")
        print(f"Success: {result}")
    except RuntimeError as e:
        print(f"Rate limited: {e}")
        print("Stopping further attempts...")
        break
print()


# Example 2: Database queries with rate limiting
@rate_limit(calls=2, period=5.0)
def database_query(query: str):
    """
    Simulates a database query with rate limiting.
    """
    print(f"  → Executing database query: {query}")
    time.sleep(0.05)  # Simulate query execution
    return f"Results for: {query}"


print("Example 2: Database queries with rate limit (2 calls per 5 seconds)")
print("-" * 55)
for i in range(4):
    try:
        print(f"\n--- Database Query #{i + 1} ---")
        result = database_query(f"SELECT * FROM table WHERE id={i + 1}")
        print(f"Success: {result}")
    except RuntimeError as e:
        print(f"Rate limited: {e}")
        print("Stopping further attempts...")
        break
print()

# Example 3: Rapid successive calls
print("Example 3: Rapid successive calls (3 quick API calls)")
print("-" * 55)
successful_calls = 0
for i in range(3):
    try:
        print(f"\n--- Quick Call #{i + 1} ---")
        result = api_call(f"/api/quick/{i + 1}")
        print(f"Call {i + 1}: Success")
        successful_calls += 1
    except RuntimeError as e:
        print(f"Call {i + 1}: Rate limited - {e}")

print(f"\nSuccessful calls: {successful_calls}/3")
print()

# Example 4: Rate limit reset over time
print("Example 4: Demonstrating rate limit reset over time")
print("-" * 55)
print("Making 3 API calls to use up the limit...")

# Use up the rate limit
for i in range(3):
    try:
        result = api_call(f"/api/initial/{i + 1}")
        print(f"  Call {i + 1}: Success")
    except RuntimeError as e:
        print(f"  Call {i + 1}: Rate limited - {e}")

print("\nWaiting 11 seconds for rate limit to reset...")
time.sleep(11)

print("\nMaking 3 more API calls after reset:")
for i in range(3):
    try:
        print(f"\n--- Post-reset Call #{i + 1} ---")
        result = api_call(f"/api/after-reset/{i + 1}")
        print(f"Success: {result}")
    except RuntimeError as e:
        print(f"Rate limited: {e}")
        break
print()


# Example 5: Different rate limit parameters
@rate_limit(calls=1, period=3.0)  # Very restrictive: 1 call per 3 seconds
def restrictive_api():
    """
    A very restrictive API that only allows 1 call per 3 seconds.
    """
    print("  → Making restrictive API call...")
    return "Restrictive API response"


print("Example 5: Very restrictive rate limit (1 call per 3 seconds)")
print("-" * 55)
print("First call (should succeed):")
try:
    result = restrictive_api()
    print(f"Success: {result}")
except RuntimeError as e:
    print(f"Rate limited: {e}")

print("\nSecond call immediately after (should fail):")
try:
    result = restrictive_api()
    print(f"Success: {result}")
except RuntimeError as e:
    print(f"Rate limited: {e}")

print("\nWaiting 3.5 seconds...")
time.sleep(3.5)

print("\nThird call after waiting (should succeed):")
try:
    result = restrictive_api()
    print(f"Success: {result}")
except RuntimeError as e:
    print(f"Rate limited: {e}")
print()

print("=" * 70)
print("All @rate_limit examples completed!")
print("=" * 70)
print()
print("Key observations:")
print(
    "  • The @rate_limit decorator prevents functions from being called too frequently"
)
print("  • You can configure the number of calls allowed per time period")
print("  • It's perfect for API rate limiting and preventing server overload")
print("  • The limit automatically resets after the specified time period")
print("  • Thread-safe implementation using locks")
