"""
Advanced class mechanics: singleton, properties, descriptors, __slots__, and
__init_subclass__ hooks. Includes when these are appropriate and a "wrong way"
singleton example.
"""

from __future__ import annotations

import sys

from python_mastery.oop import advanced_classes as _library_reference  # noqa: F401


def example_singleton_pattern() -> None:
    print("\nExample 1: Singleton via __new__ (use sparingly)")

    class ConfigSingleton:
        _instance = None

        def __new__(cls, value: str):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

        def __init__(self, value: str) -> None:
            self.value = value

    a = ConfigSingleton("first")
    b = ConfigSingleton("second")
    print("  a.value ->", a.value)
    print("  b.value ->", b.value)
    print("  a is b ->", a is b)
    print(
        "  wrong way: singletons hide state changes; prefer explicit injection when possible"
    )


def example_properties_with_validation() -> None:
    print("\nExample 2: @property with validation")

    class Temperature:
        def __init__(self, celsius: float) -> None:
            self._celsius = celsius

        @property
        def celsius(self) -> float:
            return self._celsius

        @celsius.setter
        def celsius(self, value: float) -> None:
            if value < -273.15:
                raise ValueError("Temperature below absolute zero")
            self._celsius = value

        @property
        def fahrenheit(self) -> float:
            return self._celsius * 9 / 5 + 32

    t = Temperature(20)
    print("  start C/F:", t.celsius, t.fahrenheit)
    t.celsius = 30
    print("  updated C/F:", t.celsius, t.fahrenheit)
    try:
        t.celsius = -300
    except ValueError as exc:
        print("  validation caught:", exc)


def example_slots_memory() -> None:
    print("\nExample 3: __slots__ saves per-instance overhead")

    class Regular:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    class Slotted:
        __slots__ = ("x", "y")

        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

    r = Regular(1, 2)
    s = Slotted(1, 2)
    print("  Regular has __dict__ size:", sys.getsizeof(r.__dict__))
    try:
        print("  Slotted __dict__:", s.__dict__)
    except AttributeError:
        print("  Slotted has no __dict__ (saves memory)")
    try:
        s.z = 5  # type: ignore[attr-defined]
    except AttributeError as exc:
        print("  cannot add new attr to slotted:", exc)


class PositiveInt:
    """Descriptor enforcing positive integers."""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{self.name} must be positive int")
        instance.__dict__[self.name] = value


def example_descriptor_usage() -> None:
    print("\nExample 4: Descriptor for validated fields")

    class InventoryItem:
        quantity = PositiveInt()

        def __init__(self, name: str, quantity: int) -> None:
            self.name = name
            self.quantity = quantity

    item = InventoryItem("widgets", 10)
    print("  item.quantity ->", item.quantity)
    try:
        item.quantity = -5
    except ValueError as exc:
        print("  validation caught:", exc)


def example_init_subclass_registry() -> None:
    print("\nExample 5: __init_subclass__ for registry and validation")

    class PluginBase:
        registry: list[type[PluginBase]] = []

        def __init_subclass__(cls, requires: tuple[str, ...] = (), **kwargs):
            super().__init_subclass__(**kwargs)
            for attr in requires:
                if not hasattr(cls, attr):
                    raise TypeError(f"Subclass must define attribute '{attr}'")
            PluginBase.registry.append(cls)

    class CsvPlugin(PluginBase, requires=("extension",)):
        extension = ".csv"

    try:

        class BrokenPlugin(PluginBase, requires=("extension",)):
            pass

    except TypeError as exc:
        print("  validation caught:", exc)

    print("  registry contains:", [cls.__name__ for cls in PluginBase.registry])


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING ADVANCED CLASS FEATURES")
    print("=" * 70)

    example_singleton_pattern()
    example_properties_with_validation()
    example_slots_memory()
    example_descriptor_usage()
    example_init_subclass_registry()

    print("\nAll advanced class examples completed.")


if __name__ == "__main__":
    run_all()
