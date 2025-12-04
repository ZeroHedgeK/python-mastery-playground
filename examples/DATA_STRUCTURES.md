# Data Structures Examples

## Overview
Focus on Python collections for clarity and efficiency: comprehensions, generators, slicing, and specialized containers that impact performance and readability.

## Prerequisites
- [ ] Lists, dicts, and slicing basics
- [ ] Python docs: [collections](https://docs.python.org/3/library/collections.html)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `ds_comprehensions.py` | Imperative vs comprehension, filtering, nesting | ⭐ | 15-20 min |
| `ds_generators.py` | Lazy pipelines, send(), memory footprint | ⭐⭐ | 25-35 min |
| `ds_slicing.py` | Step/negative slices, custom `__getitem__`, slice assignment | ⭐⭐ | 25-35 min |
| `ds_collections.py` | Counter/defaultdict/deque/namedtuple/ChainMap use-cases | ⭐⭐ | 25-35 min |

## Study Order

> **Reasoning:** Start with syntax (comprehensions), then laziness (generators), then slicing mechanics, then specialized containers.

1. **Start here:** `ds_comprehensions.py`
   - *Goal:* Recognize when comprehensions beat loops for clarity.
   - *Key insight:* Filtering + transform in one pass clarifies intent.

2. **Then:** `ds_generators.py`
   - *Goal:* Appreciate memory savings of lazy pipelines.
   - *Key insight:* Generators keep size small regardless of range size.

3. **Then:** `ds_slicing.py`
   - *Goal:* Use slices for clean subrange logic and custom types.
   - *Key insight:* `__getitem__` can honor slices to preserve type.

4. **Advanced:** `ds_collections.py`
   - *Goal:* Pick the right container for grouping, buffering, layering config.
   - *Key insight:* deque O(1) pops vs list O(n); ChainMap layering order.

## Key Concepts

### Concept 1: Lazy vs Eager
**Where:** `ds_generators.py`, lines ~10-50
**What to notice:** `sys.getsizeof` shows generator stays tiny; list would scale.
**Try this:** Change range to 10_000_000; generator size barely changes.

### Concept 2: Slice Semantics
**Where:** `ds_slicing.py`, lines ~40-90
**What to notice:** Custom `WindowedSeries.__getitem__` returns same type on slices.
**Try this:** Add another slice and call `.sum()` to confirm type preservation.

### Concept 3: Declarative Grouping
**Where:** `ds_comprehensions.py`, lines ~15-60
**What to notice:** Side-by-side imperative vs comprehension emphasizes readability and fewer bugs.

## Common Mistakes

### Mistake 1: Exhausting Generators Twice
**Symptom:** Second iteration yields nothing.
**Fix:** Re-create generator or materialize once; shown in `ds_generators.py`.

### Mistake 2: Mutating During Iteration
**Symptom:** Skipped elements or runtime errors.
**Fix:** Build new collections via comprehensions instead of in-loop mutation.

## Exercises

- [ ] **Exercise 1 (⭐):** Flatten nested lists with recursion or stack; verify on mixed depths.
- [ ] **Exercise 2 (⭐⭐):** Implement `group_by` returning ordered dict; reuse patterns from `ds_collections.py`.
- [ ] **Exercise 3 (⭐⭐⭐):** Build an LRU dict using `OrderedDict.move_to_end`; ensure eviction order matches access.

## Connections

| Related Module | Connection |
|----------------|------------|
| [Functional](FUNCTIONAL.md) | Generators feed functional pipelines |
| [Internals](INTERNALS.md) | Memory sizing (`getsizeof`) clarifies container costs |
| [Concurrency](CONCURRENCY.md) | Iterables feeding worker pools benefit from laziness |

## External Resources
- [Python Docs: itertools](https://docs.python.org/3/library/itertools.html) — Building blocks for iteration
- [Real Python: List Comprehensions](https://realpython.com/list-comprehension-python/) — Comprehension patterns
- [Python Docs: collections](https://docs.python.org/3/library/collections.html) — Specialized containers

---
*Estimated total time: ~2 hours | Last updated: 2025-12-04*
