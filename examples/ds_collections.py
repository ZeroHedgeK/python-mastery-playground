"""
Specialized containers from `collections`: Counter, defaultdict, deque,
namedtuple, and ChainMap. Shows when these beat plain dict/list/tuple and
compares imperative vs declarative approaches.
"""

from __future__ import annotations

from collections import ChainMap, Counter, defaultdict, deque, namedtuple


def example_counter() -> None:
    print("\nExample 1: Counter frequencies and arithmetic")
    words = ["red", "blue", "red", "green", "blue", "red"]
    counts = Counter(words)
    print(f"  counts: {counts}")
    print(f"  most_common(2): {counts.most_common(2)}")

    today = Counter({'red': 2, 'yellow': 1})
    combined = counts + today
    print(f"  combined via + : {combined}")
    diff = counts - today
    print(f"  diff via - (no negatives kept): {diff}")


def example_defaultdict_grouping() -> None:
    print("\nExample 2: defaultdict for grouping vs manual checks")
    pairs = [("fruit", "apple"), ("fruit", "pear"), ("veg", "carrot"), ("veg", "peas")]

    # Imperative grouping with checks
    grouped_manual: dict[str, list[str]] = {}
    for category, item in pairs:
        if category not in grouped_manual:
            grouped_manual[category] = []
        grouped_manual[category].append(item)
    print(f"  manual grouping: {grouped_manual}")

    # defaultdict removes the existence check
    grouped_dd: defaultdict[str, list[str]] = defaultdict(list)
    for category, item in pairs:
        grouped_dd[category].append(item)
    print(f"  defaultdict grouping: {dict(grouped_dd)}")


def example_deque_sliding_window() -> None:
    print("\nExample 3: deque as sliding window / bounded buffer")
    data = [1, 2, 3, 4, 5, 6]
    window: deque[int] = deque(maxlen=3)
    for value in data:
        window.append(value)
        print(f"  appended {value}, window = {list(window)} (rolling sum={sum(window)})")

    # Compare to list pop(0) cost
    print("  deque keeps O(1) pops/appends at both ends; lists shift elements.")


def example_namedtuple_records() -> None:
    print("\nExample 4: namedtuple for lightweight records")
    Order = namedtuple("Order", ["id", "total", "status"])
    order = Order(id=101, total=49.99, status="shipped")
    print(f"  order: {order}")
    print(f"  asdict: {order._asdict()}")
    updated = order._replace(status="delivered")
    print(f"  updated via _replace: {updated}")


def example_chainmap_overrides() -> None:
    print("\nExample 5: ChainMap for layered configuration")
    defaults = {"timeout": 5, "retries": 2, "region": "us"}
    env = {"region": "eu"}
    cli = {"timeout": 2}

    config = ChainMap(cli, env, defaults)
    print(f"  effective timeout: {config['timeout']} (cli > env > defaults)")
    print(f"  effective retries: {config['retries']}")
    print(f"  effective region:  {config['region']}")


def run_all() -> None:
    print("=" * 70)
    print("DEMONSTRATING collections SPECIALTIES")
    print("=" * 70)

    example_counter()
    example_defaultdict_grouping()
    example_deque_sliding_window()
    example_namedtuple_records()
    example_chainmap_overrides()

    print("\nAll collections examples completed.")


if __name__ == "__main__":
    run_all()
