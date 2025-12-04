# Functional Examples

## Overview
Functional techniques for clarity and composability: partial application, reduce/folds, itertools pipelines, and immutability to avoid side effects.

## Prerequisites
- [ ] Higher-order functions and lambda syntax
- [ ] Python docs: [functools](https://docs.python.org/3/library/functools.html), [itertools](https://docs.python.org/3/library/itertools.html)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `func_partial.py` | partials, currying helpers, compose patterns | ⭐⭐ | 25-35 min |
| `func_reduce.py` | reduce/folds vs loops, composition pipelines | ⭐⭐ | 25-35 min |
| `func_itertools.py` | Lazy combinators, grouping, slicing streams | ⭐⭐ | 25-35 min |
| `func_immutability.py` | Pure vs impure functions, frozen dataclasses | ⭐⭐ | 25-35 min |

## Study Order

> **Reasoning:** Build from composition tools to folds, then itertools, then purity.

1. **Start here:** `func_partial.py`
   - *Goal:* See how partials/currying reduce boilerplate in handlers.
   - *Key insight:* `partial` can hide arguments; use when it clarifies intent.

2. **Then:** `func_reduce.py`
   - *Goal:* Compare reduce to explicit loops; know when not to use it.
   - *Key insight:* Readability > cleverness; show loop equivalents.

3. **Then:** `func_itertools.py`
   - *Goal:* Use lazy tools (`chain`, `starmap`, `islice`, `groupby`).
   - *Key insight:* Some tools require sorted input (`groupby`).

4. **Advanced:** `func_immutability.py`
   - *Goal:* Separate pure functions from side effects; use frozen structures.
   - *Key insight:* Purity simplifies testing; mutation tracked for when it’s acceptable.

## Key Concepts

### Concept 1: Compose and Partial
**Where:** `func_partial.py`, lines ~10-70
**What to notice:** `compose` builds right-to-left pipelines; partial binds configs for handlers.

### Concept 2: Reduce vs Loop
**Where:** `func_reduce.py`, lines ~10-90
**What to notice:** Loop equivalents clarify when reduce is overkill.

### Concept 3: Immutability Trade-offs
**Where:** `func_immutability.py`, lines ~10-90
**What to notice:** Frozen dataclasses prevent mutation; demonstrates pure vs impure increments.

## Common Mistakes

### Mistake 1: Mutating Inside Reduce
**Symptom:** Hidden side effects; unexpected results.
**Fix:** Keep reducers pure and return new accumulators.

### Mistake 2: Using groupby on Unsorted Data
**Symptom:** Split groups unexpectedly.
**Fix:** Sort before groupby as shown in `func_itertools.py`.

## Exercises

- [ ] **Exercise 1 (⭐):** Implement `compose` that handles zero functions (returns identity).
- [ ] **Exercise 2 (⭐⭐):** Build `curry` decorator using `inspect.signature` to auto-curry functions.
- [ ] **Exercise 3 (⭐⭐⭐):** Implement a transducer pipeline combining map and filter transforms.

## Connections

| Related Module | Connection |
|----------------|------------|
| [Data Structures](DATA_STRUCTURES.md) | Generators supply lazy data to functional pipelines |
| [Testing](TESTING.md) | Pure functions simplify assertions and property tests |
| [Decorators](DECORATORS.md) | Decorators often leverage closures/partials |

## External Resources
- [Python Docs: functools](https://docs.python.org/3/library/functools.html) — partial, reduce
- [Real Python: itertools](https://realpython.com/python-itertools/) — Practical iterator recipes
- [Real Python: Functional Programming](https://realpython.com/python-functional-programming/) — Concepts and patterns

---
*Estimated total time: ~2 hours | Last updated: 2025-12-04*
