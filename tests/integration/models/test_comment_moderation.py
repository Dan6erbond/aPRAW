
import pytest

import apraw


class TestCommentModeration:
    @pytest.mark.asyncio
    async def test_comment_mod_distinguish(self, reddit):
        comment = await reddit.comment("fuoew5r")
        await comment.mod.distinguish()
        comment = await reddit.comment("fuoew5r")

        assert comment.distinguished

        await comment.mod.undistinguish()
        comment = await reddit.comment("fuoew5r")

        assert not comment.distinguished

    @pytest.mark.asyncio
    async def test_comment_mod_approve(self, reddit):
        comment = await reddit.comment("fuoew5r")
        await comment.mod.approve()
        comment = await reddit.comment("fuoew5r")

        assert comment.approved_by.lower() == reddit.user.username.lower()

    @pytest.mark.asyncio
    async def test_comment_mod_remove(self, reddit):
        comment = await reddit.comment("fuoew5r")
        await comment.mod.remove()
        comment = await reddit.comment("fuoew5r")

        assert comment.banned_by.lower() == reddit.user.username.lower()

        await comment.mod.approve()

    @pytest.mark.asyncio
    async def test_comment_mod_lock(self, reddit):
        comment = await reddit.comment("fuoew5r")
        await comment.mod.lock()
        comment = await reddit.comment("fuoew5r")

        assert comment.locked

        await comment.mod.unlock()
        comment = await reddit.comment("fuoew5r")

        assert not comment.locked
