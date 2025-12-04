"""
Demonstrate the `@rate_limit` decorator with small periods and clear feedback.

We show bursting into the limit, graceful waiting, and how separate limiters keep
independent budgets. Sleep values are tiny so the script finishes quickly.
"""

from __future__ import annotations

import time

from python_mastery.decorators import rate_limit
from python_mastery.exceptions import RateLimitExceeded


@rate_limit(calls=3, period=1.0)
def ping(endpoint: str) -> str:
    """Lightweight action to show rate limiting across repeated calls."""
    print(f"  hitting {endpoint}")
    return "ok"


@rate_limit(calls=2, period=1.5)
def heavy(endpoint: str) -> str:
    """Separate limiter to illustrate independent buckets."""
    print(f"  heavy work on {endpoint}")
    return "heavy-ok"


def example_burst_then_limit() -> None:
    print("\nExample 1: Burst until the limit is hit")
    for i in range(4):
        try:
            result = ping(f"/burst/{i}")
            print(f"    call {i} → {result}")
        except RateLimitExceeded as exc:
            print(f"    rate limited on call {i}: wait ~{exc.wait_time:.2f}s")


def example_respecting_limit() -> None:
    print("\nExample 2: Pause briefly to stay under the cap")
    for i in range(3):
        result = ping(f"/steady/{i}")
        print(f"    steady call {i} → {result}")
        time.sleep(0.4)  # Small pause keeps us inside 3 calls per 1s window


def example_independent_buckets() -> None:
    print("\nExample 3: Different limiters keep separate budgets")
    for name in ["alpha", "beta", "gamma"]:
        try:
            print(f"    heavy {name} → {heavy(f'/heavy/{name}')}")
        except RateLimitExceeded as exc:
            print(f"    heavy limited: wait ~{exc.wait_time:.2f}s")
    time.sleep(0.6)
    try:
        print(f"    heavy alpha again → {heavy('/heavy/alpha')}")
    except RateLimitExceeded as exc:
        print(f"    heavy still limited: wait ~{exc.wait_time:.2f}s")


def run_all() -> None:
    """Run all rate limit examples in sequence."""

    print("=" * 70)
    print("DEMONSTRATING @rate_limit DECORATOR")
    print("=" * 70)

    example_burst_then_limit()
    example_respecting_limit()
    example_independent_buckets()

    print("\nAll @rate_limit examples completed! Rate limiting kept calls in check.")


if __name__ == "__main__":
    run_all()
