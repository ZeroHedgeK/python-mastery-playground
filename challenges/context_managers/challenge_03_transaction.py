"""
Challenge: transaction
Difficulty: ⭐⭐⭐
Time Estimate: 20 minutes
Concepts: context managers, exception handling, rollback

Problem:
Implement a `transaction` context manager for a mutable dictionary that snapshots
state on entry and restores it if an exception occurs inside the block. On
successful exit, changes persist.

Requirements:
1. Accept a dict object and snapshot its shallow copy on entry.
2. If an exception is raised, restore the original contents and re-raise.
3. If no exception, leave the modified dict intact.

Hints:
- Use try/except/finally in a class-based context manager for clarity.
- A shallow copy (dict.copy()) is sufficient for this exercise.

Run tests:
    python challenges/context_managers/challenge_03_transaction.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


class transaction:
    def __init__(self, store):
        self.store = store
        self.snapshot = None

    def __enter__(self):
        raise NotImplementedError("Your implementation here")

    def __exit__(self, exc_type, exc, tb):
        raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


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
    import sys

    try:
        test_commits_on_success()
        print("✅ test_commits_on_success passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_commits_on_success failed: {e}")
        sys.exit(1)

    try:
        test_rolls_back_on_error()
        print("✅ test_rolls_back_on_error passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_rolls_back_on_error failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
