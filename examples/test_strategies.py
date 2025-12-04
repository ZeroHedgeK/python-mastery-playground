"""
Testing strategy patterns: naming, AAA structure, markers, edge cases, invariants,
and doubles taxonomy. Demonstrates pytest utilities plus scripted demos.
"""

from __future__ import annotations

import math
import warnings

import pytest
from _pytest.warning_types import PytestUnknownMarkWarning


warnings.filterwarnings("ignore", category=PytestUnknownMarkWarning)

from python_mastery.testing_patterns import external_services as _library_reference  # noqa: F401


# === DEMONSTRATIONS ===


def demo_arrange_act_assert():
    print("Arrange-Act-Assert with clear naming")
    numbers = [1, 2, 3]
    total = sum(numbers)
    assert total == 6
    print("  test_sum_numbers_happy_path would assert 6")


def demo_edge_cases_and_exceptions():
    print("Edge cases and exception testing")
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0
    with pytest.warns(UserWarning):
        import warnings

        warnings.warn("watch out")


def demo_property_like_check():
    print("Property-style invariant check (manual loop instead of hypothesis)")
    for x in range(-5, 6):
        assert math.sin(x) ** 2 + math.cos(x) ** 2 == pytest.approx(1)


def demo_markers_and_selection():
    print("Markers: slow vs unit; select with -m or -k")
    print("  e.g., pytest -m slow, pytest -k 'edge'")


def demo_test_doubles_taxonomy():
    print("Test doubles: dummy, stub, fake, spy, mock")
    print("  dummy -> placeholder arg; stub -> returns canned data; fake -> lightweight impl; spy -> records calls; mock -> programmable expectations")


# === PYTEST TESTS ===


def test_sum_edge_cases_empty_list():
    numbers: list[int] = []
    assert sum(numbers) == 0


def test_raise_on_invalid_input():
    with pytest.raises(ValueError):
        int("not-an-int")


def test_invariant_absolute_value():
    for x in range(-3, 4):
        assert abs(x) >= 0


@pytest.mark.slow
def test_slow_marker_example():
    # Still fast; marker shows how to categorize
    assert sum(range(1000)) == sum(range(1000))


def test_stateful_class_multiple_scenarios():
    class Counter:
        def __init__(self):
            self.count = 0

        def inc(self):
            self.count += 1

        def dec(self):
            self.count -= 1

    c = Counter()
    c.inc()
    c.inc()
    c.dec()
    assert c.count == 1


# === MAIN ===


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Patterns: Strategies")
    print("=" * 60)
    demo_arrange_act_assert()
    demo_edge_cases_and_exceptions()
    demo_property_like_check()
    demo_markers_and_selection()
    demo_test_doubles_taxonomy()
    print("\nRun 'pytest examples/test_strategies.py -v' to execute tests")
