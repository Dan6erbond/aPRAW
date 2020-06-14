import unittest

import apraw


class SubmissionTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(SubmissionTest, self).__init__(*args, **kwargs)

        self._reddit = apraw.Reddit("APB")

    async def asyncSetUp(self):
        self._submission = await self._reddit.submission("h7mna9")

    async def test_submission_full_data(self):
        full_data = await self._submission.full_data()
        self.assertEqual(
            full_data[0]["data"]["children"][0]["data"]["id"],
            "h7mna9")

    async def test_submission_comments(self):
        comment_found = False

        async for comment in self._submission.comments():
            if comment.id == "fulsybg":
                comment_found = True
                break

        self.assertTrue(comment_found)

    async def test_submission_morechildren(self):
        children = ["fulsybg"]

        comment_found = False

        for comment in await self._submission.morechildren(children):
            if comment.id == "fulsybg":
                comment_found = True
                break

        self.assertTrue(comment_found)

    async def test_submission_subreddit(self):
        subreddit = await self._submission.subreddit()
        self.assertTrue(subreddit.display_name.lower() == "aprawtest")

    async def test_submission_author(self):
        author = await self._submission.author()
        self.assertTrue(author.name.lower() == "dan6erbond")


if __name__ == "__main__":
    unittest.main()
