"""
Functional iteration with itertools: lazy chains, grouping, slicing, combinatorics,
and composition. Demonstrates memory-friendly pipelines vs eager lists.
"""

from __future__ import annotations

import itertools
from python_mastery.functional import functional_tools as _library_reference  # noqa: F401


def example_map_filter_chain() -> None:
    print("\nExample 1: map + filter pipeline")
    data = [1, 2, 3, 4, 5]
    pipeline = map(lambda x: x * 2, filter(lambda x: x % 2 == 0, data))
    print("  input ->", data)
    print("  output ->", list(pipeline))
    # Equivalent loop would append conditionally; pipeline stays lazy.


def example_chain_and_starmap() -> None:
    print("\nExample 2: chain flatten + starmap unpack")
    seqs = (["a", "b"], ["c"], [])
    chained = itertools.chain.from_iterable(seqs)
    print("  chained ->", list(chained))

    pairs = [(2, 3), (3, 4)]
    powers = list(itertools.starmap(pow, pairs))
    print("  starmap pow ->", powers)


def example_groupby_sorted_requirement() -> None:
    print("\nExample 3: groupby requires sorted keys")
    records = [
        {"dept": "sales", "name": "Ann"},
        {"dept": "eng", "name": "Bo"},
        {"dept": "sales", "name": "Cy"},
    ]
    records_sorted = sorted(records, key=lambda r: r["dept"])
    for dept, group in itertools.groupby(records_sorted, key=lambda r: r["dept"]):
        names = [r["name"] for r in group]
        print(f"  {dept}: {names}")
    print("  (If unsorted, groupby would split repeated keys.)")


def example_islice_take_drop() -> None:
    print("\nExample 4: islice, takewhile, dropwhile")
    data = itertools.count(1)
    first_five = list(itertools.islice(data, 5))
    print("  islice first 5 ->", first_five)

    nums = [1, 2, 2, 3, 4, 1]
    print("  takewhile <3 ->", list(itertools.takewhile(lambda x: x < 3, nums)))
    print("  dropwhile <3 ->", list(itertools.dropwhile(lambda x: x < 3, nums)))


def example_combinatorics() -> None:
    print("\nExample 5: product / permutations / combinations")
    colors = ["r", "g"]
    sizes = ["S", "M"]
    print("  product ->", list(itertools.product(colors, sizes)))
    print("  permutations 3 choose 2 ->", list(itertools.permutations([1, 2, 3], 2)))
    print("  combinations 3 choose 2 ->", list(itertools.combinations([1, 2, 3], 2)))


def example_tee_warning() -> None:
    print("\nExample 6: tee duplicates iterators (stores data)")
    source = (n * 2 for n in range(3))
    a, b = itertools.tee(source)
    print("  a ->", list(a))
    print("  b ->", list(b))
    print("  warning: tee buffers values; for large streams prefer re-generating")


def example_pipeline_vs_eager_memory() -> None:
    print("\nExample 7: Memory-friendly pipeline vs eager list")
    data = range(10000)
    pipeline = itertools.islice((n * 2 for n in data if n % 3 == 0), 0, 5)
    print("  pipeline first 5 ->", list(pipeline))
    # Eager alternative would build a full list: [n*2 for n in data if n%3==0]


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING itertools PATTERNS")
    print("=" * 70)

    example_map_filter_chain()
    example_chain_and_starmap()
    example_groupby_sorted_requirement()
    example_islice_take_drop()
    example_combinatorics()
    example_tee_warning()
    example_pipeline_vs_eager_memory()

    print("\nAll itertools examples completed.")


if __name__ == "__main__":
    run_all()
