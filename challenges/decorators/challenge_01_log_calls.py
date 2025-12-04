"""
Challenge: log_calls
Difficulty: ⭐
Time Estimate: 10 minutes
Concepts: decorators, *args/**kwargs, introspection

Problem:
Implement a decorator `log_calls` that prints the function name and arguments
before executing the function. Preserve return values and function metadata.

Requirements:
1. Print in the format "CALL <func> args=<args> kwargs=<kwargs>".
2. Use functools.wraps to preserve __name__ and __doc__.
3. Work for any positional/keyword arguments.

Hints:
- functools.wraps is required to copy metadata.
- The decorator should return the wrapper function.

Run tests:
    python challenges/decorators/challenge_01_log_calls.py
"""

from __future__ import annotations

import io
from contextlib import redirect_stdout
from functools import wraps


# === YOUR CODE HERE ===

def log_calls(fn):
    """Decorator stub."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        raise NotImplementedError("Your implementation here")

    return wrapper


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def _capture(func):
    buf = io.StringIO()
    with redirect_stdout(buf):
        result = func()
    return buf.getvalue(), result


def test_basic():
    @log_calls
    def add(a, b):
        return a + b

    out, result = _capture(lambda: add(2, 3))
    assert "CALL add" in out
    assert "args=(2, 3)" in out
    assert result == 5
    assert add.__name__ == "add"


def test_kwargs():
    @log_calls
    def greet(name="World"):
        return f"Hello {name}"

    out, result = _capture(lambda: greet(name="Ada"))
    assert "kwargs={'name': 'Ada'}" in out
    assert result == "Hello Ada"


if __name__ == "__main__":
    import sys

    try:
        test_basic()
        print("✅ test_basic passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_basic failed: {e}")
        sys.exit(1)

    try:
        test_kwargs()
        print("✅ test_kwargs passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_kwargs failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
