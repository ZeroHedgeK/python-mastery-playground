#! Python Mastery Challenges

Hands-on exercises to test your understanding of advanced Python concepts. Each challenge provides failing tests—your job is to make them pass.

## How It Works

```
challenges/
├── {module}/
│   ├── challenge_XX_name.py   ← Problem + failing tests
│   └── solution_XX_name.py    ← Reference implementation (no peeking!)
```

## Quick Start

```bash
# 1. Pick a challenge
python challenges/decorators/challenge_01_log_calls.py

# 2. See failing tests
#    ⬜ basic_functionality (not implemented)
#    ...

# 3. Implement the function in the challenge file

# 4. Run again until all tests pass
#    ✅ basic_functionality
#    🎉 ALL TESTS PASSED!

# 5. Compare with solution (optional)
cat challenges/decorators/solution_01_log_calls.py
```

## Progress Tracker

### Decorators
- [ ] `challenge_01_log_calls.py` — ⭐ 15-20 min
- [ ] `challenge_02_validate_args.py` — ⭐⭐ 25-35 min
- [ ] `challenge_03_memoize_async.py` — ⭐⭐⭐ 45-60 min

### Context Managers
- [ ] `challenge_01_temp_directory.py` — ⭐ 15-20 min
- [ ] `challenge_02_redirect_stdout.py` — ⭐⭐ 25-35 min
- [ ] `challenge_03_transaction.py` — ⭐⭐⭐ 45-60 min

### Data Structures (datastructures)
- [ ] `challenge_01_flatten.py` — ⭐ 15-20 min
- [ ] `challenge_02_group_by.py` — ⭐⭐ 25-35 min
- [ ] `challenge_03_lru_dict.py` — ⭐⭐⭐ 45-60 min

### OOP
- [ ] `challenge_01_vector.py` — ⭐ 20 min
- [ ] `challenge_02_observable.py` — ⭐⭐ 35 min
- [ ] `challenge_03_singleton_meta.py` — ⭐⭐⭐ 50-60 min

### Concurrency
- [ ] `challenge_01_parallel_map.py` — ⭐ 20 min
- [ ] `challenge_02_rate_limiter.py` — ⭐⭐ 30 min
- [ ] `challenge_03_producer_consumer.py` — ⭐⭐⭐ 60 min

### Control Flow
- [ ] `challenge_01_parse_config.py` — ⭐ 15-20 min
- [ ] `challenge_02_pipeline_builder.py` — ⭐⭐ 35 min
- [ ] `challenge_03_state_machine.py` — ⭐⭐⭐ 50-60 min

### Functional
- [ ] `challenge_01_compose.py` — ⭐ 15-20 min
- [ ] `challenge_02_curry.py` — ⭐⭐ 25-35 min
- [ ] `challenge_03_transducer.py` — ⭐⭐⭐ 45-60 min

### Internals
- [ ] `challenge_01_count_refs.py` — ⭐ 20 min
- [ ] `challenge_02_find_cycles.py` — ⭐⭐ 35 min
- [ ] `challenge_03_memory_profile.py` — ⭐⭐⭐ 45-60 min

### Testing Patterns (testing_patterns)
- [ ] `challenge_01_mock_time.py` — ⭐ 15-20 min
- [ ] `challenge_02_fake_filesystem.py` — ⭐⭐ 30 min
- [ ] `challenge_03_snapshot_test.py` — ⭐⭐⭐ 45-60 min

## Difficulty Guide

| Level | Symbol | Time | Description |
|-------|--------|------|-------------|
| Beginner | ⭐ | 15-20 min | Direct application of one concept |
| Intermediate | ⭐⭐ | 25-35 min | Combining concepts or edge cases |
| Advanced | ⭐⭐⭐ | 45-60 min | Production-level, deep understanding |

## Rules
1. **Don't look at solutions first** — struggle builds understanding.
2. **Tests are the spec** — read them carefully before coding.
3. **Hints are progressive** — try without hints first.
4. **Time limits are estimates** — learning matters more than speed.
5. **Ask why, not just how** — solutions explain the reasoning.

## Prerequisites

Complete the relevant `examples/` files before attempting challenges:

| Module | Required Examples |
|--------|-------------------|
| Decorators | `decorator_*.py` |
| Context Managers | `ctx_*.py` |
| Data Structures | `ds_*.py` |
| OOP | `oop_*.py` |
| Concurrency | `conc_*.py` |
| Control Flow | `flow_*.py` |
| Functional | `func_*.py` |
| Internals | `internals_*.py` |
| Testing Patterns | `test_*.py` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run from repo root, ensure `pip install -e .` |
| `SyntaxError` on `match` | Requires Python 3.10+ |
| Tests pass but solution differs | Multiple valid approaches exist |
| Stuck for >30 min | Read Hint 1, then Hint 2 |
## Challenge Suite

Hands-on exercises to practice concepts from the `python-mastery` examples. Each module has three progressively harder challenges (⭐ to ⭐⭐⭐). Every challenge file is runnable directly and contains inline tests; a corresponding solution file shows a reference implementation and key insights.

### How to use
- Open a challenge file, implement the `your_function` (and any helpers), and run the file: `python challenges/<module>/challenge_XX_<name>.py`.
- Tests will fail until you replace the `NotImplementedError` stubs.
- Compare with the matching solution file after attempting the challenge.

### Modules
- Decorators, Context Managers, Data Structures, OOP, Concurrency, Control Flow, Functional, Internals, Testing

### Time guidance
The `Time Estimate` in each file assumes familiarity with the example scripts; adjust as needed.
