"""
Memory Management
================

Python uses Reference Counting as its primary mechanism, supplemented by
Generational Garbage Collection to detect reference cycles.
"""

import gc
import sys


def demonstrate_ref_counting() -> None:
    """
    Demonstrate reference counting using sys.getrefcount().

    Note: Passing the object to getrefcount() increases the count by 1 temporarily!
    """
    print("\n=== Reference Counting ===")

    # Create a string object
    a = "Hello Python Internals"
    print(f"Initial ref count for 'a': {sys.getrefcount(a)}")

    # Create another reference
    b = a
    print(f"After 'b = a': {sys.getrefcount(a)}")

    # Delete one reference
    del b
    print(f"After 'del b': {sys.getrefcount(a)}")


def demonstrate_garbage_collection() -> None:
    """
    Demonstrate Reference Cycles and the GC module.

    Ref counting fails when two objects reference each other (cycle).
    The Cyclic GC handles this.
    """
    print("\n=== Garbage Collection (Cycles) ===")

    class Node:
        """Simple node class for demonstrating reference cycles."""

        def __init__(self, name: str) -> None:
            self.name = name
            self.link: Node | None = None

        def __repr__(self) -> str:
            return f"Node({self.name})"

    # Disable GC to show the leak first (optional, but educational)
    # Use try/finally to ensure GC is always re-enabled
    gc.disable()
    try:
        # Create a cycle: A -> B -> A
        node_a = Node("A")
        node_b = Node("B")
        node_a.link = node_b
        node_b.link = node_a

        print("Created cycle: A <-> B")

        # Verify they exist in memory
        # We use id() to track them
        id_a = id(node_a)
        id_b = id(node_b)

        # Delete stack references
        del node_a
        del node_b
        print("Deleted references. Cycle remains in memory (unreachable).")

        # Force Collection
        print("Running GC manually...")
        collected = gc.collect()
        print(f"GC collected {collected} objects.")

        # Suppress unused variable warnings (educational demonstration)
        _ = (id_a, id_b)

    finally:
        # Always re-enable GC
        gc.enable()


if __name__ == "__main__":
    demonstrate_ref_counting()
    demonstrate_garbage_collection()
