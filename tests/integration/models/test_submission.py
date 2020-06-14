
import pytest


class TestSubmission:
    @pytest.mark.asyncio
    async def test_submission_full_data(self, reddit):
        submission = await reddit.submission("h7mna9")
        full_data = await submission.full_data()
        assert full_data[0]["data"]["children"][0]["data"]["id"] == "h7mna9"

    @pytest.mark.asyncio
    async def test_submission_comments(self, reddit):
        submission = await reddit.submission("h7mna9")
        comment_found = False

        async for comment in submission.comments():
            if comment.id == "fulsybg":
                comment_found = True
                break

        assert comment_found

    @pytest.mark.asyncio
    async def test_submission_morechildren(self, reddit):
        submission = await reddit.submission("h7mna9")
        children = ["fulsybg"]

        comment_found = False

        for comment in await submission.morechildren(children):
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
