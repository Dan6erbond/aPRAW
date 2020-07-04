import os

import pytest

import apraw


class TestUser:
    @pytest.mark.asyncio
    async def test_user_me(self, reddit):
        user = await reddit.user.me()

        assert user.name.lower() == os.getenv("USERNAME").lower()

    @pytest.mark.asyncio
    async def test_user_inbox(self, reddit):
        user = await reddit.user.me()

        async for item in user.inbox():
            assert isinstance(item, apraw.models.Comment) or isinstance(item, apraw.models.Message)

    @pytest.mark.asyncio
    async def test_user_unread(self, reddit):
        user = await reddit.user.me()

        async for item in user.unread():
            assert isinstance(item, apraw.models.Comment) or isinstance(item, apraw.models.Message)

    @pytest.mark.asyncio
    async def test_user_sent(self, reddit):
        user = await reddit.user.me()

        async for item in user.sent():
            assert isinstance(item, apraw.models.Comment) or isinstance(item, apraw.models.Message)
