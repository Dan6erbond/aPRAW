import pytest

import apraw


class TestSubreddits:
    @pytest.mark.asyncio
    async def test_subreddits_new(self, reddit):
        sample = None

        async for subreddit in reddit.subreddits.new():
            sample = subreddit
            break

        assert isinstance(subreddit, apraw.models.subreddit.Subreddit)
