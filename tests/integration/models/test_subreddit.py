import pytest

import apraw


class TestSubreddit:
    @pytest.mark.asyncio
    async def test_subreddit_id(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        assert subreddit.id == "2rcbck"

    @pytest.mark.asyncio
    async def test_subreddit_moderators(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        moderator_found = False

        async for moderator in subreddit.moderators():
            if moderator.name.lower() == "aprawbot":
                moderator_found = True
                break

        assert moderator_found

    @pytest.mark.asyncio
    async def test_subreddit_moderation_listing(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        report = None

        async for rep in subreddit.mod.reports():
            report = rep
            break

        assert isinstance(
            report, apraw.models.submission.Submission) or isinstance(
            report, apraw.models.comment.Comment)

    @pytest.mark.asyncio
    async def test_subreddit_moderation_log(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        log = None

        async for l in subreddit.mod.log():
            log = l
            break

        assert isinstance(log, apraw.models.subreddit.ModAction)
