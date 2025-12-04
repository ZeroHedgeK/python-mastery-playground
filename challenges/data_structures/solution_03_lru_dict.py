"""
Solution: lru_dict

Key Insights:
1. OrderedDict.move_to_end tracks recency on both get and set.
2. When exceeding max_size, popitem(last=False) evicts the least recent entry.
3. Separate get/set methods make intent explicit without subclassing dict.

Alternative Approaches:
- Subclass OrderedDict and override __getitem__/__setitem__.
- Use a deque plus dict for manual tracking.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any


# === SOLUTION ===


class LRUDict:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self._data: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key, default=None):
        if key not in self._data:
            return default
        value = self._data.pop(key)
        self._data[key] = value  # move to end
        return value

    def set(self, key, value):
        if key in self._data:
            self._data.pop(key)
        self._data[key] = value
        if len(self._data) > self.max_size:
            self._data.popitem(last=False)


# === VERIFICATION ===


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
    test_basic_set_get()
    print("✅ test_basic_set_get passed")
    test_eviction_order()
    print("✅ test_eviction_order passed")
    print("\n🎉 All tests passed!")
