"""
Solution: memory_profile

Key Insights:
1. tracemalloc.start/stop must be paired; use try/finally to guarantee stop.
2. get_traced_memory returns current and peak; peak is the second element.
3. wraps preserves metadata of the wrapped function.

Alternative Approaches:
- Use memory_profiler or psutil; tracemalloc is stdlib and lightweight.
"""

from __future__ import annotations

import tracemalloc
from functools import wraps
from typing import Any, Callable, Tuple


# === SOLUTION ===


def memory_profile(fn: Callable) -> Callable:
    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Tuple[Any, int]:
        tracemalloc.start()
        try:
            result = fn(*args, **kwargs)
            current, peak = tracemalloc.get_traced_memory()
            return result, peak
        finally:
            tracemalloc.stop()

    return wrapper


# === VERIFICATION ===


def test_reports_peak():
    @memory_profile
    def allocate(n):
        return [0] * n

    result, peak = allocate(1000)
    assert len(result) == 1000
    assert peak > 0


if __name__ == "__main__":
    test_reports_peak()
    print("✅ test_reports_peak passed")
    print("\n🎉 All tests passed!")
