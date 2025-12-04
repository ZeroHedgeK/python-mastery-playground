"""
Challenge: singleton_meta
Difficulty: ⭐⭐⭐
Time Estimate: 20-25 minutes
Concepts: metaclass, thread safety, singletons

Problem:
Implement a metaclass `SingletonMeta` that ensures only one instance of a class
exists, even when constructed concurrently from multiple threads.

Requirements:
1. Classes using SingletonMeta should return the same instance for repeated calls.
2. Use a threading.Lock to guard instance creation.
3. Store instances per subclass, not globally shared across all.

Hints:
- Override __call__ in the metaclass to control instantiation.
- Keep a dict mapping cls -> instance.

Run tests:
    python challenges/oop/challenge_03_singleton_meta.py
"""

from __future__ import annotations

import threading


# === YOUR CODE HERE ===


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        raise NotImplementedError("Your implementation here")


class Service(metaclass=SingletonMeta):
    pass


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_single_instance():
    a = Service()
    b = Service()
    assert a is b


def test_thread_safety():
    results = []

    def create():
        results.append(Service())

    threads = [threading.Thread(target=create) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len({id(obj) for obj in results}) == 1


if __name__ == "__main__":
    import sys

    try:
        test_single_instance()
        print("✅ test_single_instance passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_single_instance failed: {e}")
        sys.exit(1)

    try:
        test_thread_safety()
        print("✅ test_thread_safety passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_thread_safety failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
