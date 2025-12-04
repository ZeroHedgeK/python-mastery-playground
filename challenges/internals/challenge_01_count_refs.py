"""
Challenge: count_refs
Difficulty: ⭐
Time Estimate: 10-15 minutes
Concepts: sys.getrefcount, reference counting

Problem:
Implement `count_refs(obj)` that returns sys.getrefcount(obj) minus one (to
exclude the temporary reference used by getrefcount itself).

Requirements:
1. Use sys.getrefcount.
2. Return an int that is one less than getrefcount output.
3. Do not mutate the object.

Hints:
- sys.getrefcount temporarily adds a reference.

Run tests:
    python challenges/internals/challenge_01_count_refs.py
"""

from __future__ import annotations

import sys


# === YOUR CODE HERE ===


def count_refs(obj) -> int:
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_counts_minus_one():
    lst = []
    before = sys.getrefcount(lst)
    expected = before - 1
    assert count_refs(lst) == expected


if __name__ == "__main__":
    import sys

    try:
        test_counts_minus_one()
        print("✅ test_counts_minus_one passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_counts_minus_one failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
