"""
Challenge: vector
Difficulty: ⭐
Time Estimate: 15 minutes
Concepts: OOP, operator overloading, __repr__

Problem:
Implement a simple 2D Vector class supporting addition, subtraction, and a
readable representation.

Requirements:
1. Vector(x, y) stores x and y as floats.
2. v1 + v2 and v1 - v2 return new Vector instances.
3. __repr__ returns "Vector(x=<x>, y=<y>)".

Hints:
- Use __add__ and __sub__ for operators.
- Implement __eq__ for test comparisons.

Run tests:
    python challenges/oop/challenge_01_vector.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


class Vector:
    def __init__(self, x, y):
        raise NotImplementedError("Your implementation here")

    def __add__(self, other):
        raise NotImplementedError("Your implementation here")

    def __sub__(self, other):
        raise NotImplementedError("Your implementation here")

    def __eq__(self, other):
        raise NotImplementedError("Your implementation here")

    def __repr__(self):
        raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_add_sub_repr():
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    assert v1 + v2 == Vector(4, 6)
    assert v2 - v1 == Vector(2, 2)
    assert repr(v1) == "Vector(x=1.0, y=2.0)"


if __name__ == "__main__":
    import sys

    try:
        test_add_sub_repr()
        print("✅ test_add_sub_repr passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_add_sub_repr failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
