"""
Challenge: validate_args
Difficulty: ⭐⭐
Time Estimate: 15 minutes
Concepts: decorators, argument validation, TypeError

Problem:
Implement a decorator `validate_args` that accepts a mapping of argument names to
expected types. When applied to a function, it should validate arguments at call
time and raise TypeError with a helpful message if any argument has the wrong
type.

Requirements:
1. `validate_args(types={'x': int, 'y': str})` should check both positional and keyword args.
2. Raise TypeError("Argument <name> must be <type>") on mismatch.
3. Preserve function metadata via functools.wraps.

Hints:
- Use inspect.signature to bind arguments and their values.
- Binding lets you handle defaults, *args, and **kwargs consistently.

Run tests:
    python challenges/decorators/challenge_02_validate_args.py
"""

from __future__ import annotations

import inspect
from functools import wraps


# === YOUR CODE HERE ===


def validate_args(types):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            raise NotImplementedError("Your implementation here")

        return wrapper

    return decorator


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_valid_positional():
    @validate_args({"x": int, "y": str})
    def combine(x, y):
        return f"{x}:{y}"

    assert combine(1, "a") == "1:a"


def test_invalid_keyword():
    @validate_args({"count": int})
    def repeat(word, count=1):
        return word * count

    try:
        repeat("hi", count="two")
    except TypeError as exc:
        assert "Argument count must be <class 'int'>" in str(exc)
    else:
        raise AssertionError("TypeError not raised")


def test_preserves_metadata():
    @validate_args({"x": int})
    def square(x):
        """Squares a number."""

        return x * x

    assert square.__name__ == "square"
    assert square.__doc__ == "Squares a number."


if __name__ == "__main__":
    import sys

    try:
        test_valid_positional()
        print("✅ test_valid_positional passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_valid_positional failed: {e}")
        sys.exit(1)

    try:
        test_invalid_keyword()
        print("✅ test_invalid_keyword passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_invalid_keyword failed: {e}")
        sys.exit(1)

    try:
        test_preserves_metadata()
        print("✅ test_preserves_metadata passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_preserves_metadata failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
