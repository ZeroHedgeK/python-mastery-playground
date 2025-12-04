"""
Tests for Functional Module
"""

from functools import partial, reduce

import pytest
from python_mastery.functional.immutability import Point3D, pure_function


def test_pure_function():
    """Ensure the pure function does not modify the input."""
    original = [1, 2, 3]
    result = pure_function(original, 4)

    assert result == [1, 2, 3, 4]
    assert original == [1, 2, 3]  # Must remain unchanged


def test_frozen_dataclass():
    """Ensure FrozenInstanceError is raised on modification."""
    p = Point3D(1, 2, 3)

    # Reading is fine
    assert p.x == 1

    # Writing raises error
    with pytest.raises(Exception):  # FrozenInstanceError is a subclass of Exception
        p.x = 10

    # Move returns new object
    p2 = p.move(1, 1, 1)
    assert p2.x == 2
    assert p.x == 1  # Original unchanged


def test_partial_application():
    """Test functools.partial logic."""

    def add(a, b):
        return a + b

    add_five = partial(add, 5)
    assert add_five(10) == 15


def test_reduce_logic():
    """Test functools.reduce logic."""
    numbers = [1, 2, 3, 4]
    # Sum
    total = reduce(lambda x, y: x + y, numbers)
    assert total == 10
