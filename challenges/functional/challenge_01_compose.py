"""
Challenge: compose
Difficulty: ⭐
Time Estimate: 10 minutes
Concepts: higher-order functions

Problem:
Implement `compose(*fns)` returning a function that applies functions right-to-left.

Requirements:
1. compose(f, g)(x) == f(g(x)).
2. Support composing any number of functions.
3. Handle the case of zero functions by returning an identity function.

Hints:
- Iterate reversed(fns) inside the composed function.

Run tests:
    python challenges/functional/challenge_01_compose.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


def compose(*fns):
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_compose_two():
    double = lambda x: x * 2
    inc = lambda x: x + 1
    f = compose(double, inc)
    assert f(3) == 8


def test_identity():
    f = compose()
    assert f(5) == 5


if __name__ == "__main__":
    import sys

    try:
        test_compose_two()
        print("✅ test_compose_two passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_compose_two failed: {e}")
        sys.exit(1)

    try:
        test_identity()
        print("✅ test_identity passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_identity failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
