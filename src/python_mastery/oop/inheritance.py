"""
Inheritance and MRO
==================

This module demonstrates multiple inheritance patterns and the Method Resolution Order (MRO).
It covers:
1. The Diamond Problem and how C3 Linearization solves it.
2. Mixins: Composition over Inheritance.
"""

import json


def demonstrate_mro() -> None:
    """
    Demonstrate Method Resolution Order (MRO).

    Python uses C3 Linearization to determine the order in which parent classes are searched.
    """
    print("\n=== Method Resolution Order (Diamond Problem) ===")

    class A:
        def speak(self) -> None:
            print("A speaks")

    class B(A):
        def speak(self) -> None:
            print("B speaks")
            super().speak()

    class C(A):
        def speak(self) -> None:
            print("C speaks")
            super().speak()

    # D inherits from B and C. Both inherit from A.
    class D(B, C):
        def speak(self) -> None:
            print("D speaks")
            super().speak()

    print(f"MRO for class D: {[cls.__name__ for cls in D.mro()]}")
    # Expected: D -> B -> C -> A -> object
    # C is called after B because B is listed first, but A is last because it's the common ancestor.

    print("\nCalling D().speak():")
    d = D()
    d.speak()


def demonstrate_mixins() -> None:
    """
    Demonstrate Mixins.

    Small classes that provide specific functionality to be reused across unrelated classes.
    They are not meant to be instantiated alone.
    """
    print("\n=== Mixins ===")

    class JsonMixin:
        """Adds to_json() capability to any class."""

        def to_json(self) -> str:
            # Access self.__dict__ of the child class
            return json.dumps(self.__dict__)

    class Person:
        def __init__(self, name: str, age: int) -> None:
            self.name = name
            self.age = age

    # Combine Person with JsonMixin
    class JsonPerson(JsonMixin, Person):
        pass

    p = JsonPerson("Alice", 30)
    print(f"Person as JSON: {p.to_json()}")


if __name__ == "__main__":
    demonstrate_mro()
    demonstrate_mixins()
