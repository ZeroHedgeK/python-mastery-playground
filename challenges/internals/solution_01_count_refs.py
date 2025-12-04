"""
Solution: count_refs

Key Insights:
1. sys.getrefcount adds a temporary reference; subtract one to report actual.
2. The object itself is not modified; only reference count is observed.

Alternative Approaches:
- ctypes can inspect refcounts, but getrefcount is simplest.
"""

from __future__ import annotations

import sys


# === SOLUTION ===


def count_refs(obj) -> int:
    return sys.getrefcount(obj) - 1


# === VERIFICATION ===


def test_counts_minus_one():
    lst = []
    before = sys.getrefcount(lst)
    expected = before - 1
    assert count_refs(lst) == expected


if __name__ == "__main__":
    test_counts_minus_one()
    print("✅ test_counts_minus_one passed")
    print("\n🎉 All tests passed!")
