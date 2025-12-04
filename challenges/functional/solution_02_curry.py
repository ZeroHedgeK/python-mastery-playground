"""
Solution: curry

Key Insights:
1. Use signature to know how many positional parameters are expected.
2. Collect args incrementally; when enough are present, call the original.
3. Return another curried function when args are still missing.

Alternative Approaches:
- Use functools.partial; here we demonstrate manual accumulation.
"""

from __future__ import annotations

from functools import wraps
from inspect import signature
from typing import Any, Callable


# === SOLUTION ===


def curry(fn: Callable) -> Callable:
    arity = len(signature(fn).parameters)

    @wraps(fn)
    def curried(*args: Any):
        if len(args) >= arity:
            return fn(*args)

        def next_call(*more):
            return curried(*args, *more)

        return next_call

    return curried


# === VERIFICATION ===


def test_basic():
    @curry
    def add3(a, b, c):
        return a + b + c

    assert add3(1)(2)(3) == 6
    assert add3(1, 2)(3) == 6


if __name__ == "__main__":
    test_basic()
    print("✅ test_basic passed")
    print("\n🎉 All tests passed!")
