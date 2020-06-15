import os

import pytest


class TestUser:
    @pytest.mark.asyncio
    async def test_user_me(self, reddit):
        user = await reddit.user.me()

        assert user.name.lower() == os.getenv("USERNAME").lower()
