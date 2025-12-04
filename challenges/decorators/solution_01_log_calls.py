"""
Solution: log_calls

Key Insights:
1. functools.wraps preserves metadata so decorated functions remain transparent.
2. The wrapper must forward *args/**kwargs and return the underlying result.
3. A simple print statement before invocation satisfies the logging requirement.

Alternative Approaches:
- Use logging module instead of print; capture the same message format.
- Accept a logger argument to make the decorator configurable.
"""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable


# === SOLUTION ===


def log_calls(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any):
        print(f"CALL {fn.__name__} args={args} kwargs={kwargs}")
        return fn(*args, **kwargs)

    return wrapper


# === VERIFICATION ===

import io
from contextlib import redirect_stdout


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
    test_basic()
    print("✅ test_basic passed")
    test_kwargs()
    print("✅ test_kwargs passed")
    print("\n🎉 All tests passed!")
