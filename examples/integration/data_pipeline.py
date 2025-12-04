"""
Data pipeline integration: generators + context managers + functional transforms.

Why this combination: streaming generators keep memory flat, context managers
guarantee file cleanup and instrumentation, and functional tools compose small
transform steps into a clear pipeline.
"""

from __future__ import annotations

import io
import itertools
from functools import reduce
from typing import Iterable, Iterator

# [CONTEXT MANAGER] timing wrapper
from python_mastery.context_managers import Timer

# [DECORATOR] timing decorator reused for individual steps
from python_mastery.decorators import timer

# [FUNCTIONAL] highlight functional composition utilities
from python_mastery.functional import (
    functional_tools as _functional_reference,
)  # noqa: F401


def fake_csv_source(rows: int = 12) -> io.StringIO:
    data = "\n".join(f"user{i},order{i},value={i*10}" for i in range(rows))
    return io.StringIO(data)


def load_all_data(file_obj: io.StringIO) -> list[str]:
    """
    Failure-first: eager load everything, increasing memory footprint.
    """

    with Timer("eager load"):  # [CONTEXT MANAGER]
        lines = file_obj.readlines()
    print(f"[eager] loaded {len(lines)} rows into memory")
    return lines


def stream_rows(file_obj: io.StringIO) -> Iterator[str]:
    """
    [GENERATOR] Lazy row streaming keeps memory constant.
    """

    for line in file_obj:
        yield line.strip()


@timer  # [DECORATOR]
def parse_row(row: str) -> dict:
    user, order, value_part = row.split(",")
    _, value_str = value_part.split("=")
    return {"user": user, "order": order, "value": int(value_str)}


def transform_rows(rows: Iterable[str]) -> Iterator[dict]:
    # [GENERATOR] pipeline composition via generator expressions
    return (parse_row(row) for row in rows if row)


def aggregate_totals(items: Iterable[dict]) -> dict:
    # [FUNCTIONAL] reduce accumulates totals
    def reducer(acc: dict, item: dict) -> dict:
        acc["count"] += 1
        acc["total"] += item["value"]
        return acc

    return reduce(reducer, items, {"count": 0, "total": 0})


def streaming_pipeline(rows: int = 12) -> None:
    print("\n[streaming] processing with generators + context managers")
    with Timer("streaming end-to-end"):
        source = fake_csv_source(rows)
        results = aggregate_totals(transform_rows(stream_rows(source)))
    print("  streaming results ->", results)


def eager_pipeline(rows: int = 12) -> None:
    print("\n[eager] processing with full materialization (expect more work)")
    source = fake_csv_source(rows)
    lines = load_all_data(source)
    results = aggregate_totals(transform_rows(lines))
    print("  eager results ->", results)


def demonstrate_memory_efficiency() -> None:
    big_rows = 5000
    print("\n[memory] comparing eager vs streaming with", big_rows, "rows")
    source_eager = fake_csv_source(big_rows)
    _ = load_all_data(source_eager)  # intentionally creates a big list

    source_stream = fake_csv_source(big_rows)
    with Timer("stream only uses one row at a time"):
        count = sum(1 for _ in itertools.islice(stream_rows(source_stream), 0, 10))
    print("  streamed first 10 rows, count=", count)


def explain_synergy() -> None:
    print("\nWhy this combination matters:")
    print("  • Generators keep memory predictable even for large files")
    print("  • Context managers ensure files/timers close even on error")
    print("  • Functional reduce/itertools compose small steps clearly")


def run_demo() -> None:
    eager_pipeline()
    streaming_pipeline()
    demonstrate_memory_efficiency()
    explain_synergy()


if __name__ == "__main__":
    run_demo()
