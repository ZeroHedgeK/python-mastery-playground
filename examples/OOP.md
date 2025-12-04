# OOP Examples

## Overview
Object-oriented patterns for extensibility and correctness: inheritance order, magic methods, advanced class mechanics, and metaclasses that enforce contracts.

## Prerequisites
- [ ] Classes, inheritance basics, and `super()`
- [ ] Python docs: [data model](https://docs.python.org/3/reference/datamodel.html)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `oop_inheritance.py` | MRO, diamond patterns, cooperative super | ⭐⭐ | 25-35 min |
| `oop_magic_methods.py` | Arithmetic/ordering dunders, container protocol | ⭐⭐ | 25-35 min |
| `oop_advanced_classes.py` | descriptors, slots, __init_subclass__, registries | ⭐⭐⭐ | 45-60 min |
| `oop_metaclasses.py` | metaclass creation hooks, validation, registries | ⭐⭐⭐ | 45-60 min |

## Study Order

> **Reasoning:** Understand method resolution and cooperation before customizing class creation.

1. **Start here:** `oop_inheritance.py`
   - *Goal:* Read MRO and avoid double-calls in diamonds.
   - *Key insight:* Cooperative `super()` prevents duplicate base invocations.

2. **Then:** `oop_magic_methods.py`
   - *Goal:* Implement rich behavior via dunders (add/iter/contains/callable).
   - *Key insight:* `__radd__` and `__iadd__` matter for interoperability.

3. **Then:** `oop_advanced_classes.py`
   - *Goal:* Encapsulate validation and behavior with descriptors/slots/hooks.
   - *Key insight:* `__init_subclass__` enforces subclass contracts.

4. **Advanced:** `oop_metaclasses.py`
   - *Goal:* Control class creation and auto-registration.
   - *Key insight:* Metaclasses should be minimal; prefer hooks when possible.

## Key Concepts

### Concept 1: MRO Visualization
**Where:** `oop_inheritance.py`, lines ~10-80
**What to notice:** Printed MRO shows diamond order; manual base calls cause double work.

### Concept 2: Container Protocol
**Where:** `oop_magic_methods.py`, lines ~60-120
**What to notice:** Implementing `__len__`, `__iter__`, `__getitem__`, `__contains__` makes custom classes iterable and usable with `in`/`len`.

### Concept 3: Descriptors and Slots
**Where:** `oop_advanced_classes.py`, lines ~60-150
**What to notice:** Descriptors enforce validation; slots cut instance overhead.

## Common Mistakes

### Mistake 1: Not Calling super()
**Symptom:** Bases not initialized, missing attributes.
**Fix:** Use cooperative `super()` as shown in `oop_inheritance.py`.

### Mistake 2: Missing `__radd__`
**Symptom:** `sum()` fails on custom numeric types.
**Fix:** Implement `__radd__`/`__iadd__` like `Money` in `oop_magic_methods.py`.

## Exercises

- [ ] **Exercise 1 (⭐):** Build a `Vector2D` supporting +, -, scalar *, repr, equality.
- [ ] **Exercise 2 (⭐⭐):** Implement `Observable` property with callbacks using descriptor protocol.
- [ ] **Exercise 3 (⭐⭐⭐):** Create a metaclass that auto-registers plugins and enforces required attributes.

## Connections

| Related Module | Connection |
|----------------|------------|
| [Testing](TESTING.md) | Protocols and fakes validate OOP interfaces |
| [Decorators](DECORATORS.md) | Decorators often wrap methods; `@classmethod`/`@staticmethod` are built-in decorators |
| [Internals](INTERNALS.md) | Slots and descriptors impact memory/layout |

## External Resources
- [PEP 3115](https://peps.python.org/pep-3115/) — Metaclasses in Python 3
- [Python Docs: Data Model](https://docs.python.org/3/reference/datamodel.html) — Magic methods and descriptors
- [Real Python: Metaclasses](https://realpython.com/python-metaclasses/) — Practical metaclass usage

---
*Estimated total time: ~3 hours | Last updated: 2025-12-04*
