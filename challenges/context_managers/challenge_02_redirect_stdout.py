"""
Challenge: redirect_stdout
Difficulty: ⭐⭐
Time Estimate: 15 minutes
Concepts: context managers, io.StringIO, stdout redirection

Problem:
Implement a context manager `redirect_stdout_to_buffer` that captures all printed
output inside the with-block into an io.StringIO buffer and returns the buffer.

Requirements:
1. Yield the buffer so callers can inspect its contents.
2. Restore original sys.stdout after the context, even on exceptions.
3. Do not rely on contextlib.redirect_stdout; implement the swap yourself.

Hints:
- Save sys.stdout, set it to the buffer, then restore in finally.
- io.StringIO is an in-memory file-like object.

Run tests:
    python challenges/context_managers/challenge_02_redirect_stdout.py
"""

from __future__ import annotations

import io
import sys
from contextlib import contextmanager


# === YOUR CODE HERE ===


@contextmanager
def redirect_stdout_to_buffer():
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


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
    import sys

    try:
        test_captures_output()
        print("✅ test_captures_output passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_captures_output failed: {e}")
        sys.exit(1)

    try:
        test_restores_stdout_on_exception()
        print("✅ test_restores_stdout_on_exception passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_restores_stdout_on_exception failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
