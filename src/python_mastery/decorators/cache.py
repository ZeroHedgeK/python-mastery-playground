"""
cache_decorator.py - The @cache decorator implementation.

This module contains the @cache decorator that caches function results with TTL expiration.
Thread-safe implementation with optional LRU eviction and async function support.
"""

import asyncio
import functools
import logging
import threading
import time
from collections import OrderedDict
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def cache(ttl: float = 300.0, maxsize: int | None = None):
    """
    A decorator that caches function results with time-to-live expiration.

    This decorator stores function results and returns the cached value
    for subsequent calls with the same arguments, until the TTL expires.
    It's useful for expensive computations, API calls, or database queries.

    Features:
        - Thread-safe using threading.Lock
        - Optional LRU eviction when maxsize is set
        - Supports both sync and async functions

    Args:
        ttl: Time-to-live in seconds (default: 300.0 = 5 minutes)
        maxsize: Maximum number of cached entries. None means unlimited.
                 When exceeded, least recently used entries are evicted.

    Returns:
        A decorator that caches function results
    """

    def decorator(func: Callable) -> Callable:
        """
        The decorator that wraps the function with caching logic.

        Args:
            func: The function to be decorated

        Returns:
            A wrapper function with caching capability
        """

        # Thread-safe lock for cache operations
        lock = threading.Lock()

        # OrderedDict to store cached results with LRU ordering
        # Key: arguments tuple, Value: (result, timestamp)
        cache_store: OrderedDict[tuple, tuple[Any, float]] = OrderedDict()

        def _make_hashable(obj: Any) -> Any:
            """Convert an object to a hashable version."""
            if isinstance(obj, dict):
                return tuple(sorted((k, _make_hashable(v)) for k, v in obj.items()))
            if isinstance(obj, (list, set)):
                return tuple(_make_hashable(item) for item in obj)
            return obj

        def _make_key(args: tuple, kwargs: dict) -> tuple:
            """Create a hashable cache key from function arguments."""
            hashable_args = tuple(_make_hashable(arg) for arg in args)
            hashable_kwargs = tuple(
                sorted((k, _make_hashable(v)) for k, v in kwargs.items())
            )
            return (hashable_args, hashable_kwargs)

        def _get_cached(key: tuple, current_time: float) -> tuple[bool, Any]:
            """
            Check cache for valid entry. Returns (found, result).
            Must be called with lock held.
            """
            if key in cache_store:
                cached_result, timestamp = cache_store[key]
                if current_time - timestamp < ttl:
                    # Move to end for LRU ordering
                    cache_store.move_to_end(key)
                    return True, cached_result
                else:
                    # Cache expired, remove it
                    del cache_store[key]
            return False, None

        def _store_result(key: tuple, result: Any, current_time: float) -> None:
            """
            Store result in cache with LRU eviction.
            Must be called with lock held.
            """
            cache_store[key] = (result, current_time)
            cache_store.move_to_end(key)

            # Evict oldest entries if maxsize exceeded
            if maxsize is not None:
                while len(cache_store) > maxsize:
                    cache_store.popitem(last=False)

        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                """Async wrapper with thread-safe caching."""
                key = _make_key(args, kwargs)
                current_time = time.time()

                with lock:
                    found, cached_result = _get_cached(key, current_time)
                    if found:
                        logger.debug(
                            "Cache hit for %s%s, %s", func.__name__, args, kwargs
                        )
                        return cached_result

                # Cache miss - call the original async function outside lock
                logger.debug("Cache miss for %s%s, %s", func.__name__, args, kwargs)
                result = await func(*args, **kwargs)

                with lock:
                    _store_result(key, result, time.time())

                return result

            return async_wrapper
        else:

            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                """Sync wrapper with thread-safe caching."""
                key = _make_key(args, kwargs)
                current_time = time.time()

                with lock:
                    found, cached_result = _get_cached(key, current_time)
                    if found:
                        logger.debug(
                            "Cache hit for %s%s, %s", func.__name__, args, kwargs
                        )
                        return cached_result

                # Cache miss - call the original function outside lock
                logger.debug("Cache miss for %s%s, %s", func.__name__, args, kwargs)
                result = func(*args, **kwargs)

                with lock:
                    _store_result(key, result, time.time())

                return result

            return wrapper

    return decorator
