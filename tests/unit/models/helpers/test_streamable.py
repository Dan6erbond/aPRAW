import pytest

from apraw.models import Streamable, streamable


class TestStreamable:
    @pytest.mark.asyncio
    async def test_streamable_parameters(self):
        items = list(range(20))

        @streamable(max_wait=12)
        async def async_generator():
            for i in items:
                yield i

        result = [i async for i in async_generator()]
        assert result == items

    @pytest.mark.asyncio
    async def test_streamable_async_generator(self):
        items = list(range(20))

        async def async_generator():
            for i in items:
                yield i

        streamable = Streamable(async_generator)
        result = [i async for i in streamable()]
        assert result == items

    @pytest.mark.asyncio
    async def test_streamable_sync_generator(self):
        items = list(range(20))

        def sync_generator():
            for i in items:
                yield i

        streamable = Streamable(sync_generator)
        result = [i async for i in streamable()]
        assert result == items

    @pytest.mark.asyncio
    async def test_streamable_async_list(self):
        items = list(range(20))

        async def get_list():
            return items

        streamable = Streamable(get_list)
        result = [i async for i in streamable()]
        assert result == items

    @pytest.mark.asyncio
    async def test_streamable_sync_list(self):
        items = list(range(20))

        def get_list():
            return items

        streamable = Streamable(get_list)
        result = [i async for i in streamable()]
        assert result == items

    @pytest.mark.asyncio
    async def test_streamable_async_list(self):
        items = list(range(20))

        async def get_list():
            return items

        streamable = Streamable(get_list)
        result = [i async for i in streamable()]
        assert result == items

    @pytest.mark.asyncio
    async def test_streamable_sync_async_iterator(self):
        items = list(range(20))

        def get_async_iterator():
            class AIterator:
                def __init__(self):
                    self._index = 0
                    self._items = items

                def __aiter__(self):
                    return self

                def __len__(self):
                    return len(self._items)

                async def __anext__(self):
                    if self._index >= len(self):
                        raise StopAsyncIteration

                    self._index += 1
                    return self._items[self._index - 1]

            return AIterator()

        streamable = Streamable(get_async_iterator)
        result = [i async for i in streamable()]
        assert result == items

    @pytest.mark.asyncio
    async def test_streamable_async_async_iterator(self):
        items = list(range(20))

        async def get_async_iterator():
            class AIterator:
                def __init__(self):
                    self._index = 0
                    self._items = items

                def __aiter__(self):
                    return self

                def __len__(self):
                    return len(self._items)

                async def __anext__(self):
                    if self._index >= len(self):
                        raise StopAsyncIteration

                    self._index += 1
                    return self._items[self._index - 1]

            return AIterator()

        streamable = Streamable(get_async_iterator)
        result = [i async for i in streamable()]
        assert result == items
