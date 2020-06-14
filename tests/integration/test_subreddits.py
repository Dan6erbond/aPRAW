import unittest

import apraw


class RedditTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(RedditTest, self).__init__(*args, **kwargs)

        self._reddit = apraw.Reddit("APB")

    async def test_subreddits_new(self):
        sample = None

        async for subreddit in self._reddit.subreddits.new():
            sample = subreddit
            break

        self.assertTrue(type(subreddit) == apraw.models.subreddit.Subreddit)


if __name__ == "__main__":
    unittest.main()
