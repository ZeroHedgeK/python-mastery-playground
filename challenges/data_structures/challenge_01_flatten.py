"""
Challenge: flatten
Difficulty: ⭐
Time Estimate: 10 minutes
Concepts: recursion/iteration, lists

Problem:
Write `flatten(nested)` that flattens a list of lists of arbitrary depth into a
single list preserving order.

Requirements:
1. Accept lists containing ints or further lists.
2. Return a new flat list without mutating the input.
3. Handle empty lists correctly.

Hints:
- Recursion is straightforward; an explicit stack also works.

Run tests:
    python challenges/data_structures/challenge_01_flatten.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


def flatten(nested):
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_basic():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_deep_empty():
    assert flatten([[], [1, [2, []]], 3]) == [1, 2, 3]


if __name__ == "__main__":
    import sys

    try:
        test_basic()
        print("✅ test_basic passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_basic failed: {e}")
        sys.exit(1)

    try:
        test_deep_empty()
        print("✅ test_deep_empty passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_deep_empty failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
