"""
Generator pipeline examples: lazy streaming transforms, composition, stateful
pipelines, and error handling. Highlights why pipelines beat loading everything
into memory and includes commented imperative equivalents.
"""

from __future__ import annotations

import time
from python_mastery.control_flow import (
    advanced_flow as _library_reference,
)  # noqa: F401


def emit(numbers):
    for n in numbers:
        print(f"  emit {n}")
        yield n


def double(seq):
    for n in seq:
        out = n * 2
        print(f"    double {n}->{out}")
        yield out


def only_even(seq):
    for n in seq:
        if n % 2 == 0:
            print(f"      keep even {n}")
            yield n


def running_total(seq):
    total = 0
    for n in seq:
        total += n
        print(f"        running total now {total}")
        yield total


def example_basic_pipeline() -> None:
    print("\nExample 1: Single lazy transformation")
    data = [1, 2, 3]
    pipeline = double(emit(data))
    print("  consuming pipeline ->", list(pipeline))
    # Imperative equivalent would build a list first, losing laziness.


def example_chained_pipeline() -> None:
    print("\nExample 2: Chained generators as filter→map→accumulate")
    data = [1, 2, 3, 4, 5]
    pipeline = running_total(only_even(double(emit(data))))
    results = list(pipeline)
    print("  final results ->", results)


def flatten(seq_of_seqs):
    for seq in seq_of_seqs:
        yield from seq  # yield from flattens without nested loops


def example_yield_from_flatten() -> None:
    print("\nExample 3: yield from for flattening")
    nested = [["a", "b"], ["c"], []]
    flat = list(flatten(nested))
    print("  flat ->", flat)


def example_pipeline_vs_list_comp() -> None:
    print("\nExample 4: Memory friendliness vs eager list chain")
    data = range(10_000)

    start = time.perf_counter()
    eager = [n * 2 for n in data if n % 2 == 0]
    eager_sum = sum(eager)
    eager_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    lazy_sum = sum(double(n for n in data if n % 2 == 0))
    lazy_elapsed = time.perf_counter() - start

    print(f"  eager sum {eager_sum}, time {eager_elapsed:.4f}s")
    print(f"  lazy  sum {lazy_sum}, time {lazy_elapsed:.4f}s (streams without list)")


def example_error_handling() -> None:
    print("\nExample 5: Handling errors in pipeline consumers")

    def maybe_fail(seq):
        for n in seq:
            if n == 3:
                raise ValueError("bad data")
            yield n

    try:
        list(maybe_fail(emit([1, 2, 3, 4])))
    except ValueError as exc:
        print("  caught error, upstream generators already consumed emitted values")
        print("  exception:", exc)


def example_real_world_log_processing() -> None:
    print("\nExample 6: Log filtering pipeline (simulated)")
    logs = [
        "INFO start",
        "WARN slow",
        "INFO ok",
        "ERROR failure",
    ]

    def parse(lines):
        for line in lines:
            level, message = line.split(maxsplit=1)
            yield {"level": level, "message": message}

    def only_errors(entries):
        for entry in entries:
            if entry["level"] == "ERROR":
                yield entry

    pipeline = only_errors(parse(emit(logs)))
    print("  error entries ->", list(pipeline))
    # Equivalent manual loop would be longer and less composable.


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING GENERATOR PIPELINES")
    print("=" * 70)

    example_basic_pipeline()
    example_chained_pipeline()
    example_yield_from_flatten()
    example_pipeline_vs_list_comp()
    example_error_handling()
    example_real_world_log_processing()

    print("\nAll pipeline examples completed.")


if __name__ == "__main__":
    run_all()
