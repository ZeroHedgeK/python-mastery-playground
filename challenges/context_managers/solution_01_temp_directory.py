"""
Solution: temp_directory

Key Insights:
1. contextlib.contextmanager simplifies pairing mkdtemp with rmtree.
2. A try/finally ensures cleanup even when exceptions occur.
3. Yield the path to allow caller usage inside the with-block.

Alternative Approaches:
- Implement __enter__/__exit__ in a class; same logic with slightly more code.
"""

from __future__ import annotations

import os
import shutil
import tempfile
from contextlib import contextmanager


# === SOLUTION ===


@contextmanager
def temp_directory():
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=True)


# === VERIFICATION ===


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
    test_creates_and_cleans()
    print("✅ test_creates_and_cleans passed")
    test_cleans_on_exception()
    print("✅ test_cleans_on_exception passed")
    print("\n🎉 All tests passed!")
