"""
Reduce/fold patterns: accumulators, initializers, data structure building, and
when to prefer clearer loops. Includes loop equivalents for each reduce use.
"""

from __future__ import annotations

import functools
import operator
from typing import Iterable

from python_mastery.functional import (
    functional_tools as _library_reference,
)  # noqa: F401


def example_basic_reduce() -> None:
    print("\nExample 1: Basic sums/products with reduce")
    nums = [1, 2, 3, 4]
    total = functools.reduce(operator.add, nums, 0)
    product = functools.reduce(operator.mul, nums, 1)
    print(f"  nums={nums}, sum={total}, product={product}")
    # Loop equivalent:
    # total = 0
    # for n in nums:
    #     total += n


def example_string_concat() -> None:
    print("\nExample 2: String concat with initializer")
    words = ["hello", "world"]
    joined = functools.reduce(lambda acc, w: acc + " " + w, words, "")
    print("  joined ->", joined.strip())
    # Loop equivalent in comments to show readability tradeoff.


def example_build_dict() -> None:
    print("\nExample 3: Building dict via reduce")
    pairs = [("a", 1), ("b", 2)]

    def to_dict(acc: dict, pair: tuple[str, int]):
        key, val = pair
        acc[key] = val
        return acc

    result = functools.reduce(to_dict, pairs, {})
    print("  dict ->", result)
    # Loop equivalent:
    # acc = {}
    # for key, val in pairs:
    #     acc[key] = val


def example_flatten() -> None:
    print("\nExample 4: Flatten nested lists with reduce")
    nested = [[1, 2], [3], [4, 5]]
    flat = functools.reduce(lambda acc, xs: acc + xs, nested, [])
    print("  flat ->", flat)
    # Loop equivalent uses extend in a for-loop.


def example_accumulate_running_totals() -> None:
    print("\nExample 5: Running totals via itertools.accumulate")
    import itertools

    data = [10, 20, -5]
    running = list(itertools.accumulate(data))
    print("  data ->", data)
    print("  running totals ->", running)


def example_reduce_composition() -> None:
    print("\nExample 6: Reduce for function composition (f ∘ g ∘ h)")

    def compose(f, g):
        return lambda x: f(g(x))

    funcs = [str.strip, int, lambda n: n * 2]
    pipeline = functools.reduce(compose, funcs)
    raw = " 21 "
    print("  pipeline(' 21 ') ->", pipeline(raw))
    # Loop equivalent would manually nest calls.


def example_any_all_with_reduce() -> None:
    print("\nExample 7: Recreating any/all with reduce (for illustration)")
    flags = [False, False, True]
    any_result = functools.reduce(lambda acc, x: acc or x, flags, False)
    all_result = functools.reduce(lambda acc, x: acc and x, flags, True)
    print("  any ->", any_result, "(built-in any() is clearer)")
    print("  all ->", all_result, "(built-in all() is clearer)")


def example_real_world_aggregate() -> None:
    print("\nExample 8: Aggregating records (total revenue)")
    orders = [
        {"id": 1, "total": 50.0},
        {"id": 2, "total": 75.5},
        {"id": 3, "total": 10.0},
    ]

    total = functools.reduce(lambda acc, order: acc + order["total"], orders, 0.0)
    print("  revenue ->", total)
    # Loop equivalent would sum in a for-loop; reduce is concise but be mindful of readability.


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING REDUCE/FOLDS")
    print("=" * 70)

    example_basic_reduce()
    example_string_concat()
    example_build_dict()
    example_flatten()
    example_accumulate_running_totals()
    example_reduce_composition()
    example_any_all_with_reduce()
    example_real_world_aggregate()

    print("\nAll reduce examples completed. Prefer loops when they read better.")


if __name__ == "__main__":
    run_all()
