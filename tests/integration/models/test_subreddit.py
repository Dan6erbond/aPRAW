import pytest


class TestSubreddit:
    @pytest.mark.asyncio
    async def test_subreddit_id(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        print(subreddit.id)

    @pytest.mark.asyncio
    async def test_subreddit_moderators(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        moderator_found = False

        async for moderator in subreddit.moderators():
            if moderator.name.lower() == "aprawbot":
                moderator_found = True
                break

        assert moderator_found
