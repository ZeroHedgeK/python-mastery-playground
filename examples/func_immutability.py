"""
Immutability and pure functions: frozen dataclasses, namedtuples, immutable
collections, and isolating side effects. Shows how purity improves testability
and predictability.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, replace
from typing import NamedTuple

from python_mastery.functional import immutability as _library_reference  # noqa: F401


def pure_increment(values: list[int]) -> list[int]:
    """Pure: returns new list, does not mutate input."""
    return [v + 1 for v in values]


hidden_state = {"count": 0}


def impure_increment(values: list[int]) -> list[int]:
    """Impure: touches global hidden_state making tests order-dependent."""
    hidden_state["count"] += 1
    for i in range(len(values)):
        values[i] += 1
    return values


@dataclass(frozen=True)
class Order:
    id: int
    total: float


class Point(NamedTuple):
    x: int
    y: int


def example_pure_vs_impure() -> None:
    print("\nExample 1: Pure vs impure function")
    data = [1, 2, 3]
    print("  pure result ->", pure_increment(data))
    print("  original after pure ->", data)

    print("  impure result ->", impure_increment(data))
    print("  original after impure ->", data)
    print("  hidden_state ->", hidden_state)


def example_frozen_dataclass() -> None:
    print("\nExample 2: @dataclass(frozen=True) prevents mutation")
    order = Order(1, 19.99)
    print("  order ->", order)
    try:
        order.total = 5.0  # type: ignore[misc]
    except Exception as exc:
        print("  mutation blocked ->", exc)
    updated = replace(order, total=25.0)
    print("  updated copy ->", updated)


def example_namedtuple_and_frozenset() -> None:
    print("\nExample 3: NamedTuple and frozenset as immutable containers")
    p = Point(2, 3)
    print("  point ->", p)
    fs = frozenset({"a", "b"})
    print("  frozenset ->", fs)
    try:
        fs.add("c")  # type: ignore[attr-defined]
    except Exception as exc:
        print("  cannot mutate frozenset ->", exc)


def example_copy_patterns() -> None:
    print("\nExample 4: Copy vs deep copy")
    nested = {"nums": [1, 2]}
    shallow = copy.copy(nested)
    deep = copy.deepcopy(nested)
    shallow["nums"].append(3)
    print("  original after shallow append ->", nested)
    print("  deep copy remains ->", deep)


def example_state_transforms() -> None:
    print("\nExample 5: Immutable state transformation (event sourcing flavor)")
    state = {"balance": 100}
    events = ["deposit 20", "withdraw 15", "withdraw 200"]

    def apply(state, event):
        kind, amount_s = event.split()
        amount = int(amount_s)
        new_state = state.copy()
        if kind == "deposit":
            new_state["balance"] += amount
        else:
            new_state["balance"] -= amount
        return new_state

    for ev in events:
        state = apply(state, ev)
        print(f"  after {ev} -> {state}")
    print("  note: each step returns new state; easier to test and replay")


def example_when_mutation_is_okay() -> None:
    print("\nExample 6: When mutation is clearer")
    nums = [1, 2, 3]
    nums.append(4)
    print("  appending in-place is fine for local, short-lived data")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING IMMUTABILITY & PURE FUNCTIONS")
    print("=" * 70)

    example_pure_vs_impure()
    example_frozen_dataclass()
    example_namedtuple_and_frozenset()
    example_copy_patterns()
    example_state_transforms()
    example_when_mutation_is_okay()

    print("\nAll immutability examples completed.")


if __name__ == "__main__":
    run_all()
