"""
Challenge: transducer
Difficulty: ⭐⭐⭐
Time Estimate: 25 minutes
Concepts: functional composition, reducers

Problem:
Implement a simple transducer pipeline that composes mapper and filter
transforms and applies them to a reducer.

Requirements:
1. `compose_transforms(*transforms)` returns a function that, given a reducer,
   returns a new reducer applying transforms first.
2. Provide helpers `mapping(fn)` and `filtering(pred)` that create transforms.
3. `transduce(data, xf, reducer, init)` applies the composed reducer over data.

Hints:
- A transform is a function that takes a reducer and returns a new reducer.

Run tests:
    python challenges/functional/challenge_03_transducer.py
"""

from __future__ import annotations


# === YOUR CODE HERE ===


def compose_transforms(*transforms):
    raise NotImplementedError("Your implementation here")


def mapping(fn):
    raise NotImplementedError("Your implementation here")


def filtering(pred):
    raise NotImplementedError("Your implementation here")


def transduce(data, xf, reducer, init):
    raise NotImplementedError("Your implementation here")


# === TESTS (DO NOT MODIFY BELOW THIS LINE) ===


def test_transducer_pipeline():
    xf = compose_transforms(mapping(lambda x: x * 2), filtering(lambda x: x > 2))

    def reducer(acc, val):
        acc.append(val)
        return acc

    result = transduce([1, 2, 3], xf, reducer, [])
    assert result == [4, 6]


if __name__ == "__main__":
    import sys

    try:
        test_transducer_pipeline()
        print("✅ test_transducer_pipeline passed")
    except (AssertionError, NotImplementedError) as e:
        print(f"❌ test_transducer_pipeline failed: {e}")
        sys.exit(1)

    print("\n🎉 All tests passed!")
