"""
Solution: redirect_stdout_to_buffer

Key Insights:
1. Swapping sys.stdout to a StringIO buffer captures print output transparently.
2. Always restore the original stdout in a finally block to avoid leaking state.
3. Yield the buffer so callers can inspect captured output after the context.

Alternative Approaches:
- Use contextlib.redirect_stdout internally; this solution shows manual control.
"""

from __future__ import annotations

import io
import sys
from contextlib import contextmanager


# === SOLUTION ===


@contextmanager
def redirect_stdout_to_buffer():
    buffer = io.StringIO()
    original = sys.stdout
    sys.stdout = buffer
    try:
        yield buffer
    finally:
        sys.stdout = original


# === VERIFICATION ===


def test_captures_output():
    with redirect_stdout_to_buffer() as buf:
        print("hello")
        print("world")
    assert buf.getvalue().strip().splitlines() == ["hello", "world"]


def test_restores_stdout_on_exception():
    original = sys.stdout
    try:
        with redirect_stdout_to_buffer():
            print("in")
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert sys.stdout is original


if __name__ == "__main__":
    test_captures_output()
    print("✅ test_captures_output passed")
    test_restores_stdout_on_exception()
    print("✅ test_restores_stdout_on_exception passed")
    print("\n🎉 All tests passed!")
