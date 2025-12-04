"""
Challenge: find_cycles
Difficulty: ⭐⭐
Time Estimate: 20 minutes
Concepts: gc, referential cycles

Problem:
Detect objects that participate in reference cycles given a list of objects.
For this exercise, return True if any object is unreachable until gc.collect()
is called (i.e., gc collects something), else False.

Requirements:
1. Call gc.collect() and check if it collected > 0 objects.
2. Should not raise on arbitrary inputs.
3. Must enable gc if disabled.

Hints:
- gc.isenabled and gc.collect are key.

Run tests:
    python challenges/internals/challenge_02_find_cycles.py
"""

from __future__ import annotations

import gc


# === YOUR CODE HERE ===


def find_cycles(objs) -> bool:
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_detects_cycle():
    class Node:
        def __init__(self):
            self.ref = None

    a = Node()
    b = Node()
    a.ref = b
    b.ref = a
    objs = [a, b]
    assert find_cycles(objs) is True


def test_no_cycle():
    objs = [object(), object()]
    assert find_cycles(objs) is False


if __name__ == "__main__":
    import sys

    try:
        test_detects_cycle()
        print("✅ test_detects_cycle passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_detects_cycle failed: {e}")
        sys.exit(1)

    try:
        test_no_cycle()
        print("✅ test_no_cycle passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_no_cycle failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
