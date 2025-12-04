"""
Garbage collection internals: generational GC, cycles, thresholds, and hooks.
Shows how to inspect GC state, create/collect cycles, and use callbacks for
debugging. CPython-specific details (refcount + generational GC).
"""

from __future__ import annotations

import gc
import weakref

from python_mastery.internals import memory_management as _library_reference  # noqa: F401


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ref: Node | None = None

    def __repr__(self) -> str:  # pragma: no cover - display helper
        return f"Node({self.name})"


def example_gc_counts() -> None:
    print("\nExample 1: gc.get_count (per-generation stats)")
    print("  counts ->", gc.get_count())


def example_create_cycle_and_collect() -> None:
    print("\nExample 2: Create cycle and collect")
    a = Node("a")
    b = Node("b")
    a.ref = b
    b.ref = a
    wr_a = weakref.ref(a)
    wr_b = weakref.ref(b)
    del a, b
    print("  before collect, weakrefs alive ->", wr_a(), wr_b())
    collected = gc.collect()
    print(f"  gc.collect() reclaimed {collected} unreachable objects")
    print("  after collect, weakrefs ->", wr_a(), wr_b())


def example_gc_thresholds() -> None:
    print("\nExample 3: Adjusting GC thresholds (demo only)")
    old = gc.get_threshold()
    print("  current thresholds ->", old)
    gc.set_threshold(*old)
    print("  leaving thresholds unchanged (only showing API)")


def example_callbacks() -> None:
    print("\nExample 4: gc.callbacks for debug")
    events: list[str] = []

    def cb(phase, info):
        events.append(f"{phase}:{info.get('generation')}")

    gc.callbacks.append(cb)
    gc.collect()
    gc.callbacks.remove(cb)
    print("  callback events ->", events)


def example_disable_enable() -> None:
    print("\nExample 5: Temporarily disabling GC (benchmarking use case)")
    gc.disable()
    print("  gc.isenabled ->", gc.isenabled())
    gc.collect()
    gc.enable()
    print("  gc.isenabled ->", gc.isenabled())


def example_gc_garbage_and_del() -> None:
    print("\nExample 6: __del__ can complicate collection (legacy)")

    class WithDel:
        def __init__(self) -> None:
            self.ref = None

        def __del__(self):
            # Finalizers can make cycles uncollectable in old versions
            pass

    o1 = WithDel()
    o2 = WithDel()
    o1.ref = o2
    o2.ref = o1
    del o1, o2
    gc.collect()
    if gc.garbage:
        print("  objects in gc.garbage ->", gc.garbage)
        gc.garbage.clear()
    else:
        print("  no uncollectable garbage (modern CPython handles most cases)")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING GARBAGE COLLECTION")
    print("=" * 70)

    example_gc_counts()
    example_create_cycle_and_collect()
    example_gc_thresholds()
    example_callbacks()
    example_disable_enable()
    example_gc_garbage_and_del()

    print("\nAll GC examples completed.")


if __name__ == "__main__":
    run_all()
