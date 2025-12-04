"""
Solution: producer_consumer

Key Insights:
1. A sentinel signals the consumer to exit cleanly after all items are processed.
2. queue.task_done/queue.join coordinate completion between threads.
3. Joining threads prevents premature exit.

Alternative Approaches:
- Use multiple consumers; same pattern with more threads.
"""

from __future__ import annotations

import queue
import threading
from typing import List


# === SOLUTION ===


def run_pipeline(items) -> List[int]:
    q: queue.Queue = queue.Queue()
    sentinel = object()
    processed: List[int] = []

    def producer():
        for item in items:
            q.put(item)
        q.put(sentinel)

    def consumer():
        while True:
            item = q.get()
            try:
                if item is sentinel:
                    break
                processed.append(item * 2)
            finally:
                q.task_done()

    t_prod = threading.Thread(target=producer)
    t_cons = threading.Thread(target=consumer)
    t_prod.start()
    t_cons.start()
    t_prod.join()
    q.join()
    t_cons.join()
    return processed


# === VERIFICATION ===


def test_pipeline_processes_all():
    processed = run_pipeline([1, 2, 3])
    assert processed == [2, 4, 6]


if __name__ == "__main__":
    test_pipeline_processes_all()
    print("✅ test_pipeline_processes_all passed")
    print("\n🎉 All tests passed!")
