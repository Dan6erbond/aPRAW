import unittest

import apraw


class RedditorTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(RedditorTest, self).__init__(*args, **kwargs)

        self._reddit = apraw.Reddit("APB")

    async def asyncSetUp(self):
        self._redditor = await self._reddit.redditor("aprawbot")

    async def test_redditor_moderated_subreddits(self):
        subreddit_found = False

        async for subreddit in self._redditor.moderated_subreddits():
            if subreddit.display_name.lower() == "aprawtest":
                subreddit_found = True
                break

        self.assertTrue(subreddit_found)

    async def test_redditor_comments(self):
        comment_found = False

        async for comment in self._redditor.comments(limit=None):
            if comment.id == "fuoew5r":
                comment_found = True
                break

        self.assertTrue(comment_found)

    async def test_redditor_submissions(self):
        submission_found = False

        async for submission in self._redditor.submissions(limit=None):
            if submission.id == "h81irf":
                submission_found = True
                break

        self.assertTrue(submission_found)


if __name__ == "__main__":
    unittest.main()
