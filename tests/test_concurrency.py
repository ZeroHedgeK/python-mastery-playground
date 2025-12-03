"""
Tests for Concurrency Module
"""

import pytest
import asyncio
from concurrency.threading_demo import download_file
from concurrency.multiprocessing_demo import heavy_computation
from concurrency.asyncio_demo import fetch_data

# 1. Test Threading Logic (Sync function used by threads)
def test_download_task():
    """Test the individual task logic."""
    result = download_file(1)
    assert result == "file_1.dat"

# 2. Test Multiprocessing Logic (CPU bound function)
def test_heavy_computation():
    """Test the computation logic."""
    result = heavy_computation(5)  # 5! = 120
    assert result == 120

# 3. Test AsyncIO Logic (Coroutine)
@pytest.mark.asyncio
async def test_async_fetch():
    """Test the coroutine logic."""
    result = await fetch_data(99)
    assert result["id"] == 99
    assert result["data"] == "chunk"

# Note: We rely on 'pytest-asyncio' for the @pytest.mark.asyncio decorator.
# It should be installed or pytest might skip/fail this.
# Let's check if we have it, otherwise we might need to add it to setup.cfg extras.

