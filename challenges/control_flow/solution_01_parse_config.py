"""
Solution: parse_config

Key Insights:
1. Structural pattern matching on dicts keeps branching concise.
2. Order patterns from specific to general; fallback with case _.

Alternative Approaches:
- Plain if/elif; match is clearer for structured keys.
"""

from __future__ import annotations


# === SOLUTION ===


def parse_config(config: dict) -> str:
    match config:
        case {"mode": "dev"}:
            return "development"
        case {"mode": "prod", "region": region}:
            return f"prod-{region}"
        case _:
            return "unknown"


# === VERIFICATION ===


def test_dev():
    assert parse_config({"mode": "dev"}) == "development"


def test_prod_region():
    assert parse_config({"mode": "prod", "region": "us"}) == "prod-us"


def test_unknown():
    assert parse_config({}) == "unknown"


if __name__ == "__main__":
    test_dev()
    print("✅ test_dev passed")
    test_prod_region()
    print("✅ test_prod_region passed")
    test_unknown()
    print("✅ test_unknown passed")
    print("\n🎉 All tests passed!")
