import asyncio
from collections import OrderedDict
from functools import wraps
from random import randint
from typing import Any, Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncLRUCache:
    def __init__(self, maxsize: int):
        self.cache = OrderedDict()
        self.maxsize = maxsize
        self.lock = asyncio.Lock()

    async def get(self, key: tuple) -> Any:
        async with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                logger.info(f"LRU Cache hit for key: {key}")
                return self.cache[key]
            logger.info(f"LRU Cache miss for key: {key}")
            return None

    async def put(self, key: tuple, value: Any) -> None:
        async with self.lock:
            self.cache[key] = value
            self.cache.move_to_end(key)
            if len(self.cache) > self.maxsize:
                removed_key = self.cache.popitem(last=False)
                logger.info(
                    f"LRU Cache evicted least recently used item: {removed_key}"
                )

    async def clear(self) -> None:
        async with self.lock:
            self.cache.clear()
            logger.info("LRU Cache cleared")


def async_lru_cache(maxsize: int = 1024) -> Callable:
    """
    Decorator factory for creating an LRU cache for async functions.
    :param maxsize: Maximum size of the cache.
    :return: A decorator that can be applied to async functions for caching their results.
    """
    cache = AsyncLRUCache(maxsize)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            cached_result = await cache.get(key)
            if cached_result is not None:
                return cached_result

            try:
                result = await func(*args, **kwargs)
                await cache.put(key, result)
                return result
            except Exception as e:
                logger.error(f"Error in async LRU cached function {func.__name__}: {e}")
                raise

        wrapper.clear_cache = cache.clear  # Attach the clear method to the wrapper
        return wrapper

    return decorator


# Example usage
@async_lru_cache(maxsize=2)
async def async_generate_random_int(end_range: int) -> int:
    """Asynchronous function to generate a random integer."""
    # Some async operation
    await asyncio.sleep(1)
    return randint(0, end_range)


async def main():
    rand_int1 = await async_generate_random_int(100)
    logger.info(f"Rand number 1 is {rand_int1}")

    # A little delay might be needed to allow caching
    # await asyncio.sleep(0.010)
    rand_int2 = await async_generate_random_int(200)
    logger.info(f"Rand number 2 is {rand_int2}")

    # Evicts first value so range 100 would produce a different value
    rand_int3 = await async_generate_random_int(300)
    logger.info(f"Rand number 3 is {rand_int3}")

    rand_int22 = await async_generate_random_int(200)
    logger.info(f"Rand number 2 is {rand_int22}")


asyncio.run(main())
