"""
Challenge: group_by
Difficulty: ⭐⭐
Time Estimate: 15 minutes
Concepts: dictionaries, grouping, iteration

Problem:
Implement `group_by(items, key_func)` that returns a dict mapping keys to lists
of items for which key_func(item) equals that key.

Requirements:
1. Preserve insertion order of groups as they first appear.
2. Do not mutate the input list.
3. key_func is called once per item.

Hints:
- Use dict.setdefault or collections.defaultdict.

Run tests:
    python challenges/data_structures/challenge_02_group_by.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


def group_by(items, key_func):
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_groups_numbers():
    data = [1, 2, 3, 4, 5]
    grouped = group_by(data, lambda x: "even" if x % 2 == 0 else "odd")
    assert grouped == {"odd": [1, 3, 5], "even": [2, 4]}


def test_order_preserved():
    data = ["apple", "apricot", "banana", "blueberry"]
    grouped = group_by(data, lambda s: s[0])
    assert list(grouped.keys()) == ["a", "b"]


if __name__ == "__main__":
    import sys

    try:
        test_groups_numbers()
        print("✅ test_groups_numbers passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_groups_numbers failed: {e}")
        sys.exit(1)

    try:
        test_order_preserved()
        print("✅ test_order_preserved passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_order_preserved failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
