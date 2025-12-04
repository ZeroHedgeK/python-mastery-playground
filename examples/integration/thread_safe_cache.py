"""
Thread-safe cache integration: threading + decorators + OOP descriptor.

Why this combination: concurrency introduces races, decorators express policies
(timing/ttl), and a descriptor encapsulates per-instance cache plus locking.
"""

from __future__ import annotations

import threading
import time
from typing import Any, Callable, Dict, Optional, Tuple

# [DECORATOR] timing helper
from python_mastery.decorators import timer

# [CONTEXT MANAGER] Timer used for visibility
from python_mastery.context_managers import Timer

# [OOP] reference import to align with descriptor patterns
from python_mastery.oop import advanced_classes as _oop_reference  # noqa: F401

# [THREADING] reference import for concept alignment
from python_mastery.concurrency import threading_demo as _thread_reference  # noqa: F401


unsafe_cache: Dict[str, Tuple[float, str]] = {}


@timer
def expensive_lookup(key: str) -> str:
    """Simulate a costly lookup to show redundant work when races occur."""

    time.sleep(0.05)
    return f"value-for-{key}-{time.time():.3f}"


def racey_lookup(key: str, repeats: int = 4) -> None:
    """
    Failure-first: no locking around shared cache, multiple threads recompute.
    """

    def worker():
        if key not in unsafe_cache:  # race window
            unsafe_cache[key] = (time.time(), expensive_lookup(key))
        print("  [race]", unsafe_cache[key][1])

    threads = [threading.Thread(target=worker) for _ in range(repeats)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


class SafeCacheDescriptor:
    """
    [DESCRIPTOR][THREADING] Cache with per-instance lock and TTL.
    """

    def __init__(self, *, ttl: float, loader: Callable[[str], str]):
        self.ttl = ttl
        self.loader = loader
        self._values: Dict[int, Dict[str, Tuple[float, str]]] = {}
        self._locks: Dict[int, threading.Lock] = {}

    def __get__(self, instance, owner):
        if instance is None:
            return self
        inst_id = id(instance)
        self._values.setdefault(inst_id, {})
        self._locks.setdefault(inst_id, threading.Lock())
        return self

    def get(self, instance, key: str) -> str:
        inst_id = id(instance)
        cache = self._values[inst_id]
        lock = self._locks[inst_id]

        with lock:  # [THREADING]
            now = time.time()
            hit = cache.get(key)
            if hit and now - hit[0] < self.ttl:
                return hit[1]
            value = self.loader(key)
            cache[key] = (now, value)
            return value


class CachedClient:
    data = SafeCacheDescriptor(ttl=0.3, loader=expensive_lookup)

    def __init__(self, name: str):
        self.name = name

    def fetch(self, key: str) -> str:
        return self.data.get(self, key)


def thread_safe_lookup(key: str, repeats: int = 4) -> None:
    client = CachedClient("demo")

    def worker():
        val = client.fetch(key)
        print(f"  [safe] {val}")

    threads = [threading.Thread(target=worker) for _ in range(repeats)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def explain_synergy() -> None:
    print("\nWhy this combination matters:")
    print("  • Threading introduces races; locks inside the descriptor guard shared state")
    print("  • Decorators keep instrumentation and policy reusable")
    print("  • Descriptor keeps per-instance caches isolated without boilerplate")


def run_demo() -> None:
    print("[race] unsafe cache demonstration")
    with Timer("racey run"):
        racey_lookup("key1")

    print("\n[safe] thread-safe cache demonstration")
    with Timer("safe run"):
        thread_safe_lookup("key1")

    explain_synergy()


if __name__ == "__main__":
    run_demo()
