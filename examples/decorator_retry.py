"""
Demonstrate the `@retry` decorator with fast, deterministic scenarios.

We cover success-after-retry, exponential backoff, exception filtering, and the
exhausted path. Each example keeps sleeps short so the whole file runs quickly
while showing why retries add resilience.
"""

from __future__ import annotations

import itertools
import time

from python_mastery.decorators import retry
from python_mastery.exceptions import RetryExhausted


def example_succeeds_after_retry() -> None:
    print("\nExample 1: Succeeds on the second attempt (fixed delay)")

    attempts = itertools.count(1)

    @retry(max_attempts=3, delay=0.1)
    def sometimes_fails() -> str:
        attempt = next(attempts)
        print(f"  attempt {attempt}: simulating transient failure")
        if attempt == 1:
            raise ValueError("first attempt fails")
        return "success on retry"

    result = sometimes_fails()
    print(f"Result: {result}")


def example_exponential_backoff() -> None:
    print("\nExample 2: Exponential backoff limits rapid fire retries")

    attempts = itertools.count(1)

    @retry(max_attempts=3, delay=0.05, backoff=2.0)
    def flaky_service() -> str:
        attempt = next(attempts)
        print(f"  attempt {attempt}: raising on first two attempts")
        if attempt < 3:
            raise ConnectionError("service flaked")
        return "service recovered"

    result = flaky_service()
    print(f"Result: {result}")


def example_exception_filtering() -> None:
    print("\nExample 3: Only retry specific exception types")

    @retry(max_attempts=2, delay=0.05, exceptions=(ValueError,))
    def picky_retry(path: str) -> str:
        print(f"  accessing {path}")
        raise TypeError("wrong exception triggers no retry")

    try:
        picky_retry("/tmp/data")
    except TypeError as exc:  # Raised immediately because it's not retryable
        print(f"Caught expected fast-fail: {exc}")


def example_exhausted() -> None:
    print("\nExample 4: Exhausted retries raise RetryExhausted with context")

    @retry(max_attempts=2, delay=0.05)
    def always_fail() -> None:
        print("  still failing...")
        raise RuntimeError("persistent error")

    try:
        always_fail()
    except RetryExhausted as exc:
        print(f"Caught RetryExhausted: {exc}")
        print(f"  function: {exc.func_name}, attempts: {exc.max_attempts}")


def run_all() -> None:
    """Run all retry examples in sequence."""

    print("=" * 70)
    print("DEMONSTRATING @retry DECORATOR")
    print("=" * 70)

    example_succeeds_after_retry()
    example_exponential_backoff()
    example_exception_filtering()
    example_exhausted()

    print("\nAll @retry examples completed! Notice how retries are controlled and explicit.")


if __name__ == "__main__":
    run_all()
