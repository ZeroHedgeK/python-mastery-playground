"""
Challenge: fake_filesystem
Difficulty: ⭐⭐
Time Estimate: 20 minutes
Concepts: fakes, dictionaries, file-like API

Problem:
Implement a simple in-memory fake filesystem supporting write_text and
read_text for paths (strings). Paths map to string contents.

Requirements:
1. FakeFS().write_text(path, content) stores content.
2. FakeFS().read_text(path) returns content or raises FileNotFoundError.
3. Reading does not remove the stored content.

Hints:
- Use a dict internally mapping paths to contents.

Run tests:
    python challenges/testing/challenge_02_fake_filesystem.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


class FakeFS:
    def __init__(self):
        raise NotImplementedError("Your implementation here")

    def write_text(self, path: str, content: str):
        raise NotImplementedError("Your implementation here")

    def read_text(self, path: str) -> str:
        raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_write_read():
    fs = FakeFS()
    fs.write_text("/tmp/file.txt", "hello")
    assert fs.read_text("/tmp/file.txt") == "hello"


def test_missing_file():
    fs = FakeFS()
    try:
        fs.read_text("/nope")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("FileNotFoundError not raised")


if __name__ == "__main__":
    import sys

    try:
        test_write_read()
        print("✅ test_write_read passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_write_read failed: {e}")
        sys.exit(1)

    try:
        test_missing_file()
        print("✅ test_missing_file passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_missing_file failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
