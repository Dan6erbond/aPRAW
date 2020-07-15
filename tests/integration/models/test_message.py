import pytest

import apraw


class TestMessage:
    @pytest.mark.asyncio
    async def test_message_author(self, reddit: apraw.Reddit):
        user = await reddit.user.me()

        async for message in user.inbox():
            if isinstance(message, apraw.models.Message):
                author = await message.author()
                assert isinstance(author, apraw.models.Redditor)
                break
