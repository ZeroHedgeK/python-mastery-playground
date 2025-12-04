"""
Solution: flatten

Key Insights:
1. Recursing on list elements and extending the result preserves order.
2. Avoid mutating the input; build a new output list.
3. Base case: non-list items append directly.

Alternative Approaches:
- Use an explicit stack to avoid recursion depth concerns.
"""

from __future__ import annotations

from typing import List, Any


# === SOLUTION ===


def flatten(nested) -> List[Any]:
    out: List[Any] = []

    for item in nested:
        if isinstance(item, list):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


# === VERIFICATION ===


def test_basic():
    assert flatten([1, [2, 3], 4]) == [1, 2, 3, 4]


def test_deep_empty():
    assert flatten([[], [1, [2, []]], 3]) == [1, 2, 3]


if __name__ == "__main__":
    test_basic()
    print("✅ test_basic passed")
    test_deep_empty()
    print("✅ test_deep_empty passed")
    print("\n🎉 All tests passed!")
