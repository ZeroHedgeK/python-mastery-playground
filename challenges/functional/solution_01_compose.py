"""
Solution: compose

Key Insights:
1. Reduce right-to-left by iterating reversed function list.
2. Returning identity when no functions are given keeps API predictable.
3. Inner function captures *fns via closure.

Alternative Approaches:
- Use functools.reduce; explicit loop is clear.
"""

from __future__ import annotations

from typing import Callable, Any


# === SOLUTION ===


def compose(*fns: Callable) -> Callable:
    if not fns:
        return lambda x: x

    def inner(value: Any):
        result = value
        for fn in reversed(fns):
            result = fn(result)
        return result

    return inner


# === VERIFICATION ===


def test_compose_two():
    double = lambda x: x * 2
    inc = lambda x: x + 1
    f = compose(double, inc)
    assert f(3) == 8


def test_identity():
    f = compose()
    assert f(5) == 5


if __name__ == "__main__":
    test_compose_two()
    print("✅ test_compose_two passed")
    test_identity()
    print("✅ test_identity passed")
    print("\n🎉 All tests passed!")
