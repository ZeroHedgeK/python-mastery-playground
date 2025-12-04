"""
Solution: group_by

Key Insights:
1. dict.setdefault keeps code concise while preserving insertion order in Python 3.7+.
2. Avoid mutating inputs; build a new dictionary.
3. Call key_func once per item to prevent double work.

Alternative Approaches:
- collections.defaultdict(list) with a simple loop.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List


# === SOLUTION ===


def group_by(items, key_func: Callable[[Any], Any]) -> Dict[Any, List[Any]]:
    grouped: Dict[Any, List[Any]] = {}
    for item in items:
        key = key_func(item)
        grouped.setdefault(key, []).append(item)
    return grouped


# === VERIFICATION ===


def test_groups_numbers():
    data = [1, 2, 3, 4, 5]
    grouped = group_by(data, lambda x: "even" if x % 2 == 0 else "odd")
    assert grouped == {"odd": [1, 3, 5], "even": [2, 4]}


def test_order_preserved():
    data = ["apple", "apricot", "banana", "blueberry"]
    grouped = group_by(data, lambda s: s[0])
    assert list(grouped.keys()) == ["a", "b"]


if __name__ == "__main__":
    test_groups_numbers()
    print("✅ test_groups_numbers passed")
    test_order_preserved()
    print("✅ test_order_preserved passed")
    print("\n🎉 All tests passed!")
