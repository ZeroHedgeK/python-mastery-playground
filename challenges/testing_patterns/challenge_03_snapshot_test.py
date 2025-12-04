"""
Challenge: snapshot_test
Difficulty: ⭐⭐⭐
Time Estimate: 20-25 minutes
Concepts: testing, file snapshots, comparison

Problem:
Implement `assert_matches_snapshot(output: str, snapshot_path: str)` that writes
the snapshot file if it doesn't exist, otherwise compares output to the file
contents and raises AssertionError on mismatch.

Requirements:
1. If snapshot file is missing, create it with the given output.
2. If present and different, raise AssertionError("Snapshot mismatch").
3. If present and identical, do nothing.

Hints:
- Use pathlib.Path for convenience.

Run tests:
    python challenges/testing/challenge_03_snapshot_test.py
"""

from __future__ import annotations

from pathlib import Path


# === YOUR CODE HERE ===


def assert_matches_snapshot(output: str, snapshot_path: str):
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_creates_and_compares(tmp_path: Path):
    snap = tmp_path / "snap.txt"
    assert_matches_snapshot("hello", snap)
    assert snap.read_text() == "hello"
    # same output passes
    assert_matches_snapshot("hello", snap)
    try:
        assert_matches_snapshot("bye", snap)
    except AssertionError:
        pass
    else:
        raise AssertionError("Snapshot mismatch not raised")


if __name__ == "__main__":
    import sys
    from tempfile import TemporaryDirectory

    try:
        with TemporaryDirectory() as tmp:
            test_creates_and_compares(Path(tmp))
        print("✅ test_creates_and_compares passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_creates_and_compares failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
