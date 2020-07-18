import pytest

import apraw
from apraw import Reddit


class TestCommentForrest:
    @pytest.mark.asyncio
    async def test_comment_forrest_replace_more(self, reddit: Reddit):
        submission = await reddit.submission("hneroz")

        await submission.fetch()

        if submission.comments:
            original = len(submission.comments)
            await submission.comments.replace_more()

            for comment in submission.comments:
                assert not isinstance(comment, apraw.models.MoreComments)

            assert len(submission.comments) >= original
