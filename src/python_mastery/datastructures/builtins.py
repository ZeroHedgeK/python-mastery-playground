"""
Advanced Built-ins
=================

Mastering Python's built-in data structures is key to writing efficient and "Pythonic" code.
This module covers advanced slicing, comprehensions, and generators.
"""

import sys


def demonstrate_slicing():
    """
    Advanced Slicing techniques.
    Syntax: list[start:stop:step]
    """
    print("\n=== Advanced Slicing ===")
    numbers = list(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Original: {numbers}")

    # 1. Reverse a list
    print(f"Reverse [::-1]:       {numbers[::-1]}")

    # 2. Every second element
    print(f"Step 2 [::2]:         {numbers[::2]}")

    # 3. Slice assignment (modifying parts of the list)
    numbers[2:5] = [99, 99, 99]
    print(f"Slice assignment:     {numbers} (replaced index 2-5 with 99s)")

    # 4. Deleting slices
    del numbers[::2]
    print(f"Delete slice [::2]:   {numbers} (removed every 2nd element)")


def demonstrate_comprehensions():
    """
    List, Dictionary, and Set Comprehensions.
    More concise and often faster than loops.
    """
    print("\n=== Comprehensions ===")

    # 1. List Comprehension with filtering
    # Get squares of even numbers from 0 to 9
    evens_squared = [x**2 for x in range(10) if x % 2 == 0]
    print(f"List Comp (Even Squares): {evens_squared}")

    # 2. Dictionary Comprehension
    # Map number to its square
    squares_dict = {x: x**2 for x in range(5)}
    print(f"Dict Comp (Squares):      {squares_dict}")

    # 3. Set Comprehension
    # Unique lengths of words
    words = ["apple", "banana", "apple", "cherry", "date"]
    unique_lengths = {len(w) for w in words}
    print(f"Set Comp (Unique Lens):   {unique_lengths}")

    # 4. Nested Comprehension (Flattening a matrix)
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [num for row in matrix for num in row]
    print(f"Nested Comp (Flatten):    {flattened}")


def demonstrate_generators():
    """
    Generators and Generator Expressions.
    Memory efficient way to handle large datasets.
    """
    print("\n=== Generators ===")

    # 1. Generator Expression (Parentheses instead of brackets)
    # This doesn't create the list in memory
    gen_exp = (x**2 for x in range(1_000_000))
    print(f"Generator Size: {sys.getsizeof(gen_exp)} bytes (constant memory!)")

    # Compare with List Comprehension
    # list_comp = [x**2 for x in range(1_000_000)]
    # print(f"List Size:      {sys.getsizeof(list_comp)} bytes") # Would be ~8MB

    print(f"First item: {next(gen_exp)}")
    print(f"Next item:  {next(gen_exp)}")

    # 2. Generator Function (yield)
    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    print(f"Fibonacci(5): {list(fibonacci(5))}")


if __name__ == "__main__":
    demonstrate_slicing()
    demonstrate_comprehensions()
    demonstrate_generators()
