"""
Generator patterns: expressions, generator functions, pipelines, send(), and a
quick memory comparison vs lists. Emphasizes lazy evaluation for efficiency.
"""

from __future__ import annotations

import sys


def example_memory_comparison() -> None:
    print("\nExample 1: List vs generator size for large ranges")
    gen_exp = (n * n for n in range(1_000_000))
    list_comp = [0, 1, 2]  # small placeholder to avoid huge allocation

    print(f"  generator sys.getsizeof: {sys.getsizeof(gen_exp)} bytes")
    print(f"  tiny list placeholder size: {sys.getsizeof(list_comp)} bytes")
    print("  (A real list of 1M ints would be ~8–9MB; generator stays tiny.)")


def example_pipeline() -> None:
    print("\nExample 2: Chaining generators as a pipeline")

    def numbers():
        for n in range(10):
            yield n

    def evens(seq):
        for n in seq:
            if n % 2 == 0:
                yield n

    def squares(seq):
        for n in seq:
            yield n * n

    pipeline = squares(evens(numbers()))
    print(f"  pipeline output: {list(pipeline)}")


def example_generator_expression() -> None:
    print("\nExample 3: Generator expression for streaming sums")
    data = [5, 7, 9, 10, 12]
    gen = (x + 1 for x in data if x % 2 == 1)
    print(f"  input: {data}")
    print(f"  streamed result: {list(gen)}")


def example_send_coroutine() -> None:
    print("\nExample 4: Using send() to push data into a generator")

    def accumulator():
        total = 0
        while True:
            value = yield total
            if value is None:
                break
            total += value

    gen = accumulator()
    start_total = next(gen)  # prime
    print(f"  start total: {start_total}")
    print(f"  after sending 5: {gen.send(5)}")
    print(f"  after sending 7: {gen.send(7)}")
    print(f"  after sending -2: {gen.send(-2)}")
    try:
        gen.send(None)  # gracefully end
    except StopIteration:
        print("  accumulator closed")


def example_imperative_vs_generator() -> None:
    print("\nExample 5: Imperative aggregation vs generator-driven sum")
    numbers = list(range(20))
    print(f"  input: {numbers}")

    # Imperative
    total = 0
    for n in numbers:
        if n % 3 == 0:
            total += n
    print(f"  imperative sum of multiples of 3: {total}")

    # Declarative/lazy: generator feeds sum()
    gen_total = sum(n for n in numbers if n % 3 == 0)
    print(f"  generator + sum result: {gen_total}")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING GENERATORS")
    print("=" * 70)

    example_memory_comparison()
    example_pipeline()
    example_generator_expression()
    example_send_coroutine()
    example_imperative_vs_generator()

    print("\nAll generator examples completed.")


if __name__ == "__main__":
    run_all()
