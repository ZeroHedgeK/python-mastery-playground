"""
Solution: validate_args

Key Insights:
1. inspect.signature().bind_partial binds provided args to parameter names, handling defaults and keywords uniformly.
2. Validating against a types mapping allows clear TypeError messages per argument.
3. functools.wraps preserves metadata for decorated functions.

Alternative Approaches:
- Manually map positional indices to names, but binding is less error-prone.
- Accept tuples of types to allow multiple valid types per argument.
"""

from __future__ import annotations

import inspect
from functools import wraps
from typing import Any, Callable, Mapping


# === SOLUTION ===


def validate_args(types: Mapping[str, type]):
    def decorator(fn: Callable):
        sig = inspect.signature(fn)

        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any):
            bound = sig.bind_partial(*args, **kwargs)
            for name, expected in types.items():
                if name in bound.arguments:
                    value = bound.arguments[name]
                    if not isinstance(value, expected):
                        raise TypeError(f"Argument {name} must be {expected}")
            return fn(*args, **kwargs)

        return wrapper

    return decorator


# === VERIFICATION ===


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
    test_valid_positional()
    print("✅ test_valid_positional passed")
    test_invalid_keyword()
    print("✅ test_invalid_keyword passed")
    test_preserves_metadata()
    print("✅ test_preserves_metadata passed")
    print("\n🎉 All tests passed!")
