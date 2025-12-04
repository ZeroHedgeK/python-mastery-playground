"""
Challenge: pipeline_builder
Difficulty: ⭐⭐
Time Estimate: 15-20 minutes
Concepts: generators, fluent API, control flow

Problem:
Implement a Pipeline class that supports chaining transformations and then
executing them lazily over an iterable.

Requirements:
1. Pipeline().map(fn).filter(pred).run(data) returns a generator applying steps.
2. Chaining should not mutate previous pipelines; create new Pipeline instances.
3. Preserve order of data.

Hints:
- Store steps as callables; copy list when adding a step.

Run tests:
    python challenges/control_flow/challenge_02_pipeline_builder.py
"""

from __future__ import annotations

from typing import Callable, Iterable


# === YOUR CODE HERE ===


class Pipeline:
    def __init__(self, steps=None):
        raise NotImplementedError("Your implementation here")

    def map(self, fn: Callable):
        raise NotImplementedError("Your implementation here")

    def filter(self, pred: Callable):
        raise NotImplementedError("Your implementation here")

    def run(self, data: Iterable):
        raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_pipeline():
    pipeline = Pipeline().map(lambda x: x * 2).filter(lambda x: x > 2)
    result = list(pipeline.run([1, 2, 3]))
    assert result == [4, 6]


if __name__ == "__main__":
    import sys

    try:
        test_pipeline()
        print("✅ test_pipeline passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_pipeline failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
