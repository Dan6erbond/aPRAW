import asyncio
from functools import update_wrapper
from typing import AsyncIterator, Callable, Any, Union, AsyncGenerator

from .apraw_base import aPRAWBase


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
    def streamable(cls,
                   func: Union[
                       Callable[[Any, int, Any], AsyncIterator[aPRAWBase]], AsyncGenerator[aPRAWBase, None]] = None,
                   max_wait: int = 16,
                   attribute_name: str = "fullname"):
        if func:
            return Streamable(func)
        else:
            def wrapper(
                    _func: Union[Callable[[Any, int, Any], AsyncIterator[aPRAWBase]], AsyncGenerator[aPRAWBase, None]]):
                return Streamable(_func, max_wait, attribute_name)

            return wrapper

    def __init__(self,
                 func: Union[Callable[[Any, int, Any], AsyncIterator[aPRAWBase]], AsyncGenerator[aPRAWBase, None]],
                 max_wait: int = 16,
                 attribute_name: str = "fullname"):
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
        self.func = func
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
        async for item in self.func(self.instance, *args, **kwargs):
            yield item

    async def stream(self, skip_existing: bool = False, *args, **kwargs):
        """
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
        wait = 0
        seen_attributes = list()

        if skip_existing:
            items = [i async for i in self.func(self.instance, 1, *args, **kwargs)]
            for item in reversed(items):
                seen_attributes.append(getattr(item, self.attribute_name))
                break

        while True:
            found = False
            items = [i async for i in self.func(self.instance, 100, *args, **kwargs)]
            for item in reversed(items):
                attribute = getattr(item, self.attribute_name)

                if attribute in seen_attributes:
                    break
                if len(seen_attributes) >= 301:
                    seen_attributes = seen_attributes[1:]

                seen_attributes.append(attribute)
                found = True
                yield item

            if found:
                wait = 1
            else:
                wait *= 2
                if wait > self.max_wait:
                    wait = 1

            await asyncio.sleep(wait)
