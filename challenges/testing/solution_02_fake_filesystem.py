"""
Solution: fake_filesystem

Key Insights:
1. A dict is sufficient to map paths to contents for a lightweight fake.
2. Raise FileNotFoundError to mirror pathlib/read_text behavior.
3. Do not delete on read; keep state for repeated reads.

Alternative Approaches:
- Support directories; unnecessary for this exercise.
"""

from __future__ import annotations


# === SOLUTION ===


class FakeFS:
    def __init__(self):
        self._files = {}

    def write_text(self, path: str, content: str):
        self._files[path] = content

    def read_text(self, path: str) -> str:
        if path not in self._files:
            raise FileNotFoundError(path)
        return self._files[path]


# === VERIFICATION ===


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
    test_write_read()
    print("✅ test_write_read passed")
    test_missing_file()
    print("✅ test_missing_file passed")
    print("\n🎉 All tests passed!")
