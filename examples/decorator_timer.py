"""
Demonstrate the `@timer` decorator with small, fast-running examples.

The goal is to show how timing wraps different shapes of functions (sleepy work,
CPU work, string processing, defaults, and nested calls) without changing their
behavior. Each example prints the inputs and outputs so you can see the decorator
is transparent while adding timing information.
"""

from __future__ import annotations

import time

from python_mastery.decorators import timer


@timer
def sleepy_task(duration: float = 0.2) -> str:
    """Simulate I/O or waiting; shows timing around wall-clock pauses."""
    print(f"→ sleepy_task: pretending to wait {duration:.2f}s for an API response")
    time.sleep(duration)
    return "done waiting"


@timer
def crunch_numbers(numbers: list[int]) -> int:
    """Show that CPU-bound work is also timed and return value is preserved."""
    print(f"→ crunch_numbers: summing {len(numbers)} numbers")
    return sum(n * n for n in numbers)


@timer
def render_report(title: str, rows: list[str]) -> str:
    """Tiny text aggregation to mimic light I/O and formatting."""
    print(f"→ render_report: building report for '{title}' ({len(rows)} rows)")
    time.sleep(0.05)
    body = "\n".join(f"- {row}" for row in rows)
    return f"{title}\n{body}"


@timer
def greet(name: str = "World", punctuation: str = "!") -> str:
    """Defaults demonstrate decorator compatibility with kwargs and defaults."""
    return f"Hello, {name}{punctuation}"


@timer
def chained_computation(n: int) -> int:
    """
    Combine timed calls to show decorators compose: this calls another timed
    function to make sure timing doesn't swallow return values.
    """

    # Using a short list keeps runtime tiny while showing nested timing.
    numbers = list(range(n))
    subtotal = crunch_numbers(numbers)
    print(f"→ chained_computation: subtotal from crunch_numbers = {subtotal}")
    return subtotal + n


def example_basic_sleep() -> None:
    print("\nExample 1: Basic sleep to see timing around waiting")
    result = sleepy_task(0.15)
    print(f"Result: {result}")


def example_cpu_work() -> None:
    print("\nExample 2: CPU-ish work (small sum of squares)")
    data = [1, 2, 3, 4, 5]
    result = crunch_numbers(data)
    print(f"Result: {result}")


def example_text_processing() -> None:
    print("\nExample 3: Text processing with light formatting")
    report = render_report("Status", ["ready", "steady", "go"])
    print("Rendered report:\n" + report)


def example_defaults_and_kwargs() -> None:
    print("\nExample 4: Defaults and kwargs still work with decorators")
    print(greet())
    print(greet("Alice"))
    print(greet(name="Bob", punctuation="!!"))


def example_chained_calls() -> None:
    print("\nExample 5: Chained timed calls remain transparent")
    total = chained_computation(6)
    print(f"Chained total: {total}")


def run_all() -> None:
    """Run all timer examples in a clear order."""

    print("=" * 70)
    print("DEMONSTRATING @timer DECORATOR")
    print("=" * 70)

    example_basic_sleep()
    example_cpu_work()
    example_text_processing()
    example_defaults_and_kwargs()
    example_chained_calls()

    print("\nAll @timer examples completed! Timing messages appear above.")


if __name__ == "__main__":
    run_all()
