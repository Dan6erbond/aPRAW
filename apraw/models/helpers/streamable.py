import asyncio
from functools import update_wrapper
from typing import AsyncIterator, Callable, Any

from .apraw_base import aPRAWBase


# noinspection PyPep8Naming
class streamable:
    def __init__(self, func: Callable[[Any, int, Any], AsyncIterator[aPRAWBase]], max_wait: int = 16,
                 attribute_name: str = "fullname"):
        self.func = func
        update_wrapper(self, func)

        self.max_wait = max_wait
        self.attribute_name = attribute_name

    def __get__(self, instance: Any, owner: Any):
        self.instance = instance
        return self

    def __call__(self, *args, **kwargs):
        return self.func(self.instance, *args, **kwargs)

    async def stream(self, skip_existing: bool = False, *args, **kwargs):
        wait = 0
        seen_attributes = list()

        if skip_existing:
            items = [i async for i in self.func(self.instance, 1, *args, **kwargs)]
            for item in reversed(items):
                seen_attributes.append(getattr(item, self.attribute_name))
                break

        while True:
            found = False
            items = [i async for i in self.func(self.instance, 100, **kwargs)]
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
