"""
Challenge: lru_dict
Difficulty: ⭐⭐⭐
Time Estimate: 20-25 minutes
Concepts: dict subclassing, OrderedDict, eviction policy

Problem:
Implement an LRU-like dictionary with a fixed max_size. On set, if the key
already exists, update and mark it as most-recent. If inserting exceeds max_size,
evict the least recently used item.

Requirements:
1. Provide `get(key, default=None)` and `set(key, value)` methods.
2. Accessing an existing key should mark it as most recent.
3. Evict oldest entry when size would exceed max_size.

Hints:
- collections.OrderedDict has move_to_end and popitem(last=False).

Run tests:
    python challenges/data_structures/challenge_03_lru_dict.py
"""

from __future__ import annotations

from collections import OrderedDict


# === YOUR CODE HERE ===


class LRUDict:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self._data = OrderedDict()

    def get(self, key, default=None):
        raise NotImplementedError("Your implementation here")

    def set(self, key, value):
        raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_basic_set_get():
    cache = LRUDict(2)
    cache.set("a", 1)
    assert cache.get("a") == 1


def test_eviction_order():
    cache = LRUDict(2)
    cache.set("a", 1)
    cache.set("b", 2)
    cache.get("a")  # a becomes most recent
    cache.set("c", 3)  # should evict b
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3


if __name__ == "__main__":
    import sys

    try:
        test_basic_set_get()
        print("✅ test_basic_set_get passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_basic_set_get failed: {e}")
        sys.exit(1)

    try:
        test_eviction_order()
        print("✅ test_eviction_order passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_eviction_order failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
