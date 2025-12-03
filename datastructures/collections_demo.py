"""
Collections Module Demo
======================

The 'collections' module implements specialized container datatypes providing
alternatives to Python's general purpose built-in containers, dict, list, set, and tuple.
"""

from collections import Counter, defaultdict, deque, namedtuple, ChainMap

def demonstrate_counter():
    """
    Counter: A dict subclass for counting hashable objects.
    """
    print("\n=== collections.Counter ===")

    # 1. Basic counting
    words = ['apple', 'banana', 'apple', 'cherry', 'apple', 'banana']
    count = Counter(words)
    print(f"Counts: {count}")

    # 2. Most common elements
    print(f"Most common (2): {count.most_common(2)}")

    # 3. Math operations on counters
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2)
    print(f"Add (c1+c2): {c1 + c2}")  # Adds counts
    print(f"Sub (c1-c2): {c1 - c2}")  # Subtracts, keeping only positive counts


def demonstrate_defaultdict():
    """
    defaultdict: dict subclass that calls a factory function to supply missing values.
    """
    print("\n=== collections.defaultdict ===")

    # 1. Grouping items (List factory)
    # Traditional way requires checking if key exists
    pairs = [('fruit', 'apple'), ('fruit', 'banana'), ('veg', 'carrot')]

    grouped = defaultdict(list)
    for category, item in pairs:
        grouped[category].append(item)

    print(f"Grouped: {dict(grouped)}")

    # 2. Counting (Int factory)
    # int() returns 0, perfect for counters
    char_counts = defaultdict(int)
    for char in "mississippi":
        char_counts[char] += 1
    print(f"Char counts: {dict(char_counts)}")


def demonstrate_deque():
    """
    deque: list-like container with fast appends and pops on either end.
    O(1) complexity for append/pop vs O(n) for list.pop(0).
    """
    print("\n=== collections.deque ===")

    d = deque(['middle'])

    # 1. Efficient append/pop on both ends
    d.append('right')
    d.appendleft('left')
    print(f"Deque: {d}")

    d.pop()      # remove right
    d.popleft()  # remove left
    print(f"After pops: {d}")

    # 2. Maxlen (Circular buffer)
    # useful for keeping "last N items" history
    history = deque(maxlen=3)
    for i in range(5):
        history.append(i)
        print(f"Added {i}, history: {list(history)}")


def demonstrate_namedtuple():
    """
    namedtuple: factory function for creating tuple subclasses with named fields.
    Memory efficient like tuples, readable like objects.
    """
    print("\n=== collections.namedtuple ===")

    Point = namedtuple('Point', ['x', 'y'])
    p = Point(10, 20)

    print(f"Point: {p}")
    print(f"Access by name: p.x = {p.x}, p.y = {p.y}")
    print(f"Access by index: p[0] = {p[0]}")


def demonstrate_chainmap():
    """
    ChainMap: dict-like class for creating a single view of multiple mappings.
    """
    print("\n=== collections.ChainMap ===")

    defaults = {'theme': 'dark', 'show_index': True}
    user_config = {'show_index': False}

    # Search order: user_config -> defaults
    config = ChainMap(user_config, defaults)

    print(f"Effective config: {config['theme']} (from defaults)")
    print(f"Effective config: {config['show_index']} (from user)")


if __name__ == "__main__":
    demonstrate_counter()
    demonstrate_defaultdict()
    demonstrate_deque()
    demonstrate_namedtuple()
    demonstrate_chainmap()

