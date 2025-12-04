"""
Partial application, currying, and function composition to build reusable
specialized callables. Highlights where partial improves clarity (configured
callbacks/clients) and when a simple lambda/inline call is clearer.
"""

from __future__ import annotations

import operator
from functools import partial
from typing import Callable

from python_mastery.functional import functional_tools as _library_reference  # noqa: F401


def compose(*fns: Callable):
    """Compose functions right-to-left: compose(f, g)(x) == f(g(x))."""

    def _composed(arg):
        result = arg
        for fn in reversed(fns):
            result = fn(result)
        return result

    return _composed


def curry_two_arg(fn: Callable):
    """Turn f(a, b) into f(a)(b)."""

    def first(a):
        def second(b):
            return fn(a, b)

        return second

    return first


def example_partial_positional() -> None:
    print("\nExample 1: partial for specialized callbacks")
    apply_discount = partial(operator.mul, 0.9)
    prices = [10, 20, 30]
    discounted = list(map(apply_discount, prices))
    print(f"  prices -> {prices}")
    print(f"  discounted (10% off) -> {discounted}")
    # Inline lambda alternative: lambda x: x * 0.9 — fine for trivial cases.


def example_partial_kwargs() -> None:
    print("\nExample 2: partial with keyword args for config")

    def connect(host: str, *, timeout: float, retries: int) -> str:
        return f"connect to {host} (timeout={timeout}, retries={retries})"

    staging_connect = partial(connect, timeout=1.0, retries=1)
    prod_connect = partial(connect, timeout=2.0, retries=3)
    print("  staging ->", staging_connect("staging.db"))
    print("  prod    ->", prod_connect("prod.db"))


def example_compose_pipeline() -> None:
    print("\nExample 3: compose to build pipelines")
    strip = str.strip
    to_int = int
    double = partial(operator.mul, 2)
    pipeline = compose(double, to_int, strip)
    raw = " 21 "
    print(f"  input {raw!r} ->", pipeline(raw))
    # Imperative equivalent:
    # tmp = raw.strip(); tmp = int(tmp); result = tmp * 2


def example_currying() -> None:
    print("\nExample 4: Currying turns multi-arg into chained single-arg calls")

    def add(a, b):
        return a + b

    curried_add = curry_two_arg(add)
    add_five = curried_add(5)
    print("  add_five(3) ->", add_five(3))


def example_real_world_handler() -> None:
    print("\nExample 5: Partial to preconfigure event handlers")

    def log_event(event: str, *, source: str) -> str:
        return f"[{source}] {event}"

    api_logger = partial(log_event, source="api")
    ui_logger = partial(log_event, source="ui")
    events = ["login", "click"]
    print("  api events ->", [api_logger(ev) for ev in events])
    print("  ui events  ->", [ui_logger(ev) for ev in events])
    print("  note: overusing partial can hide args; use when it clarifies intent")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING PARTIAL/CURRY/COMPOSE")
    print("=" * 70)

    example_partial_positional()
    example_partial_kwargs()
    example_compose_pipeline()
    example_currying()
    example_real_world_handler()

    print("\nAll partial/curry/compose examples completed.")


if __name__ == "__main__":
    run_all()
