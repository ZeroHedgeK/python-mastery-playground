"""
Tests for Internals Module
"""

import gc
import sys

import pytest
from internals.bytecode_inspector import example_function
from internals.memory_management import demonstrate_garbage_collection


def test_bytecode_function_output():
    """
    Verify the function we inspect actually works correctly.
    """
    assert example_function(10, 20) == 60


def test_gc_collection():
    """
    Verify that we can trigger GC manually.
    """

    # Create some garbage
    class Trash:
        pass

    t1 = Trash()
    t2 = Trash()
    t1.ref = t2
    t2.ref = t1
    del t1
    del t2

    collected = gc.collect()
    # We can't assert the exact number because other tests might leave trash,
    # but it should return an integer >= 0
    assert isinstance(collected, int)
    assert collected >= 0
