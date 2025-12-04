# Internals Examples

## Overview
Peek under the hood of CPython: bytecode, refcounts, garbage collection, and memory sizing. These examples explain performance characteristics and pitfalls like uncollectable cycles.

## Prerequisites
- [ ] Familiarity with CPython specifics (not guaranteed on other interpreters)
- [ ] Python docs: [dis](https://docs.python.org/3/library/dis.html), [gc](https://docs.python.org/3/library/gc.html), [sys](https://docs.python.org/3/library/sys.html)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `internals_bytecode.py` | Disassembly, LOAD_FAST vs LOAD_GLOBAL, constant folding | ⭐⭐ | 25-35 min |
| `internals_refcount.py` | Refcount +1 rule, weakrefs, interning | ⭐⭐ | 25-35 min |
| `internals_gc.py` | Generational GC, cycles, callbacks, disable/enable | ⭐⭐ | 25-35 min |
| `internals_memory.py` | getsizeof limits, slots savings, tracemalloc snapshots | ⭐⭐ | 25-35 min |

## Study Order

> **Reasoning:** Start with execution (bytecode), then lifetime (refcount/GC), then sizing.

1. **Start here:** `internals_bytecode.py`
   - *Goal:* See how Python executes your code.
   - *Key insight:* LOCALS vs GLOBALS affect opcode choice and speed.

2. **Then:** `internals_refcount.py`
   - *Goal:* Understand reference increments and caching.
   - *Key insight:* `sys.getrefcount` reports +1 while inspecting.

3. **Then:** `internals_gc.py`
   - *Goal:* Observe generational collection and cycle handling.
   - *Key insight:* `gc.collect()` return value signals collected objects.

4. **Advanced:** `internals_memory.py`
   - *Goal:* Measure container sizes, slots benefits, and allocations.
   - *Key insight:* `getsizeof` is shallow; recursive sizing differs.

## Key Concepts

### Concept 1: Opcode Costs
**Where:** `internals_bytecode.py`, lines ~10-80
**What to notice:** LOAD_FAST cheaper than LOAD_GLOBAL; comprehension bytecode shows BUILD_LIST/APPEND.

### Concept 2: Refcount +1
**Where:** `internals_refcount.py`, lines ~10-70
**What to notice:** `getrefcount` temporarily bumps counts; weakrefs don’t.

### Concept 3: GC Generations
**Where:** `internals_gc.py`, lines ~10-80
**What to notice:** Collecting cycles via `gc.collect()`; callbacks show phases.

## Common Mistakes

### Mistake 1: Misreading getsizeof
**Symptom:** Assuming getsizeof includes contents.
**Fix:** Use recursive sizing like shown in `internals_memory.py`.

### Mistake 2: Creating Uncollectable Cycles with __del__
**Symptom:** Objects stick in `gc.garbage`.
**Fix:** Avoid `__del__` or break cycles; see `internals_gc.py`.

## Exercises

- [ ] **Exercise 1 (⭐):** Disassemble a function with list comprehension and compare to map/sum.
- [ ] **Exercise 2 (⭐⭐):** Write `count_refs(obj)` subtracting the observer refcount.
- [ ] **Exercise 3 (⭐⭐⭐):** Implement a memory profiler decorator using `tracemalloc` snapshots.

## Connections

| Related Module | Connection |
|----------------|------------|
| [Concurrency](CONCURRENCY.md) | GIL behavior comes from bytecode execution model |
| [Data Structures](DATA_STRUCTURES.md) | Memory insights guide container choice |
| [Testing](TESTING.md) | Profilers and refcount checks help detect leaks |

## External Resources
- [Python Docs: dis](https://docs.python.org/3/library/dis.html) — Bytecode inspection
- [Python Docs: gc](https://docs.python.org/3/library/gc.html) — Garbage collector controls
- [Real Python: Memory Management](https://realpython.com/python-memory-management/) — Practical overview

---
*Estimated total time: ~2.5 hours | Last updated: 2025-12-04*
