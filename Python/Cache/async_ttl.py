from functools import wraps
from time import monotonic
import traceback
from typing import Callable, Any
import logging
from random import randint
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# As `cachetools` don't work for async methods
def async_time_based_cache(ttl: int) -> Callable:
    """
    Decorator factory for creating a time-based cache for async functions.
    :param ttl: Time-to-live of cached items in seconds.
    :return: A decorator that can be applied to async functions for caching their results.
    """

    def decorator(func: Callable) -> Callable:
        cache: dict[tuple, tuple[float, Any]] = {}
        cache_lock = asyncio.Lock()

        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            """Wrapper function for caching with time-based invalidation."""
            cache_key = (args, tuple(sorted(kwargs.items())))
            current_time = monotonic()

            async with cache_lock:
                if cache_key in cache and current_time - cache[cache_key][0] < ttl:
                    logger.debug(
                        f"Async cache hit for {func.__name__} with args: {args} and kwargs: {kwargs}"
                    )
                    return cache[cache_key][1]

                try:
                    result = await func(*args, **kwargs)
                    cache[cache_key] = (current_time, result)
                    logger.debug(
                        f"Async cache miss - storing result for {func.__name__} with args: {args} and kwargs: {kwargs}"
                    )
                    return result
                except Exception:
                    logger.error(
                        f"Error in async cached function {func.__name__}: {traceback.print_exc()}"
                    )
                    raise

        def clear_cache() -> None:
            """Method to clear the cache manually."""
            with cache_lock:
                cache.clear()
                logger.info(f"Async cache cleared for {func.__name__}")

        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator


# Example usage
@async_time_based_cache(ttl=60)
async def async_generate_random_int() -> int:
    """Asynchronous function to generate a random integer."""
    # Some async operation
    await asyncio.sleep(1)
    return randint(0, 100)


async def main():
    rand_int1 = await async_generate_random_int()
    logger.info(f"Rand number is {rand_int1}")

    # A little delay might be needed to allow caching
    # await asyncio.sleep(0.010)

    rand_int2 = await async_generate_random_int()
    # Should be the same as rand_int1
    logger.info(f"Rand number is {rand_int2}")


asyncio.run(main())
