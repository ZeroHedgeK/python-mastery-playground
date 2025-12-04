"""
Solution: parallel_map

Key Insights:
1. ThreadPoolExecutor.map preserves input order, simplifying result handling.
2. Using a context manager ensures the pool shuts down cleanly.
3. Converting to list forces evaluation and collects results.

Alternative Approaches:
- Submit futures individually and sort by input order; map is simpler.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, Callable, Any, List


# === SOLUTION ===


def parallel_map(func: Callable[[Any], Any], iterable: Iterable[Any], max_workers: int = 4) -> List[Any]:
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        return list(ex.map(func, iterable))


# === VERIFICATION ===


def test_basic():
    data = [1, 2, 3]
    out = parallel_map(lambda x: x * 2, data)
    assert out == [2, 4, 6]


if __name__ == "__main__":
    test_basic()
    print("✅ test_basic passed")
    print("\n🎉 All tests passed!")
