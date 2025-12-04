"""
Challenge: curry
Difficulty: ⭐⭐
Time Estimate: 15 minutes
Concepts: decorators, partial application

Problem:
Implement a decorator `curry` that transforms a function of N positional args
into a chain of single-argument calls until all args are provided.

Requirements:
1. curry should work for any number of positional-only arguments.
2. When enough args are supplied, call the original function and return result.
3. Support calling with multiple args at once (e.g., f(1)(2,3)).

Hints:
- Track collected args in a closure; return a function expecting the rest.

Run tests:
    python challenges/functional/challenge_02_curry.py
"""

from __future__ import annotations

from functools import wraps
from inspect import signature


# === YOUR CODE HERE ===


def curry(fn):
    @wraps(fn)
    def curried(*args):
        raise NotImplementedError("Your implementation here")

    return curried


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_basic():
    @curry
    def add3(a, b, c):
        return a + b + c

    assert add3(1)(2)(3) == 6
    assert add3(1, 2)(3) == 6


if __name__ == "__main__":
    import sys

    try:
        test_basic()
        print("✅ test_basic passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_basic failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
