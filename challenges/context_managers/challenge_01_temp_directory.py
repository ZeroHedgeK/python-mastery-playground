"""
Challenge: temp_directory
Difficulty: ⭐
Time Estimate: 10 minutes
Concepts: context managers, tempfile, cleanup

Problem:
Create a context manager `temp_directory` that yields a temporary directory path
and deletes the directory (and its contents) when the context exits.

Requirements:
1. Use tempfile.mkdtemp to create the directory.
2. Ensure deletion occurs even if an exception is raised inside the context.
3. Return the path string from the context manager.

Hints:
- Use contextlib.contextmanager to simplify setup/teardown.
- shutil.rmtree removes non-empty directories.

Run tests:
    python challenges/context_managers/challenge_01_temp_directory.py
"""

from __future__ import annotations

import os
import shutil
import tempfile
from contextlib import contextmanager


# === YOUR CODE HERE ===


@contextmanager
def temp_directory():
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_creates_and_cleans():
    path_seen = None
    try:
        with temp_directory() as path:
            path_seen = path
            assert os.path.isdir(path)
            with open(os.path.join(path, "file.txt"), "w", encoding="utf-8") as fh:
                fh.write("hi")
    finally:
        if path_seen:
            assert not os.path.exists(path_seen)


def test_cleans_on_exception():
    path_seen = None
    try:
        with temp_directory() as path:
            path_seen = path
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert path_seen and not os.path.exists(path_seen)


if __name__ == "__main__":
    import sys

    try:
        test_creates_and_cleans()
        print("✅ test_creates_and_cleans passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_creates_and_cleans failed: {e}")
        sys.exit(1)

    try:
        test_cleans_on_exception()
        print("✅ test_cleans_on_exception passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_cleans_on_exception failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
