"""
Solution: mock_time

Key Insights:
1. Replace time.time with a lambda returning the fixed value inside the context.
2. Use try/finally to restore the original function even on exceptions.
3. contextmanager keeps usage lightweight.

Alternative Approaches:
- Use unittest.mock.patch; manual swap shows the core idea.
"""

from __future__ import annotations

import time
from contextlib import contextmanager


# === SOLUTION ===


@contextmanager
def mock_time(fixed: float):
    original = time.time
    time.time = lambda: fixed
    try:
        yield
    finally:
        time.time = original


# === VERIFICATION ===


def test_mock_time():
    before = time.time()
    with mock_time(123.0):
        assert time.time() == 123.0
    assert time.time() >= before


if __name__ == "__main__":
    test_mock_time()
    print("✅ test_mock_time passed")
    print("\n🎉 All tests passed!")
