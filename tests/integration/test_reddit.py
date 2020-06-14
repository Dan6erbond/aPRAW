import pytest


class TestReddit:
    @pytest.mark.asyncio
    async def test_reddit_subreddit(self, reddit):
        subreddit = await reddit.subreddit("aPRAWTest")
        assert subreddit.description == "Testing subreddit for aPRAW."

    @pytest.mark.asyncio
    async def test_reddit_submission(self, reddit):
        submission = await reddit.submission("h7mna9")
        assert submission.title == "Test Post"

    @pytest.mark.asyncio
    async def test_reddit_comment(self, reddit):
        comment = await reddit.comment("fulsybg")
        assert comment.body == "This is a test comment."

    @pytest.mark.asyncio
    async def test_reddit_redditor(self, reddit):
        redditor = await reddit.redditor("Dan6erbond")
        assert redditor.id == "11qzch"
