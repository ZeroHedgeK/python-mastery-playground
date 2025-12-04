"""
Solution: singleton_meta

Key Insights:
1. Overriding metaclass __call__ centralizes instance control per subclass.
2. A class-level lock prevents races during first creation.
3. Cache instances in a dict keyed by cls to support multiple singleton classes.

Alternative Approaches:
- Use __new__ inside the class; metaclass approach keeps logic reusable.
"""

from __future__ import annotations

import threading


# === SOLUTION ===


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Service(metaclass=SingletonMeta):
    pass


# === VERIFICATION ===


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
    test_single_instance()
    print("✅ test_single_instance passed")
    test_thread_safety()
    print("✅ test_thread_safety passed")
    print("\n🎉 All tests passed!")
