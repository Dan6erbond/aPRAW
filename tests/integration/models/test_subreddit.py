import pytest

import apraw
from apraw.models.reddit.submission import SubmissionKind


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
            report, apraw.models.Submission) or isinstance(
            report, apraw.models.Comment)

    @pytest.mark.asyncio
    async def test_subreddit_moderation_log(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        log = None

        async for l in subreddit.mod.log():
            log = l
            break

        assert isinstance(log, apraw.models.ModAction)

    @pytest.mark.asyncio
    async def test_subreddit_submit(self, reddit):
        sub = await reddit.subreddit("aprawtest")
        submission = await sub.submit("Test submission", SubmissionKind.SELF, text="The body")

        assert isinstance(submission, apraw.models.Submission)
        assert submission.title == "Test submission"

        await submission.delete()

    @pytest.mark.asyncio
    async def test_subreddit_random(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        submission = await subreddit.random()
        assert isinstance(submission, apraw.models.Submission)

    @pytest.mark.asyncio
    async def test_subreddit_all(self, reddit):
        subreddit = await reddit.subreddit("all")

        count = 0
        async for submission in subreddit.new(limit=5):
            count += 1
            assert isinstance(submission, apraw.models.Submission)

        assert count == 5

    @pytest.mark.asyncio
    async def test_subreddit_mod(self, reddit):
        subreddit = await reddit.subreddit("mod")

        async for submission in subreddit.new(limit=5):
            assert isinstance(submission, apraw.models.Submission)

    @pytest.mark.asyncio
    async def test_subreddit_removal_reasons(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for removal_reason in subreddit.removal_reasons:
            assert isinstance(removal_reason, apraw.models.SubredditRemovalReason)

    @pytest.mark.asyncio
    async def test_subreddit_removal_reasons_delete_add(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for removal_reason in subreddit.removal_reasons:
            title = removal_reason.title
            message = removal_reason.message

            await removal_reason.delete()
            reason = await subreddit.removal_reasons.add(title, message)

            assert reason.title == title
            assert reason.message == message

            break
