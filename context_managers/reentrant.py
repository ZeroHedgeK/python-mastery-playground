"""
Reentrant Context Managers
=========================

Demonstrates the difference between single-use and reusable context managers.

Most context managers (like 'open()') are single-use. Once you exit them,
you cannot enter them again. Reentrant context managers allow you to
enter/exit multiple times.
"""

from contextlib import contextmanager

class SingleUse:
    """
    Typical context manager. Can only be used once.
    """
    def __init__(self):
        self.used = False

    def __enter__(self):
        if self.used:
            raise RuntimeError("Cannot reuse this context manager!")
        self.used = True
        print("Entering SingleUse")
        return self

    def __exit__(self, *args):
        print("Exiting SingleUse")


class Reusable:
    """
    Reusable context manager. Can be used multiple times.
    Useful for connection pools, thread locks, etc.
    """
    def __init__(self):
        self.count = 0

    def __enter__(self):
        self.count += 1
        print(f"Entering Reusable (usage #{self.count})")
        return self

    def __exit__(self, *args):
        print(f"Exiting Reusable (usage #{self.count})")


def demonstrate_reentrancy():
    print("--- Single Use ---")
    single = SingleUse()

    with single:
        pass

    try:
        print("Trying to reuse...")
        with single:
            pass
    except RuntimeError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Reusable ---")
    reusable = Reusable()

    with reusable:
        pass

    with reusable:
        pass

    print("Success!")

if __name__ == "__main__":
    demonstrate_reentrancy()

