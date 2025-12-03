"""
Immutability & Pure Functions
============================

Functional programming relies on:
1. Immutability: Data that cannot change after creation.
2. Pure Functions: Output depends ONLY on input; no side effects.
"""

from dataclasses import dataclass
from typing import List

# 1. Immutability with Dataclasses
@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float

    def move(self, dx, dy, dz) -> 'Point3D':
        """
        Since we can't modify self, we return a NEW instance.
        This is the functional way.
        """
        return Point3D(self.x + dx, self.y + dy, self.z + dz)

def demonstrate_frozen_dataclass():
    print("\n=== Immutable Data Structures ===")

    p1 = Point3D(1, 2, 3)
    print(f"Original: {p1}")

    try:
        p1.x = 10  # This raises FrozenInstanceError
    except Exception as e:
        print(f"Caught error modifying frozen object: {e}")

    p2 = p1.move(1, 1, 1)
    print(f"Moved (New Object): {p2}")
    print(f"Original is still: {p1}")


# 2. Pure Functions vs Impure Functions

def impure_function(data: List[int]):
    """Modifies the input list (Side Effect). BAD for FP."""
    data.append(999)
    return data

def pure_function(data: List[int], new_item: int) -> List[int]:
    """
    Returns a NEW list with the item added.
    Does NOT modify the original input.
    """
    return data + [new_item]

def demonstrate_purity():
    print("\n=== Pure vs Impure Functions ===")

    original = [1, 2, 3]

    # Pure
    new_list = pure_function(original, 4)
    print(f"Pure Result: {new_list}")
    print(f"Original after pure: {original} (Unchanged!)")

    # Impure
    impure_function(original)
    print(f"Original after impure: {original} (CHANGED!)")

if __name__ == "__main__":
    demonstrate_frozen_dataclass()
    demonstrate_purity()

