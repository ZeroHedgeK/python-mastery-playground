"""
OOP Module
=========

This module explores Python's Object-Oriented Programming features in depth.
It covers:
- Advanced Class Mechanics (__new__, __slots__, properties)
- Inheritance Patterns (MRO, Mixins)
- Magic Methods (Operator overloading, containers)
- Metaclasses (Class creation hooks)
"""

from .advanced_classes import demonstrate_singleton, demonstrate_slots, demonstrate_properties
from .inheritance import demonstrate_mro, demonstrate_mixins
from .magic_methods import demonstrate_magic_methods
from .metaclasses import demonstrate_metaclass

__all__ = [
    "demonstrate_singleton",
    "demonstrate_slots",
    "demonstrate_properties",
    "demonstrate_mro",
    "demonstrate_mixins",
    "demonstrate_magic_methods",
    "demonstrate_metaclass",
]
