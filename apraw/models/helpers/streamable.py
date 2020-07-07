import asyncio
from functools import update_wrapper
from typing import AsyncIterator, Callable, Any, Union, AsyncGenerator, Generator, Iterator, Awaitable

from .apraw_base import aPRAWBase
from ...utils import ExponentialCounter

# I know, I know, this code is cursed
SYNC_OR_ASYNC_ITERABLE = Union[
    Callable[[Any, int, Any], Union[Awaitable[Union[AsyncIterator[aPRAWBase], Iterator[aPRAWBase]]], Union[
        AsyncIterator[aPRAWBase], Iterator[aPRAWBase]]]], AsyncGenerator[aPRAWBase, None], Generator[
        aPRAWBase, None, None]]


class Streamable:
    """
    A decorator to make functions returning a generator streamable.

    Members
    -------
    max_wait: int
        The maximum amount of seconds to wait before repolling the function.
    attribute_name: str
        The attribute name to use as a unique identifier for returned objects.
    """

    @classmethod
    def streamable(cls, func: SYNC_OR_ASYNC_ITERABLE = None, max_wait: int = 16, attribute_name: str = "fullname"):
        if func:
            return Streamable(func)
        else:
            def wrapper(
                    _func: SYNC_OR_ASYNC_ITERABLE):
                return Streamable(_func, max_wait, attribute_name)

            return wrapper

    def __init__(self, func: SYNC_OR_ASYNC_ITERABLE, max_wait: int = 16, attribute_name: str = "fullname"):
        """
        Create an instance of the streamable object.

        Parameters
        ----------
        func: Callable[[Any, int, Any], AsyncIterator[Any]]
            The function returning an asynchronous iterator.
        max_wait: int
            The maximum amount of seconds to wait before repolling the function.
        attribute_name: str
            The attribute name to use as a unique identifier for returned objects.
        """
        self._func = func
        update_wrapper(self, func)

        self.max_wait = max_wait
        self.attribute_name = attribute_name

    def __get__(self, instance: Any, owner: Any):
        """
        Allow streamable to access its top-level object instance to forward to functions later.
        """
        self.instance = instance
        return self

    async def __call__(self, *args, **kwargs):
        """
        Make streamable callable to return result of decorated function.
        """
        if hasattr(self._func, "__call__"):
            func_args = (self.instance, *args) if hasattr(self, "instance") else args
            if asyncio.iscoroutinefunction(self._func):
                iterable = await self._func(*func_args, **kwargs)
            else:
                iterable = self._func(*func_args, **kwargs)
        else:
            iterable = self._func

        if hasattr(iterable, "__aiter__"):
            async for item in iterable:
                yield item
        else:
            for item in iterable:
                yield item

    async def stream(self, skip_existing: bool = False, *args, **kwargs):
        r"""
        Call the stream method on the decorated function.

        Parameters
        ----------
        skip_existing: bool
            Whether items found before the function call should be returned as well.
        kwargs: \*\*Dict
            ``kwargs`` to be passed on to the function.

        Yields
        ------
        item: aPRAWBase
            The item retrieved by the function in chronological order.
        """
        counter = ExponentialCounter(self.max_wait)
        seen_attributes = list()

        while True:
            found = False
            items = [i async for i in self(100, *args, **kwargs)]
            for item in reversed(items):
                attribute = getattr(item, self.attribute_name)
                if attribute in seen_attributes:
                    continue

                if len(seen_attributes) >= 301:
                    seen_attributes = seen_attributes[1:]

                seen_attributes.append(attribute)
                found = True
                if not skip_existing:
                    yield item

            skip_existing = False

            if found:
                wait = counter.reset()
            else:
                wait = counter.count()

            await asyncio.sleep(wait)
