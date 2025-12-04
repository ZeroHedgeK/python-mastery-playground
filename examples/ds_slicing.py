"""
Advanced slicing patterns: negative indices, steps, slice objects, slice
assignment, and custom __getitem__ handling slices. Shows how slicing can be
clearer than manual index math.
"""

from __future__ import annotations


def example_basic_and_steps() -> None:
    print("\nExample 1: Negative indices and step values")
    letters = list("abcdefghij")
    print(f"  input: {letters}")
    print(f"  last 3: {letters[-3:]}")
    print(f"  every other: {letters[::2]}")
    print(f"  reversed: {letters[::-1]}")


def example_slice_objects() -> None:
    print("\nExample 2: slice objects for reuse")
    data = list(range(12))
    odds = slice(1, None, 2)
    print(f"  data: {data}")
    print(f"  odds via slice obj: {data[odds]}")
    first_half = slice(None, 6)
    print(f"  first half: {data[first_half]}")


def example_slice_assignment() -> None:
    print("\nExample 3: Slice assignment mutates in bulk")
    data = [10, 20, 30, 40, 50]
    print(f"  before: {data}")
    data[1:4] = [21, 31, 41]
    print(f"  replaced middle: {data}")
    data[::2] = [0, 0, 0]
    print(f"  zeroed every other: {data}")


class WindowedSeries:
    """Custom sequence supporting slice-based windowing."""

    def __init__(self, values: list[int]):
        self._values = values

    def __getitem__(self, key):
        if isinstance(key, slice):
            # Return a new WindowedSeries to preserve type
            return WindowedSeries(self._values[key])
        return self._values[key]

    def __repr__(self) -> str:  # pragma: no cover - illustrative
        return f"WindowedSeries({self._values})"

    def sum(self) -> int:
        return sum(self._values)


def example_custom_getitem() -> None:
    print("\nExample 4: Custom class honoring slice semantics")
    series = WindowedSeries([5, 6, 7, 8, 9, 10])
    print(f"  original: {series}")
    middle = series[2:5]
    print(f"  slice [2:5]: {middle} (sum={middle.sum()})")
    tail = series[-3:]
    print(f"  slice last 3: {tail} (sum={tail.sum()})")


def example_imperative_vs_slice() -> None:
    print("\nExample 5: Slicing vs manual loops for subranges")
    data = list(range(15))
    print(f"  input: {data}")

    # Imperative
    manual = []
    for i in range(3, 12, 2):
        manual.append(data[i])
    print(f"  manual stride collect: {manual}")

    # Declarative slicing
    sliced = data[3:12:2]
    print(f"  slicing equivalent: {sliced}")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING ADVANCED SLICING")
    print("=" * 70)

    example_basic_and_steps()
    example_slice_objects()
    example_slice_assignment()
    example_custom_getitem()
    example_imperative_vs_slice()

    print("\nAll slicing examples completed.")


if __name__ == "__main__":
    run_all()
