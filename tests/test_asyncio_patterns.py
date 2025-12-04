import asyncio

import pytest

from python_mastery.concurrency.asyncio_patterns import (
    bounded_gather,
    retry_async,
    run_blocking,
    stream_chunks,
    timeout_example,
)


@pytest.mark.asyncio
async def test_timeout_example():
    assert await timeout_example(0.01, timeout=0.05) is True
    assert await timeout_example(0.1, timeout=0.01) is False


@pytest.mark.asyncio
async def test_bounded_gather_limits_concurrency():
    work = [(1, 0.01), (2, 0.01), (3, 0.01), (4, 0.01)]
    results, peak = await bounded_gather(work, max_concurrent=2)
    assert results == [2, 4, 6, 8]
    assert peak <= 2


@pytest.mark.asyncio
async def test_stream_chunks():
    chunks = []
    async for chunk in stream_chunks("abcdef", 2):
        chunks.append(chunk)
    assert chunks == ["ab", "cd", "ef"]


@pytest.mark.asyncio
async def test_run_blocking_in_executor():
    def blocking_sum(values):
        return sum(values)

    result = await run_blocking(blocking_sum, [1, 2, 3])
    assert result == 6


@pytest.mark.asyncio
async def test_retry_async_backoff():
    attempts = {"count": 0}

    async def flaky():
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise RuntimeError("fail")
        return "ok"

    result = await retry_async(flaky, retries=3, base_delay=0.001)
    assert result == "ok"
    assert attempts["count"] == 3
