"""
Challenge: parallel_map
Difficulty: ⭐
Time Estimate: 15 minutes
Concepts: ThreadPoolExecutor, mapping

Problem:
Implement `parallel_map(func, iterable, max_workers=4)` that applies func to each
item using a ThreadPoolExecutor and returns a list of results preserving order.

Requirements:
1. Use ThreadPoolExecutor with the given max_workers.
2. Preserve input order in the returned list.
3. Ensure the executor is properly shut down.

Hints:
- executor.map preserves order; list(...) will realize results.

Run tests:
    python challenges/concurrency/challenge_01_parallel_map.py
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor


# === YOUR CODE HERE ===


def parallel_map(func, iterable, max_workers=4):
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_basic():
    data = [1, 2, 3]
    out = parallel_map(lambda x: x * 2, data)
    assert out == [2, 4, 6]


if __name__ == "__main__":
    import sys

    try:
        test_basic()
        print("✅ test_basic passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_basic failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
