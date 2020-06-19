import pytest

import apraw


class TestReddit:
    @pytest.mark.asyncio
    async def test_reddit_subreddit(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aPRAWTest")
        assert subreddit.description == "Testing subreddit for aPRAW."

    @pytest.mark.asyncio
    async def test_reddit_submission(self, reddit: apraw.Reddit):
        submission = await reddit.submission("h7mna9")
        assert submission.title == "Test Post"

    @pytest.mark.asyncio
    async def test_reddit_comment(self, reddit: apraw.Reddit):
        comment = await reddit.comment("fulsybg")
        assert comment.body == "This is a test comment."

    @pytest.mark.asyncio
    async def test_reddit_redditor(self, reddit: apraw.Reddit):
        redditor = await reddit.redditor("Dan6erbond")
        assert redditor.id == "11qzch"

    @pytest.mark.asyncio
    async def test_reddit_subreddits(self, reddit: apraw.Reddit):
        subreddit = None

        async for sub in reddit.subreddits():
            subreddit = sub
            break

        assert isinstance(subreddit, apraw.models.subreddit.Subreddit)
