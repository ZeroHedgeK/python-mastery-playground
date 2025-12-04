"""
Challenge: mock_time
Difficulty: ⭐
Time Estimate: 10-15 minutes
Concepts: context managers, monkeypatching

Problem:
Create a context manager `mock_time(fixed)` that temporarily overrides
time.time() to return a fixed value during the context.

Requirements:
1. Restore the original time.time after exit, even on exception.
2. Should be used as `with mock_time(123): time.time() -> 123`.
3. Do not rely on external libraries.

Hints:
- Save original time.time; assign a lambda returning fixed.

Run tests:
    python challenges/testing/challenge_01_mock_time.py
"""

from __future__ import annotations

import time
from contextlib import contextmanager


# === YOUR CODE HERE ===


@contextmanager
def mock_time(fixed: float):
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_mock_time():
    before = time.time()
    with mock_time(123.0):
        assert time.time() == 123.0
    assert time.time() >= before


if __name__ == "__main__":
    import sys

    try:
        test_mock_time()
        print("✅ test_mock_time passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_mock_time failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
