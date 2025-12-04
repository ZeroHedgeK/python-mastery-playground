# Testing Examples

## Overview
Testing patterns with pytest: fixtures, mocking, type-safety checks, and strategy design to keep tests reliable and maintainable.

## Prerequisites
- [ ] pytest installed and basic usage
- [ ] Python docs: [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## Files in This Module

| File | What You'll Learn | Difficulty | Time |
|------|-------------------|------------|------|
| `test_fixtures.py` | Fixture scopes, parametrization, async fixtures | ⭐⭐ | 25-35 min |
| `test_mocking.py` | Patch location rules, MagicMock vs Mock, DI over patch | ⭐⭐ | 25-35 min |
| `test_type_safety.py` | Protocols, TypedDict, Literal/Final in tests | ⭐⭐ | 25-35 min |
| `test_strategies.py` | AAA pattern, markers, edge/invariant tests | ⭐⭐ | 25-35 min |

## Study Order

> **Reasoning:** Start with fixtures, then mocking, then type-safety and strategy patterns.

1. **Start here:** `test_fixtures.py`
   - *Goal:* Understand fixture lifecycle and parametrization.
   - *Key insight:* Scope controls setup/teardown frequency.

2. **Then:** `test_mocking.py`
   - *Goal:* Patch correctly and favor DI where possible.
   - *Key insight:* Patch where used, not where defined.

3. **Then:** `test_type_safety.py`
   - *Goal:* Use Protocols and TypedDict to validate fakes.
   - *Key insight:* `isinstance` with `@runtime_checkable` Protocols verifies doubles.

4. **Advanced:** `test_strategies.py`
   - *Goal:* Structure tests with AAA and markers; cover edge/invariant cases.
   - *Key insight:* Markers slice suites; invariants expose hidden bugs.

## Key Concepts

### Concept 1: Fixture Scope
**Where:** `test_fixtures.py`, lines ~10-80
**What to notice:** Session/module/function scopes print lifecycle; yields show teardown.

### Concept 2: Patch Location Rule
**Where:** `test_mocking.py`, lines ~20-70
**What to notice:** Patch where attribute is looked up; DI often simpler than patching.

### Concept 3: Protocol-based Fakes
**Where:** `test_type_safety.py`, lines ~10-70
**What to notice:** Protocols allow `isinstance(fake, Protocol)` checks; TypedDict enforces keys.

## Common Mistakes

### Mistake 1: Patching the Wrong Target
**Symptom:** Mock not used; real network/file call happens.
**Fix:** Patch where imported/used (module path), demonstrated in `test_mocking.py`.

### Mistake 2: Overusing Global Fixtures
**Symptom:** Hidden coupling between tests.
**Fix:** Prefer function-scoped fixtures unless cost requires broader scope.

## Exercises

- [ ] **Exercise 1 (⭐):** Write `mock_time` context to freeze `time.time` in tests.
- [ ] **Exercise 2 (⭐⭐):** Build `FakeFS` with read/write/exist methods for tests.
- [ ] **Exercise 3 (⭐⭐⭐):** Implement snapshot testing helper that writes once then compares output on subsequent runs.

## Connections

| Related Module | Connection |
|----------------|------------|
| [OOP](OOP.md) | Protocols define interfaces that tests verify |
| [Decorators](DECORATORS.md) | Wrapping functions can complicate patching if metadata lost |
| [Internals](INTERNALS.md) | Refcount/memory checks can detect leaks during testing |

## External Resources
- [pytest Docs](https://docs.pytest.org/) — Fixtures, markers, parametrize
- [Python Docs: unittest.mock](https://docs.python.org/3/library/unittest.mock.html) — Mocking tools
- [Real Python: pytest](https://realpython.com/pytest-python-testing/) — Practical pytest guide

---
*Estimated total time: ~2 hours | Last updated: 2025-12-04*
