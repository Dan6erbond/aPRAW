import pytest


class TestRedditor:
    @pytest.mark.asyncio
    async def test_redditor_moderated_subreddits(self, reddit):
        redditor = await reddit.redditor("aprawbot")
        subreddits = [str(sub).lower() async for sub in redditor.moderated_subreddits()]
        assert "aprawtest" in subreddits

        redditor = await reddit.redditor("noahbm")
        subreddits = [sub async for sub in redditor.moderated_subreddits()]
        assert subreddits
        
        redditor = await reddit.redditor("dan6erbond")
        subreddits = [sub async for sub in redditor.moderated_subreddits()]
        assert subreddits

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

    @pytest.mark.asyncio
    async def test_redditor_message(self, reddit):
        redditor = await reddit.redditor("aprawbot")
        success = await redditor.message("Subject", "Body.")
        assert success
