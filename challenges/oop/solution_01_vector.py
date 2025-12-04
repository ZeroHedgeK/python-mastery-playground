"""
Solution: vector

Key Insights:
1. Implement __eq__ to allow direct comparisons in tests.
2. __add__/__sub__ should return new instances to keep objects immutable.
3. Coerce to float for consistent representation and arithmetic.

Alternative Approaches:
- Use dataclasses for boilerplate reduction.
"""

from __future__ import annotations


# === SOLUTION ===


class Vector:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return isinstance(other, Vector) and self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"


# === VERIFICATION ===


def test_add_sub_repr():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    assert v1 + v2 == Vector(4, 6)
    assert v2 - v1 == Vector(2, 2)
    assert repr(v1) == "Vector(x=1.0, y=2.0)"


if __name__ == "__main__":
    test_add_sub_repr()
    print("✅ test_add_sub_repr passed")
    print("\n🎉 All tests passed!")
