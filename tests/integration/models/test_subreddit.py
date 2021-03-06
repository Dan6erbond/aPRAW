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
    async def test_subreddit_hot(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        count = 0
        async for submission in subreddit.hot(limit=50):
            assert isinstance(submission, apraw.models.Submission)
            count += 1

        assert count <= 50

    @pytest.mark.asyncio
    async def test_subreddit_moderation_listing(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")
        report = None

        async for rep in subreddit.mod.reports():
            report = rep
            break

        assert isinstance(report, (apraw.models.Submission, apraw.models.Comment))

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
    async def test_multireddit(self, reddit):
        subreddit = await reddit.subreddit("askreddit+apraw+askouija")

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

    @pytest.mark.asyncio
    async def test_subreddit_settings(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")

        settings = await subreddit.mod.settings()
        assert settings.title.lower() == "aprawtest"

    @pytest.mark.asyncio
    async def test_subreddit_modmail(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")

        conv = None
        async for conv in subreddit.modmail.conversations():
            assert isinstance(conv, apraw.models.ModmailConversation)

        assert conv

        if conv:
            c = await subreddit.modmail(conv.id)
            assert isinstance(c, apraw.models.ModmailConversation)

    @pytest.mark.asyncio
    async def test_subreddit_banned(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for banned_user in subreddit.banned():
            if banned_user:
                assert isinstance(banned_user, apraw.models.BannedUser)

        found = False
        async for _ in subreddit.banned(redditor="test"):
            found = True

        if found:
            resp = await subreddit.banned.remove("test")
            print(resp)

            found = False
            async for _ in subreddit.banned(redditor="test"):
                found = True
            assert not found
        else:
            resp = await subreddit.banned.add("test")
            print(resp)

            found = False
            async for _ in subreddit.banned(redditor="test"):
                found = True
            assert found

    @pytest.mark.asyncio
    async def test_subreddit_mod_log(self, reddit: apraw.Reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for action in subreddit.mod.log():
            assert isinstance(action, apraw.models.ModAction)

        assert action

        assert isinstance(await action.mod(), apraw.models.Redditor)
