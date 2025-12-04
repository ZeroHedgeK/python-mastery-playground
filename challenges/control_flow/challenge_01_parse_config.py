"""
Challenge: parse_config
Difficulty: ⭐
Time Estimate: 10-15 minutes
Concepts: match/case, control flow

Problem:
Implement `parse_config(config: dict)` that inspects keys using match/case and
returns a string describing the config type.

Requirements:
1. If config has {"mode": "dev"} -> return "development".
2. If config has {"mode": "prod", "region": <str>} -> return "prod-<region>".
3. Otherwise return "unknown".

Hints:
- Use match on config dict.

Run tests:
    python challenges/control_flow/challenge_01_parse_config.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


def parse_config(config: dict) -> str:
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_dev():
    assert parse_config({"mode": "dev"}) == "development"


def test_prod_region():
    assert parse_config({"mode": "prod", "region": "us"}) == "prod-us"


def test_unknown():
    assert parse_config({}) == "unknown"


if __name__ == "__main__":
    import sys

    try:
        test_dev()
        print("✅ test_dev passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_dev failed: {e}")
        sys.exit(1)

    try:
        test_prod_region()
        print("✅ test_prod_region passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_prod_region failed: {e}")
        sys.exit(1)

    try:
        test_unknown()
        print("✅ test_unknown passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_unknown failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
