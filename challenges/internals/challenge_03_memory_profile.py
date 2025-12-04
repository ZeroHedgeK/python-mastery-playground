"""
Challenge: memory_profile
Difficulty: ⭐⭐⭐
Time Estimate: 25 minutes
Concepts: decorators, tracemalloc, profiling

Problem:
Implement a decorator `memory_profile` that measures peak memory usage of a
function using tracemalloc and returns a tuple (result, peak_bytes).

Requirements:
1. Start/stop tracemalloc inside the decorator.
2. After function runs, get peak from tracemalloc.get_traced_memory()[1].
3. Preserve function metadata with functools.wraps.

Hints:
- Ensure tracemalloc.stop() runs in finally to avoid leaking tracing state.

Run tests:
    python challenges/internals/challenge_03_memory_profile.py
"""

from __future__ import annotations

import tracemalloc
from functools import wraps


# === YOUR CODE HERE ===


def memory_profile(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        raise NotImplementedError("Your implementation here")

    return wrapper


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_reports_peak():
    @memory_profile
    def allocate(n):
        return [0] * n

    result, peak = allocate(1000)
    assert len(result) == 1000
    assert peak > 0


if __name__ == "__main__":
    import sys

    try:
        test_reports_peak()
        print("✅ test_reports_peak passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_reports_peak failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
