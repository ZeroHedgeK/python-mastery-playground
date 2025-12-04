"""
Advanced Class Mechanics
=======================

This module demonstrates advanced features of Python classes:
1. __new__ vs __init__: The Singleton Pattern
2. __slots__: Memory Optimization
3. @property: Managed Attributes
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self


def demonstrate_singleton() -> None:
    """
    Demonstrate __new__ to create a Singleton.

    __new__ is the actual constructor that creates the instance.
    __init__ is just the initializer.
    """
    print("\n=== Singleton Pattern (__new__) ===")

    class Singleton:
        _instance: Self | None = None

        def __new__(cls, *args: Any, **kwargs: Any) -> Self:
            if cls._instance is None:
                print("Creating new instance...")
                cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self, value: str) -> None:
            # Note: __init__ is called every time you call the class!
            self.value = value

    s1 = Singleton("First")
    print(f"s1 value: {s1.value}")

    s2 = Singleton("Second")
    print(f"s2 value: {s2.value}")

    print(f"s1 value is now: {s1.value} (because s1 and s2 are the SAME object)")
    print(f"s1 is s2: {s1 is s2}")


def demonstrate_slots() -> None:
    """
    Demonstrate __slots__ for memory optimization.

    By default, Python objects use a dict to store attributes (allows dynamic addition).
    __slots__ tells Python to reserve space for specific attributes only, saving RAM.
    """
    print("\n=== __slots__ (Memory Optimization) ===")

    class RegularPoint:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    class SlottedPoint:
        __slots__ = ["x", "y"]

        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    p1 = RegularPoint(1, 2)
    p2 = SlottedPoint(1, 2)

    print(f"Regular dict size: {sys.getsizeof(p1.__dict__)} bytes + object overhead")

    try:
        print(f"Slotted dict: {p2.__dict__}")  # type: ignore[attr-defined]
    except AttributeError:
        print("Slotted object has NO __dict__ (saves memory!)")

    # You can add new attributes to RegularPoint
    p1.z = 3  # type: ignore[attr-defined]
    print("Added p1.z successfully")

    # You CANNOT add new attributes to SlottedPoint
    try:
        p2.z = 3  # type: ignore[attr-defined]
    except AttributeError as e:
        print(f"Failed to add p2.z: {e}")


def demonstrate_properties() -> None:
    """
    Demonstrate @property for attribute management.

    Allows validation logic when getting/setting values.
    """
    print("\n=== @property (Managed Attributes) ===")

    class BankAccount:
        def __init__(self, balance: float) -> None:
            self._balance = balance  # "Private" attribute

        @property
        def balance(self) -> float:
            """Getter for balance."""
            print("Accessing balance...")
            return self._balance

        @balance.setter
        def balance(self, value: float) -> None:
            """Setter with validation."""
            if value < 0:
                raise ValueError("Balance cannot be negative!")
            print(f"Setting balance to {value}")
            self._balance = value

    account = BankAccount(100)

    # Uses getter
    print(f"Current: {account.balance}")

    # Uses setter
    account.balance = 200

    # Validation
    try:
        account.balance = -50
    except ValueError as e:
        print(f"Validation caught: {e}")


if __name__ == "__main__":
    demonstrate_singleton()
    demonstrate_slots()
    demonstrate_properties()
