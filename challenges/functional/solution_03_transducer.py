"""
Solution: transducer

Key Insights:
1. A transform wraps a reducer, adding pre-processing (map) or conditional
   forwarding (filter).
2. compose_transforms applies transforms right-to-left so the first argument is
   the outermost transformation.
3. transduce runs the composed reducer over the data, threading the accumulator.

Alternative Approaches:
- Chain generator expressions; transducers keep data flow reducer-driven.
"""

from __future__ import annotations

from typing import Callable, Iterable, Any


# === SOLUTION ===


def compose_transforms(*transforms):
    def composed(reducer):
        wrapped = reducer
        for xf in reversed(transforms):
            wrapped = xf(wrapped)
        return wrapped

    return composed


def mapping(fn):
    def transform(reducer):
        def new_reducer(acc, val):
            return reducer(acc, fn(val))

        return new_reducer

    return transform


def filtering(pred):
    def transform(reducer):
        def new_reducer(acc, val):
            if pred(val):
                return reducer(acc, val)
            return acc

        return new_reducer

    return transform


def transduce(data: Iterable[Any], xf, reducer: Callable, init: Any):
    reduce_fn = xf(reducer)
    acc = init
    for item in data:
        acc = reduce_fn(acc, item)
    return acc


# === VERIFICATION ===


def test_transducer_pipeline():
    xf = compose_transforms(mapping(lambda x: x * 2), filtering(lambda x: x > 2))

    def reducer(acc, val):
        acc.append(val)
        return acc

    result = transduce([1, 2, 3], xf, reducer, [])
    assert result == [4, 6]


if __name__ == "__main__":
    test_transducer_pipeline()
    print("✅ test_transducer_pipeline passed")
    print("\n🎉 All tests passed!")
