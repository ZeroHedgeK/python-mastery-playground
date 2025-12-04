"""
Solution: transaction

Key Insights:
1. Snapshot the dict on entry so rollback can simply replace contents.
2. __exit__ sees exception info; restore and return False to re-raise.
3. Using dict.clear/update avoids replacing the original object reference.

Alternative Approaches:
- Manage deep copies for nested data if required; shallow suffices here.
- Accept a callable to perform commit actions instead of mutating the dict.
"""

from __future__ import annotations


# === SOLUTION ===


class transaction:
    def __init__(self, store):
        self.store = store
        self.snapshot = None

    def __enter__(self):
        self.snapshot = self.store.copy()
        return self.store

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.store.clear()
            self.store.update(self.snapshot)
            return False  # re-raise
        return False


# === VERIFICATION ===


def test_commits_on_success():
    data = {"balance": 10}
    with transaction(data):
        data["balance"] += 5
    assert data["balance"] == 15


def test_rolls_back_on_error():
    data = {"balance": 10}
    try:
        with transaction(data):
            data["balance"] += 5
            raise RuntimeError("fail")
    except RuntimeError:
        pass
    assert data["balance"] == 10


if __name__ == "__main__":
    test_commits_on_success()
    print("✅ test_commits_on_success passed")
    test_rolls_back_on_error()
    print("✅ test_rolls_back_on_error passed")
    print("\n🎉 All tests passed!")
