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

        submission = await reddit.submission(url="https://www.reddit.com/r/aPRAWTest/comments/h7mna9/test_post/")
        assert submission.title == "Test Post"

    @pytest.mark.asyncio
    async def test_reddit_comment(self, reddit: apraw.Reddit):
        comment = await reddit.comment("fuoew5r")
        assert comment.body == "Test comment by bot."

        comment = await reddit.comment(url="https://www.reddit.com/r/aPRAWTest/comments/h7mna9/test_post/fuoew5r")
        assert comment.body == "Test comment by bot."

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

        assert isinstance(subreddit, apraw.models.Subreddit)

    @pytest.mark.asyncio
    async def test_reddit_user_karma(self, reddit: apraw.Reddit):
        user = await reddit.user.me()
        karma = await user.karma()

        assert isinstance(karma, list)
        if karma:
            assert isinstance(karma[0], apraw.models.Karma)
            assert isinstance(await karma[0].subreddit(), apraw.models.Subreddit)
