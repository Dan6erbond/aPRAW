import pytest

import apraw


class TestSubmission:
    @pytest.mark.asyncio
    async def test_submission_comments(self, reddit):
        submission = await reddit.submission("h7mna9")
        comment_found = False

        await submission.fetch()

        for comment in submission.comments:
            if comment.id == "fulsybg":
                comment_found = True
                break

        assert comment_found

    @pytest.mark.asyncio
    async def test_submission_subreddit(self, reddit):
        submission = await reddit.submission("h7mna9")
        subreddit = await submission.subreddit()
        assert subreddit.display_name.lower() == "aprawtest"

    @pytest.mark.asyncio
    async def test_submission_author(self, reddit):
        submission = await reddit.submission("h7mna9")
        author = await submission.author()
        assert author.name.lower() == "dan6erbond"

    @pytest.mark.asyncio
    async def test_submission_reply(self, reddit):
        submission = await reddit.submission("h7mna9")
        reply = await submission.reply("Test response by bot.")
        assert isinstance(reply, apraw.models.Comment)
