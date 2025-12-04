"""
Comprehension patterns: list/dict/set comprehensions, filtering, nesting, and
imperative vs declarative comparisons. Shows when comprehensions improve clarity
and how they map to equivalent for-loop code.
"""

from __future__ import annotations

import itertools


def example_filtering_and_transform() -> None:
    print("\nExample 1: Filter + transform (imperative vs comprehension)")
    numbers = list(range(12))
    print(f"  input: {numbers}")

    # Imperative approach
    squares_of_evens: list[int] = []
    for n in numbers:
        if n % 2 == 0:
            squares_of_evens.append(n * n)
    print(f"  imperative result: {squares_of_evens}")

    # Declarative comprehension — shorter, clearer intent
    comp_result = [n * n for n in numbers if n % 2 == 0]
    print(f"  comprehension result: {comp_result}")


def example_nested_vs_product() -> None:
    print("\nExample 2: Nested comprehension vs itertools.product")
    colors = ["red", "blue"]
    sizes = ["S", "M", "L"]

    nested = [(c, s) for c in colors for s in sizes if s != "M"]
    print(f"  nested comprehension (skip M): {nested}")

    product_version = [
        pair for pair in itertools.product(colors, sizes) if pair[1] != "M"
    ]
    print(f"  product equivalent: {product_version}")


def example_dict_and_set_comps() -> None:
    print("\nExample 3: Dict and set comprehensions from iterables")
    words = ["apple", "banana", "cherry", "banana", "apple"]
    lengths = {w: len(w) for w in words}
    print(f"  dict comp (word → length): {lengths}")

    vowels = {ch for word in words for ch in word if ch in "aeiou"}
    print(f"  set comp (unique vowels): {vowels}")


def example_conditional_exprs() -> None:
    print("\nExample 4: Inline conditionals to label data")
    temps = [18, 23, 29, 16, 21]
    labels = ["hot" if t >= 25 else "cool" for t in temps]
    print(f"  temps:  {temps}")
    print(f"  labels: {labels}")


def example_flattening_and_filtering() -> None:
    print("\nExample 5: Flatten with predicate in a single pass")
    matrix = [
        [1, -1, 2],
        [0, 5, -3],
        [4, 2, 1],
    ]

    positive = [n for row in matrix for n in row if n > 0]
    print(f"  flattened positives: {positive}")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING COMPREHENSIONS")
    print("=" * 70)

    example_filtering_and_transform()
    example_nested_vs_product()
    example_dict_and_set_comps()
    example_conditional_exprs()
    example_flattening_and_filtering()

    print("\nAll comprehension examples completed.")


if __name__ == "__main__":
    run_all()
