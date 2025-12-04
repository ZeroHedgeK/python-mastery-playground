"""
Showcase timing contexts: class-based `Timer` vs generator-based `timer_context`.

We time small operations, access elapsed time inside a class-based context, and
show exception behavior. Each example prints before/during/after so you can see
what the context manager adds without changing business logic.
"""

from __future__ import annotations

import time

from python_mastery.context_managers import Timer, timer_context


def example_class_basic() -> None:
    print("\nExample 1: Class-based Timer with elapsed access during the block")
    with Timer("basic") as t:
        time.sleep(0.05)
        print(f"  inside: elapsed so far ≈ {t.elapsed:.4f}s")
    print(f"  after: final elapsed ≈ {t.elapsed:.4f}s")


def example_decorator_basic() -> None:
    print("\nExample 2: @contextmanager variant for concise timing")
    with timer_context("decorator_variant"):
        time.sleep(0.03)
        print("  inside: work done (no elapsed access here)")


def example_nested_timers() -> None:
    print("\nExample 3: Nested timers to see overlapping scopes")
    with Timer("outer"):
        time.sleep(0.02)
        with timer_context("inner"):
            time.sleep(0.02)
            print("  inside inner: quick task")
        time.sleep(0.01)
        print("  back to outer work")


def example_exception_handling() -> None:
    print("\nExample 4: Exception propagation while still recording time")
    try:
        with Timer("failing") as t:
            time.sleep(0.02)
            raise RuntimeError("simulated failure")
    except RuntimeError as exc:
        print(f"  caught: {exc}")
        print(f"  timer still captured ≈ {t.elapsed:.4f}s")

    try:
        with timer_context("failing_decorator"):
            time.sleep(0.01)
            raise ValueError("another failure")
    except ValueError as exc:
        print(f"  decorator context propagated: {exc}")


def example_pipeline_use_case() -> None:
    print("\nExample 5: Timing micro-stages in a tiny pipeline")

    with Timer("load"):
        time.sleep(0.015)
        print("  loaded data")

    with Timer("process") as t:
        time.sleep(0.02)
        print(f"  midway process elapsed ≈ {t.elapsed:.4f}s")
        time.sleep(0.01)
    print("  processed data")

    with timer_context("save"):
        time.sleep(0.015)
        print("  saved data")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING CONTEXT MANAGER TIMERS")
    print("=" * 70)

    example_class_basic()
    example_decorator_basic()
    example_nested_timers()
    example_exception_handling()
    example_pipeline_use_case()

    print("\nAll timer context examples done. Notice behavior differences and timing access.")


if __name__ == "__main__":
    run_all()
