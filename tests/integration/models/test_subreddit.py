import unittest

import apraw


class SubredditTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(SubredditTest, self).__init__(*args, **kwargs)

        self._reddit = apraw.Reddit("APB")

    async def asyncSetUp(self):
        self._subreddit = await self._reddit.subreddit("aprawtest")

    async def test_subreddit_id(self):
        print(self._subreddit.id)

    async def test_subreddit_moderators(self):
        moderator_found = False

        async for moderator in self._subreddit.moderators():
            if moderator.name.lower() == "aprawbot":
                moderator_found = True
                break

        self.assertTrue(moderator_found)


if __name__ == "__main__":
    unittest.main()
