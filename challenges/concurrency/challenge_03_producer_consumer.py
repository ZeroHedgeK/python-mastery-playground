"""
Challenge: producer_consumer
Difficulty: ⭐⭐⭐
Time Estimate: 25 minutes
Concepts: threading, queue, producer/consumer

Problem:
Implement a producer-consumer pipeline using a Queue where producers put items
and a consumer thread processes them until a sentinel is seen.

Requirements:
1. Use queue.Queue; sentinel object stops consumer.
2. consumer should append processed items to a shared list.
3. Ensure threads join cleanly.

Hints:
- Call queue.task_done() after processing.
- Use queue.join() to wait for all tasks.

Run tests:
    python challenges/concurrency/challenge_03_producer_consumer.py
"""

from __future__ import annotations

import queue
import threading


# === YOUR CODE HERE ===


def run_pipeline(items):
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_pipeline_processes_all():
    processed = run_pipeline([1, 2, 3])
    assert processed == [2, 4, 6]


if __name__ == "__main__":
    import sys

    try:
        test_pipeline_processes_all()
        print("✅ test_pipeline_processes_all passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_pipeline_processes_all failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
