"""
Challenge: observable
Difficulty: ⭐⭐
Time Estimate: 15-20 minutes
Concepts: OOP, property, callbacks

Problem:
Create an Observable class whose `value` property notifies subscribed callbacks
whenever it changes (including initial set in __init__).

Requirements:
1. Subscribers are callables taking the new value.
2. Observable(value).subscribe(fn) adds a callback; multiple subscribers allowed.
3. Setting .value triggers all subscribers with the new value.

Hints:
- Store subscribers in a list; call them inside the setter.

Run tests:
    python challenges/oop/challenge_02_observable.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


class Observable:
    def __init__(self, value=None):
        raise NotImplementedError("Your implementation here")

    def subscribe(self, fn):
        raise NotImplementedError("Your implementation here")

    @property
    def value(self):
        raise NotImplementedError("Your implementation here")

    @value.setter
    def value(self, new):
        raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_notifies_on_change():
    seen = []
    obs = Observable(1)
    obs.subscribe(seen.append)
    obs.value = 2
    obs.value = 3
    assert seen == [1, 2, 3]


if __name__ == "__main__":
    import sys

    try:
        test_notifies_on_change()
        print("✅ test_notifies_on_change passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_notifies_on_change failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
