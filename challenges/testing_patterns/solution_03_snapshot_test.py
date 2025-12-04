"""
Solution: snapshot_test

Key Insights:
1. First-run creation seeds the snapshot; later runs compare for stability.
2. pathlib simplifies file existence checks and reading/writing text.
3. Raise a clear AssertionError on mismatch to integrate with test runners.

Alternative Approaches:
- Add newline normalization; not needed here but common in snapshot tools.
"""

from __future__ import annotations

from pathlib import Path


# === SOLUTION ===


def assert_matches_snapshot(output: str, snapshot_path: str | Path):
    path = Path(snapshot_path)
    if not path.exists():
        path.write_text(output)
        return
    existing = path.read_text()
    if existing != output:
        raise AssertionError("Snapshot mismatch")


# === VERIFICATION ===


def test_creates_and_compares(tmp_path: Path):
    snap = tmp_path / "snap.txt"
    assert_matches_snapshot("hello", snap)
    assert snap.read_text() == "hello"
    assert_matches_snapshot("hello", snap)
    try:
        assert_matches_snapshot("bye", snap)
    except AssertionError:
        pass
    else:
        raise AssertionError("Snapshot mismatch not raised")


if __name__ == "__main__":
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmp:
        test_creates_and_compares(Path(tmp))
    print("✅ test_creates_and_compares passed")
    print("\n🎉 All tests passed!")
