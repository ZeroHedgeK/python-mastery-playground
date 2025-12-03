"""
Magic Methods (Dunder Methods)
=============================

This module demonstrates how to make classes behave like built-in types using
double-underscore (dunder) methods.
"""

class CustomList:
    """
    A custom list-like container that supports indexing and iteration.
    """
    def __init__(self, *args):
        self._data = list(args)

    def __len__(self):
        """Called by len(obj)"""
        return len(self._data)

    def __getitem__(self, index):
        """Called by obj[index]"""
        return self._data[index]

    def __setitem__(self, index, value):
        """Called by obj[index] = value"""
        self._data[index] = value

    def __str__(self):
        """Called by str(obj) or print(obj) (End-user string)"""
        return f"CustomList({self._data})"

    def __repr__(self):
        """Called by repr(obj) (Developer string)"""
        return f"CustomList(*{self._data})"

    def __add__(self, other):
        """Called by obj + other"""
        if isinstance(other, CustomList):
            return CustomList(*(self._data + other._data))
        return NotImplemented


def demonstrate_magic_methods():
    print("\n=== Magic Methods (Custom Container) ===")

    cl1 = CustomList(1, 2, 3)
    print(f"Created: {cl1}")
    print(f"Length: {len(cl1)}")

    print(f"Index 1: {cl1[1]}")
    cl1[1] = 99
    print(f"Modified: {cl1}")

    cl2 = CustomList(4, 5)
    cl3 = cl1 + cl2
    print(f"Added lists: {cl3}")


if __name__ == "__main__":
    demonstrate_magic_methods()

