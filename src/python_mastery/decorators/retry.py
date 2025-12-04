"""
retry_decorator.py - The @retry decorator implementation.

This module contains the @retry decorator that retries failed functions.
Supports both sync and async functions with configurable retry strategies.
"""

import asyncio
import functools
import logging
import time
from collections.abc import Callable
from typing import Any

from python_mastery.exceptions import RetryExhausted

logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    backoff: float = 1.0,
):
    """
    A decorator that retries a function if it fails.

    This decorator will catch exceptions and retry the function multiple times
    before giving up. It's useful for network calls, file operations, or any
    function that might fail temporarily.

    Features:
        - Supports both sync and async functions
        - Configurable exponential backoff
        - Raises RetryExhausted with original exception preserved

    Args:
        max_attempts: Maximum number of times to try the function (default: 3)
        delay: Initial seconds to wait between retries (default: 1.0)
        exceptions: Tuple of exception types to catch and retry on (default: (Exception,))
        backoff: Multiplier for delay after each attempt (default: 1.0, no backoff)
                 Use 2.0 for exponential backoff (delay doubles each retry)

    Returns:
        A decorator that wraps the function with retry logic

    Raises:
        RetryExhausted: When all retry attempts fail (wraps the last exception)
    """

    def decorator(func: Callable) -> Callable:
        """
        The decorator that wraps the function with retry logic.

        Args:
            func: The function to be decorated

        Returns:
            A wrapper function with retry capability
        """

        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                """Async wrapper with retry logic."""
                attempts = 0
                current_delay = delay
                last_exception: Exception = RuntimeError("No attempts made")

                while attempts < max_attempts:
                    attempts += 1

                    try:
                        result = await func(*args, **kwargs)
                        if attempts > 1:
                            logger.info(
                                "Function '%s' succeeded on attempt %d",
                                func.__name__,
                                attempts,
                            )
                        return result

                    except exceptions as e:
                        last_exception = e

                        if attempts == max_attempts:
                            logger.error(
                                "Function '%s' failed after %d attempts",
                                func.__name__,
                                max_attempts,
                            )
                            raise RetryExhausted(
                                func.__name__, max_attempts, e
                            ) from e

                        logger.warning(
                            "Function '%s' failed on attempt %d: %s",
                            func.__name__,
                            attempts,
                            e,
                        )
                        logger.debug("Retrying in %.1f seconds...", current_delay)

                        await asyncio.sleep(current_delay)
                        current_delay *= backoff

                # Should never reach here
                raise RetryExhausted(func.__name__, max_attempts, last_exception)

            return async_wrapper
        else:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                """Sync wrapper with retry logic."""
                attempts = 0
                current_delay = delay
                last_exception: Exception = RuntimeError("No attempts made")

                while attempts < max_attempts:
                    attempts += 1

                    try:
                        result = func(*args, **kwargs)
                        if attempts > 1:
                            logger.info(
                                "Function '%s' succeeded on attempt %d",
                                func.__name__,
                                attempts,
                            )
                        return result

                    except exceptions as e:
                        last_exception = e

                        if attempts == max_attempts:
                            logger.error(
                                "Function '%s' failed after %d attempts",
                                func.__name__,
                                max_attempts,
                            )
                            raise RetryExhausted(
                                func.__name__, max_attempts, e
                            ) from e

                        logger.warning(
                            "Function '%s' failed on attempt %d: %s",
                            func.__name__,
                            attempts,
                            e,
                        )
                        logger.debug("Retrying in %.1f seconds...", current_delay)

                        time.sleep(current_delay)
                        current_delay *= backoff

                # Should never reach here
                raise RetryExhausted(func.__name__, max_attempts, last_exception)

            return wrapper

    return decorator
