"""
Solution: pipeline_builder

Key Insights:
1. Treat pipeline steps as immutable; each map/filter returns a new Pipeline with copied steps.
2. run composes steps by applying them sequentially to the iterable.
3. Using generator expressions keeps evaluation lazy.

Alternative Approaches:
- Mutate self steps; immutability is safer for reuse.
"""

from __future__ import annotations

from typing import Callable, Iterable, List


# === SOLUTION ===


class Pipeline:
    def __init__(self, steps=None):
        self.steps: List[Callable[[Iterable], Iterable]] = steps or []

    def _clone(self, step: Callable[[Iterable], Iterable]):
        return Pipeline(self.steps + [step])

    def map(self, fn: Callable):
        return self._clone(lambda data: (fn(x) for x in data))

    def filter(self, pred: Callable):
        return self._clone(lambda data: (x for x in data if pred(x)))

    def run(self, data: Iterable):
        result = data
        for step in self.steps:
            result = step(result)
        return result


# === VERIFICATION ===


def test_pipeline():
    pipeline = Pipeline().map(lambda x: x * 2).filter(lambda x: x > 2)
    result = list(pipeline.run([1, 2, 3]))
    assert result == [4, 6]


if __name__ == "__main__":
    test_pipeline()
    print("✅ test_pipeline passed")
    print("\n🎉 All tests passed!")
