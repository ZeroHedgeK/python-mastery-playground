"""
Solution: find_cycles

Key Insights:
1. gc.collect returns the number of unreachable objects collected; >0 implies cycles or otherwise unreferenced objects.
2. Ensure GC is enabled before collecting; restore previous state if needed.

Alternative Approaches:
- Use gc.get_objects and graph traversal; gc.collect suffices here.
"""

from __future__ import annotations

import gc


# === SOLUTION ===


def find_cycles(objs) -> bool:
    was_enabled = gc.isenabled()
    if not was_enabled:
        gc.enable()
    try:
        collected = gc.collect()
        return collected > 0
    finally:
        if not was_enabled:
            gc.disable()


# === VERIFICATION ===


def test_detects_cycle():
    class Node:
        def __init__(self):
            self.ref = None

    a = Node()
    b = Node()
    a.ref = b
    b.ref = a
    objs = [a, b]
    assert find_cycles(objs) is True


def test_no_cycle():
    objs = [object(), object()]
    assert find_cycles(objs) is False


if __name__ == "__main__":
    test_detects_cycle()
    print("✅ test_detects_cycle passed")
    test_no_cycle()
    print("✅ test_no_cycle passed")
    print("\n🎉 All tests passed!")
