"""
Reference counting internals: observe refcounts, caching, and weakrefs. Knowing
refcounts helps debug leaks and understand object lifetimes. Note: CPython adds
one extra reference while inside sys.getrefcount.
"""

from __future__ import annotations

import sys
import weakref

from python_mastery.internals import (
    memory_management as _library_reference,
)  # noqa: F401


def example_basic_refcount() -> None:
    print("\nExample 1: getrefcount basics (+1 for the temp reference)")
    obj = []
    print("  initial ->", sys.getrefcount(obj))
    alias = obj
    print("  after alias ->", sys.getrefcount(obj))
    del alias
    print("  after del alias ->", sys.getrefcount(obj))


def example_function_args() -> None:
    print("\nExample 2: Passing as arg bumps refcount during call")

    def show(o):
        print("  inside call ->", sys.getrefcount(o))

    data = {"a": 1}
    print("  before call ->", sys.getrefcount(data))
    show(data)
    print("  after call ->", sys.getrefcount(data))


def example_container_refs() -> None:
    print("\nExample 3: Containers hold references")
    lst = [1, 2, 3]
    wrap = [lst, lst]
    print("  refcount with two references ->", sys.getrefcount(lst))
    del wrap
    print("  after deleting container ->", sys.getrefcount(lst))


def example_small_int_cache() -> None:
    print("\nExample 4: Small int and string interning")
    a = 5
    b = 5
    print("  small ints share object id ->", id(a) == id(b))
    s1 = "hello"
    s2 = "hello"
    print("  interned strings share id ->", id(s1) == id(s2))
    s3 = sys.intern("dynamic" + "_" + "string")
    s4 = sys.intern("dynamic_string")
    print("  manual intern ->", id(s3) == id(s4))


def example_weakref() -> None:
    print("\nExample 5: weakref does not increment refcount")

    class Widget:
        pass

    w = Widget()
    print("  before weakref ->", sys.getrefcount(w))
    ref = weakref.ref(w)
    print("  after weakref ->", sys.getrefcount(w))
    print("  deref weakref ->", ref())
    del w
    print("  after deleting strong refs ->", ref())


def example_del_statement() -> None:
    print(
        "\nExample 6: del lowers refcount but may not free immediately if other refs exist"
    )
    obj = [1, 2, 3]
    holder = obj
    print("  before del ->", sys.getrefcount(obj))
    del obj
    print("  after del original name, holder still alive ->", sys.getrefcount(holder))


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING REFERENCE COUNTING")
    print("=" * 70)

    example_basic_refcount()
    example_function_args()
    example_container_refs()
    example_small_int_cache()
    example_weakref()
    example_del_statement()

    print("\nAll refcount examples completed.")


if __name__ == "__main__":
    run_all()
