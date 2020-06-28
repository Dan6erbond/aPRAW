import pytest

import apraw


class TestComment:
    @pytest.mark.asyncio
    async def test_comment_author(self, reddit):
        comment = await reddit.comment("fulsybg")
        author = await comment.author()
        assert author.name == "Dan6erbond"

    @pytest.mark.asyncio
    async def test_comment_submission(self, reddit):
        comment = await reddit.comment("fulsybg")
        submission = await comment.submission()
        assert submission.id == "h7mna9"

    @pytest.mark.asyncio
    async def test_comment_subreddit(self, reddit):
        comment = await reddit.comment("fulsybg")
        subreddit = await comment.subreddit()
        assert subreddit.display_name.lower() == "aprawtest"

    @pytest.mark.asyncio
    async def test_comment_replies(self, reddit):
        comment = await reddit.comment("fulsybg")

        async def scan_comments(c):
            async for reply in c.replies():
                assert isinstance(reply, apraw.models.Comment)
                await scan_comments(reply)

        await scan_comments(comment)
