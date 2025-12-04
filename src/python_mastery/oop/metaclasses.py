"""
Metaclasses
==========

Metaclasses are "classes of classes". They define how a class is created.
They are powerful tools for framework authors to enforce rules or inject behavior.
"""

from typing import Any


def demonstrate_metaclass() -> None:
    """
    Demonstrate a simple metaclass that enforces coding standards.

    Here, it ensures all class attributes are uppercase.
    """
    print("\n=== Metaclasses ===")

    class EnforceUppercaseAttributes(type):
        """Metaclass to ensure all non-callable attributes are uppercase."""

        def __new__(
            mcs,
            name: str,
            bases: tuple[type, ...],
            attrs: dict[str, Any],
        ) -> type:
            print(f"Metaclass creating class: {name}")

            new_attrs: dict[str, Any] = {}
            for key, value in attrs.items():
                if not key.startswith("__") and not callable(value):
                    if not key.isupper():
                        raise TypeError(f"Attribute '{key}' must be uppercase!")
                new_attrs[key] = value

            return super().__new__(mcs, name, bases, new_attrs)

    print("Defining ValidClass...")

    class ValidClass(metaclass=EnforceUppercaseAttributes):
        CONFIG_VALUE = 100  # This is valid

    print("ValidClass defined successfully.")

    print("Defining InvalidClass...")
    try:

        class InvalidClass(metaclass=EnforceUppercaseAttributes):
            config_value = 100  # This will raise TypeError

    except TypeError as e:
        print(f"Caught expected error: {e}")

    # Suppress unused variable warning
    _ = ValidClass


if __name__ == "__main__":
    demonstrate_metaclass()
