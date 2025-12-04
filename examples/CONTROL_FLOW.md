# Control Flow Examples

## Overview
Modern Python control flow with pattern matching, generator pipelines, and loop semantics that reduce boilerplate and clarify intent.

## Prerequisites
- [ ] Python 3.10+ for match/case
- [ ] Python docs: [match statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `flow_loops.py` | for/else, while/else, break/continue semantics | ⭐ | 15-20 min |
| `flow_pipelines.py` | Generator pipelines, yield from, lazy transforms | ⭐⭐ | 25-35 min |
| `flow_pattern_matching.py` | Structural patterns, guards, mapping/class patterns | ⭐⭐ | 25-35 min |

## Study Order

> **Reasoning:** Loop semantics first, then pipelines, then modern pattern matching.

1. **Start here:** `flow_loops.py`
   - *Goal:* Understand when loop `else` runs and nested break strategies.
   - *Key insight:* `else` executes only when no break occurs.

2. **Then:** `flow_pipelines.py`
   - *Goal:* Build lazy pipelines to avoid materializing lists.
   - *Key insight:* `yield from` flattens without nested loops.

3. **Advanced:** `flow_pattern_matching.py`
   - *Goal:* Route logic with match/case instead of brittle if/elif chains.
   - *Key insight:* Guards and OR patterns simplify complex dispatch.

## Key Concepts

### Concept 1: Loop Else
**Where:** `flow_loops.py`, lines ~10-70
**What to notice:** `for/else` used for search/validation without flags.

### Concept 2: Generator Pipelines
**Where:** `flow_pipelines.py`, lines ~10-80
**What to notice:** Compose emit→double→filter→accumulate lazily; memory stays small.

### Concept 3: Pattern Matching Guards
**Where:** `flow_pattern_matching.py`, lines ~10-90
**What to notice:** Guards (`case {"status": code} if code >= 500`) and OR patterns reduce nested if/elif noise.

## Common Mistakes

### Mistake 1: Missing Wildcard Case
**Symptom:** Unhandled inputs crash pattern matching.
**Fix:** Add `case _:` fallback as shown in `flow_pattern_matching.py`.

### Mistake 2: Breaking Pipeline Laziness
**Symptom:** Converting generator to list too early; memory spikes.
**Fix:** Keep pipeline as generators until final consumption (`flow_pipelines.py`).

## Exercises

- [ ] **Exercise 1 (⭐):** Write a config parser using match/case to map modes to actions.
- [ ] **Exercise 2 (⭐⭐):** Build a lazy pipeline that doubles numbers, filters odds, and sums lazily.
- [ ] **Exercise 3 (⭐⭐⭐):** Create a state machine using match/case transitions with guards for invalid events.

## Connections

| Related Module | Connection |
|----------------|------------|
| [Functional](FUNCTIONAL.md) | Pipelines mirror functional composition |
| [Decorators](DECORATORS.md) | Decorators often wrap control flow (e.g., retry) |
| [Concurrency](CONCURRENCY.md) | Async control flow uses the same match/guard patterns |

## External Resources
- [PEP 622](https://peps.python.org/pep-0622/) — Structural Pattern Matching
- [Python Docs: itertools](https://docs.python.org/3/library/itertools.html) — Helpers for pipelines
- [Real Python: Pattern Matching](https://realpython.com/python-pattern-matching/) — Practical match/case usage

---
*Estimated total time: ~2 hours | Last updated: 2025-12-04*
# Control Flow Examples

## Overview
Modern Python control flow with pattern matching, generator pipelines, and loop semantics that reduce boilerplate and clarify intent.

## Prerequisites
- [ ] Python 3.10+ for match/case
- [ ] Python docs: [match statement](https://docs.python.org/3/reference/compound_stmts.html#the-match-statement)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `flow_loops.py` | for/else, while/else, break/continue semantics | ⭐ | 15-20 min |
| `flow_pipelines.py` | Generator pipelines, yield from, lazy transforms | ⭐⭐ | 25-35 min |
| `flow_pattern_matching.py` | Structural patterns, guards, mapping/class patterns | ⭐⭐ | 25-35 min |

## Study Order

> **Reasoning:** Loop semantics first, then pipelines, then modern pattern matching.

1. **Start here:** `flow_loops.py`
   - *Goal:* Understand when loop `else` runs and nested break strategies.
   - *Key insight:* `else` executes only when no break occurs.

2. **Then:** `flow_pipelines.py`
   - *Goal:* Build lazy pipelines to avoid materializing lists.
   - *Key insight:* `yield from` flattens without nested loops.

3. **Advanced:** `flow_pattern_matching.py`
   - *Goal:* Route logic with match/case instead of brittle if/elif chains.
   - *Key insight:* Guards and OR patterns simplify complex dispatch.

## Key Concepts

### Concept 1: Loop Else
**Where:** `flow_loops.py`, lines ~10-70
**What to notice:** `for/else` used for search/validation without flags.

### Concept 2: Generator Pipelines
**Where:** `flow_pipelines.py`, lines ~10-80
**What to notice:** Compose emit→double→filter→accumulate lazily; memory stays small.

### Concept 3: Pattern Matching Guards
**Where:** `flow_pattern_matching.py`, lines ~10-90
**What to notice:** Guards (`case {
