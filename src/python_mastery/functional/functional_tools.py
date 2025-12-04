"""
Functional Tools
===============

Python provides powerful tools in 'functools' and 'itertools' to support
functional programming styles.
"""

import itertools
import operator
from functools import partial, reduce


def power(base, exponent):
    return base**exponent


def demonstrate_partial():
    """
    functools.partial: Creates a new function with some arguments pre-filled.
    """
    print("\n=== functools.partial ===")

    # Create a specialized function 'square' from general 'power'
    square = partial(power, exponent=2)

    # Create 'cube'
    cube = partial(power, exponent=3)

    print(f"Square of 5: {square(5)}")
    print(f"Cube of 5:   {cube(5)}")


def demonstrate_reduce():
    """
    functools.reduce: Applies a function cumulatively to items in a sequence.
    """
    print("\n=== functools.reduce ===")

    numbers = [1, 2, 3, 4, 5]

    # Calculate product: ((((1*2)*3)*4)*5)
    product = reduce(operator.mul, numbers)
    print(f"Product of {numbers}: {product}")

    # Custom reducer: Find max
    max_val = reduce(lambda a, b: a if a > b else b, numbers)
    print(f"Max of {numbers}: {max_val}")


def demonstrate_itertools():
    """
    itertools: Functions creating iterators for efficient looping.
    """
    print("\n=== itertools ===")

    # 1. Infinite Iterators (cycle)
    # Cycles through ABCD indefinitely (we break after 10)
    counter = 0
    result = []
    for char in itertools.cycle("ABCD"):
        result.append(char)
        counter += 1
        if counter >= 10:
            break
    print(f"Cycle 'ABCD' 10 times: {result}")

    # 2. Cartesian Product
    # Equivalent to nested loops
    colors = ["red", "blue"]
    sizes = ["S", "M"]
    combinations = list(itertools.product(colors, sizes))
    print(f"Product (Colors x Sizes): {combinations}")

    # 3. Chain (Combine iterables)
    list1 = [1, 2]
    list2 = [3, 4]
    chained = list(itertools.chain(list1, list2))
    print(f"Chained lists: {chained}")


if __name__ == "__main__":
    demonstrate_partial()
    demonstrate_reduce()
    demonstrate_itertools()
