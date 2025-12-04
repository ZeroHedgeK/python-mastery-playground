"""
Tests for Datastructures Module
"""

from collections import Counter, deque


def test_generator_fibonacci():
    """Test the generator function manually."""

    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    result = list(fibonacci(5))
    assert result == [0, 1, 1, 2, 3]


def test_slicing_behavior():
    """Test basic slicing logic."""
    numbers = list(range(10))
    # Reverse
    assert numbers[::-1] == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    # Step
    assert numbers[::2] == [0, 2, 4, 6, 8]


def test_counter_logic():
    """Test Counter arithmetic."""
    c1 = Counter(a=3, b=1)
    c2 = Counter(a=1, b=2)

    # Addition
    sum_c = c1 + c2
    assert sum_c["a"] == 4
    assert sum_c["b"] == 3

    # Subtraction (keeps only positive)
    diff_c = c1 - c2
    assert diff_c["a"] == 2
    assert "b" not in diff_c  # 1 - 2 = -1, which is removed


def test_deque_maxlen():
    """Test deque circular buffer behavior."""
    d = deque(maxlen=3)
    for i in range(5):
        d.append(i)

    # Should have last 3 elements
    assert list(d) == [2, 3, 4]
