import unittest

import apraw


class RedditTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(RedditTest, self).__init__(*args, **kwargs)

        self.reddit = apraw.Reddit("D6B")

    async def test_reddit_subreddit(self):
        subreddit = await self.reddit.subreddit("aPRAWTest")
        self.assertEqual(subreddit.description, "Testing subreddit for aPRAW.")

    async def test_reddit_submission(self):
        submission = await self.reddit.submission("h7mna9")
        self.assertEqual(submission.title, "Test Post")

    async def test_reddit_comment(self):
        comment = await self.reddit.comment("fulsybg")
        self.assertEqual(comment.body, "This is a test comment.")

    async def test_reddit_redditor(self):
        redditor = await self.reddit.redditor("Dan6erbond")
        self.assertEqual(redditor.id, "11qzch")


if __name__ == "__main__":
    unittest.main()
