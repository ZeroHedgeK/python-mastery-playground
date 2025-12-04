# Object-Oriented Programming Learning Guide

## Overview

This module covers advanced OOP concepts in Python that go beyond basic class definitions. Understanding these patterns is essential for writing maintainable, efficient, and Pythonic code.

## Core Concepts & Examples

1. **Advanced Classes** (`src/python_mastery/oop/advanced_classes.py`)

   - Singleton Pattern with `__new__`
   - Memory optimization with `__slots__`
   - Managed attributes with `@property`

2. **Inheritance & MRO** (`src/python_mastery/oop/inheritance.py`)

   - The Diamond Problem
   - C3 Linearization
   - Mixins

3. **Magic Methods** (`src/python_mastery/oop/magic_methods.py`)

   - Container protocols (`__len__`, `__getitem__`)
   - Operator overloading (`__add__`)
   - String representations (`__str__`, `__repr__`)

4. **Metaclasses** (`src/python_mastery/oop/metaclasses.py`)
   - Class factories
   - Attribute validation
   - Framework patterns

---

## 1. Advanced Class Mechanics

### Singleton Pattern with `__new__`

The Singleton pattern ensures only one instance of a class exists.

```python
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value: str) -> None:
        self.value = value

# Usage
s1 = Singleton("first")
s2 = Singleton("second")
print(s1 is s2)  # True - same object!
print(s1.value)  # "second" - __init__ called twice!
```

**Key Insight**: `__new__` creates the instance, `__init__` initializes it. Both are called when you instantiate a class.

### Memory Optimization with `__slots__`

By default, Python stores instance attributes in a `__dict__`. Using `__slots__` pre-allocates fixed memory.

```python
class RegularPoint:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ["x", "y"]

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

# SlottedPoint uses ~40% less memory per instance
# But: cannot add new attributes dynamically
```

**When to Use**:

- Creating millions of instances (data classes, records)
- Memory-constrained environments
- Performance-critical code

**Trade-offs**:

- No dynamic attribute addition
- No `__dict__` (can't use `vars(obj)`)
- Inheritance requires careful handling

### Managed Attributes with `@property`

Properties allow getter/setter logic while maintaining attribute-like syntax.

```python
class BankAccount:
    def __init__(self, balance: float) -> None:
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative!")
        self._balance = value

# Usage - looks like attribute access
account = BankAccount(100)
print(account.balance)    # Calls getter
account.balance = 200     # Calls setter with validation
account.balance = -50     # Raises ValueError
```

---

## 2. Inheritance & Method Resolution Order (MRO)

### The Diamond Problem

When a class inherits from two classes that share a common ancestor:

```
     A
    / \
   B   C
    \ /
     D
```

Python uses **C3 Linearization** to determine method lookup order.

```python
class A:
    def speak(self) -> None:
        print("A")

class B(A):
    def speak(self) -> None:
        print("B")
        super().speak()

class C(A):
    def speak(self) -> None:
        print("C")
        super().speak()

class D(B, C):
    def speak(self) -> None:
        print("D")
        super().speak()

print(D.mro())  # [D, B, C, A, object]

D().speak()
# Output: D, B, C, A (each called once!)
```

**Key Rule**: `super()` follows the MRO, not the direct parent.

### Mixins

Mixins are small, focused classes that add specific functionality.

```python
import json

class JsonMixin:
    """Adds JSON serialization to any class."""
    def to_json(self) -> str:
        return json.dumps(self.__dict__)

class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

class JsonPerson(JsonMixin, Person):
    pass

p = JsonPerson("Alice", 30)
print(p.to_json())  # {"name": "Alice", "age": 30}
```

**Mixin Guidelines**:

- Should not have `__init__` (or call `super().__init__()`)
- Should not have state (instance attributes)
- Should provide a single, focused capability
- Name should end with `Mixin` for clarity

---

## 3. Magic Methods (Dunder Methods)

Magic methods make your objects behave like built-in types.

### Container Protocol

```python
class CustomList:
    def __init__(self, *args) -> None:
        self._data = list(args)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, index: int):
        return self._data[index]

    def __setitem__(self, index: int, value) -> None:
        self._data[index] = value

    def __iter__(self):
        return iter(self._data)

# Now works with built-in functions
cl = CustomList(1, 2, 3)
print(len(cl))      # 3
print(cl[0])        # 1
for item in cl:     # Iteration works
    print(item)
```

### Operator Overloading

```python
class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)      # Vector(4, 6)
print(v1 * 3)       # Vector(3, 6)
```

### String Representations

```python
class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """For end users (print, str())"""
        return self.name

    def __repr__(self) -> str:
        """For developers (debugging, logging)"""
        return f"User(name={self.name!r}, email={self.email!r})"
```

---

## 4. Metaclasses

Metaclasses are "classes of classes" - they define how classes are created.

```python
class ValidatedMeta(type):
    """Metaclass that enforces uppercase attribute names."""

    def __new__(mcs, name: str, bases: tuple, attrs: dict) -> type:
        for key, value in attrs.items():
            if not key.startswith("_") and not callable(value):
                if not key.isupper():
                    raise TypeError(f"Attribute '{key}' must be uppercase")
        return super().__new__(mcs, name, bases, attrs)

class Config(metaclass=ValidatedMeta):
    MAX_CONNECTIONS = 100  # OK
    TIMEOUT = 30           # OK
    # host = "localhost"   # Would raise TypeError!
```

**Use Cases**:

- ORM frameworks (Django models)
- API validation frameworks
- Singleton enforcement
- Automatic registration of subclasses

**Guidelines**:

- Most developers never need to write metaclasses
- Consider `__init_subclass__` for simpler class customization
- Consider class decorators as an alternative

---

## Running Examples

```bash
# Run individual module demonstrations
python -m python_mastery.oop.advanced_classes
python -m python_mastery.oop.inheritance
python -m python_mastery.oop.magic_methods
python -m python_mastery.oop.metaclasses

# Or use the interactive CLI
python -m python_mastery
# Select: 3. Object-Oriented Programming
```

---

## Best Practices

1. **Prefer composition over inheritance** when possible
2. **Use `__slots__` sparingly** - only when memory matters
3. **Always implement `__repr__`** for debugging
4. **Follow the MRO** when using `super()`
5. **Avoid metaclasses** unless building a framework
6. **Use `@property`** for computed or validated attributes
