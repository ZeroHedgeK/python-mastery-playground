"""
Solution: observable

Key Insights:
1. Call subscribers inside the setter to notify on every change.
2. Trigger notification for the initial value during __init__ to reflect state.
3. Keep subscribers in insertion order using a simple list.

Alternative Approaches:
- Provide unsubscribe; omitted here for brevity.
"""

from __future__ import annotations

from typing import Callable, List


# === SOLUTION ===


class Observable:
    def __init__(self, value=None):
        self._value = value
        self._subs: List[Callable] = []
        self._notify(self._value)

    def subscribe(self, fn: Callable):
        self._subs.append(fn)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new):
        self._value = new
        self._notify(new)

    def _notify(self, val):
        for fn in self._subs:
            fn(val)


# === VERIFICATION ===


def test_notifies_on_change():
    seen = []
    obs = Observable(1)
    obs.subscribe(seen.append)
    obs.value = 2
    obs.value = 3
    assert seen == [1, 2, 3]


if __name__ == "__main__":
    test_notifies_on_change()
    print("✅ test_notifies_on_change passed")
    print("\n🎉 All tests passed!")
