"""
Memory introspection: object sizes, shallow vs deep size, slots savings,
tracemalloc snapshots, and data-structure comparisons. Knowing actual sizes
helps choose the right containers for performance-sensitive code.
"""

from __future__ import annotations

import array
import sys
import tracemalloc
from dataclasses import dataclass

from python_mastery.internals import (  # noqa: F401
    memory_management as _library_reference,
)


def sizeof(label: str, obj) -> None:
    print(f"  {label:<25} -> {sys.getsizeof(obj)} bytes")


def example_basic_sizes() -> None:
    print("\nExample 1: sys.getsizeof shallow sizes")
    sizeof("empty list", [])
    sizeof("list [1,2,3]", [1, 2, 3])
    sizeof("tuple (1,2,3)", (1, 2, 3))
    sizeof("dict {}", {})
    sizeof("set {1,2,3}", {1, 2, 3})
    print("  Note: list/dict sizes exclude contents; elements live elsewhere.")


def recursive_size(obj, seen=None):
    if seen is None:
        seen = set()
    oid = id(obj)
    if oid in seen:
        return 0
    seen.add(oid)
    size = sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(
            recursive_size(k, seen) + recursive_size(v, seen) for k, v in obj.items()
        )
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(recursive_size(i, seen) for i in obj)
    return size


def example_recursive_size() -> None:
    print("\nExample 2: Recursive size vs shallow")
    obj = {"nums": [1, 2, 3], "nested": {"a": 1}}
    sizeof("shallow", obj)
    print("  deep size ->", recursive_size(obj), "bytes")


def example_slots_savings() -> None:
    print("\nExample 3: __slots__ memory savings")

    class Regular:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class Slotted:
        __slots__ = ("x", "y")

        def __init__(self, x, y):
            self.x = x
            self.y = y

    r = Regular(1, 2)
    s = Slotted(1, 2)
    sizeof("regular instance", r)
    try:
        sizeof("slotted __dict__", s.__dict__)
    except AttributeError:
        print("  slotted has no __dict__ (saves overhead)")
    sizeof("slotted instance", s)


def example_string_and_int_memory() -> None:
    print("\nExample 4: Strings and ints")
    sizeof("short string", "hi")
    sizeof("long string", "x" * 100)
    sizeof("small int 5", 5)
    sizeof("large int 10**20", 10**20)
    print("  small ints are cached; large ints grow with digit count")


def example_array_vs_list() -> None:
    print("\nExample 5: array.array vs list for numbers")
    nums = list(range(10))
    arr = array.array("I", nums)
    sizeof("list of 10 ints", nums)
    sizeof("array('I') of 10", arr)
    print("  arrays pack data tightly; lists store PyObject* pointers")


def example_tracemalloc_snapshot() -> None:
    print("\nExample 6: tracemalloc snapshot for allocations")
    tracemalloc.start()

    data = [str(i) for i in range(1000)]
    snap1 = tracemalloc.take_snapshot()
    more = [str(i) for i in range(1000, 1500)]
    snap2 = tracemalloc.take_snapshot()

    top_stats = snap2.compare_to(snap1, "filename")[:3]
    for stat in top_stats:
        print(
            f"  {stat.traceback[0].filename} +{stat.size_diff} bytes in {stat.count_diff} blocks"
        )

    # Clean up to avoid keeping refs
    del data, more
    tracemalloc.stop()


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING MEMORY INTROSPECTION")
    print("=" * 70)

    example_basic_sizes()
    example_recursive_size()
    example_slots_savings()
    example_string_and_int_memory()
    example_array_vs_list()
    example_tracemalloc_snapshot()

    print("\nAll memory introspection examples completed.")


if __name__ == "__main__":
    run_all()
