"""
Demonstrate the `@cache` decorator: cache hits, TTL expiry, complex keys, and LRU.

Each example uses tiny sleeps so you can feel the difference between cache hits
and misses without waiting. Prints show when work is recomputed versus served
instantly from cache.
"""

from __future__ import annotations

import time

from python_mastery.decorators import cache


@cache(ttl=5.0)
def slow_square(n: int) -> int:
    """Pretend this is expensive; sleep briefly to make hits noticeable."""
    print(f"  computing square for {n}")
    time.sleep(0.1)
    return n * n


@cache(ttl=0.3)
def short_lived(value: str) -> str:
    """Short TTL so we can see expiry quickly."""
    print("  computing short-lived value")
    return f"fresh-{value}-{time.time():.2f}"


@cache(ttl=5.0)
def normalize_and_join(data: dict[str, int], tags: list[str]) -> str:
    """
    Mutable inputs (dict/list) get normalized for cache keys; repeats hit cache.
    """

    print("  joining normalized data")
    time.sleep(0.05)
    body = ",".join(f"{k}:{v}" for k, v in sorted(data.items()))
    tag_block = ":".join(sorted(tags))
    return f"{body}|{tag_block}"


@cache(ttl=5.0, maxsize=2)
def tiny_lru(value: str) -> str:
    """Small maxsize to force eviction and show LRU behavior."""
    print(f"  computing for {value}")
    return f"payload-{value}-{time.time():.2f}"


def example_basic_hit_miss() -> None:
    print("\nExample 1: Basic cache hit vs miss")
    print("First call (miss → computes):")
    print(f"  result: {slow_square(6)}")
    print("Second call (hit → instant):")
    print(f"  result: {slow_square(6)}")


def example_ttl_expiry() -> None:
    print("\nExample 2: TTL expiry")
    first = short_lived("alpha")
    print(f"  first: {first}")
    second = short_lived("alpha")
    print(f"  immediate hit: {second}")
    print("  waiting for TTL to expire...")
    time.sleep(0.4)
    third = short_lived("alpha")
    print(f"  after expiry (recomputed): {third}")


def example_complex_keys() -> None:
    print("\nExample 3: Complex/mutable arguments become stable cache keys")
    payload = {"b": 2, "a": 1}
    tags = ["x", "y"]
    print(f"  first call: {normalize_and_join(payload, tags)}")
    print(f"  second call same args (hit): {normalize_and_join(payload, tags)}")
    print(f"  different order still a hit: {normalize_and_join({'a': 1, 'b': 2}, ['y', 'x'])}")


def example_lru_eviction() -> None:
    print("\nExample 4: LRU eviction with tiny maxsize")
    print(f"  A: {tiny_lru('A')}")
    print(f"  B: {tiny_lru('B')}")
    print(f"  A again (hit): {tiny_lru('A')}")
    print(f"  C (evicts B): {tiny_lru('C')}")
    print(f"  B recomputed (was evicted): {tiny_lru('B')}")


def run_all() -> None:
    """Run all cache examples in sequence."""

    print("=" * 70)
    print("DEMONSTRATING @cache DECORATOR")
    print("=" * 70)

    example_basic_hit_miss()
    example_ttl_expiry()
    example_complex_keys()
    example_lru_eviction()

    print("\nAll @cache examples completed! Watch for cache hits vs recomputes.")


if __name__ == "__main__":
    run_all()
