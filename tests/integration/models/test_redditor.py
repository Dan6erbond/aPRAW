import pytest


class TestRedditor:
    @pytest.mark.asyncio
    async def test_redditor_moderated_subreddits(self, reddit):
        redditor = await reddit.redditor("aprawbot")
        subreddit_found = False

        async for subreddit in redditor.moderated_subreddits():
            if subreddit.display_name.lower() == "aprawtest":
                subreddit_found = True
                break

        assert subreddit_found

    @pytest.mark.asyncio
    async def test_redditor_comments(self, reddit):
        redditor = await reddit.redditor("aprawbot")
        comment_found = False

        async for comment in redditor.comments(limit=None):
            if comment.id == "fuoew5r":
                comment_found = True
                break

        assert comment_found

    @pytest.mark.asyncio
    async def test_redditor_submissions(self, reddit):
        redditor = await reddit.redditor("aprawbot")
        submission_found = False

        async for submission in redditor.submissions(limit=None):
            if submission.id == "h81irf":
                submission_found = True
                break

        assert submission_found
