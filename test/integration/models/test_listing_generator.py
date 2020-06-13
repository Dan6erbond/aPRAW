import unittest

import apraw


class ListingGeneratorTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(ListingGeneratorTest, self).__init__(*args, **kwargs)

        self._reddit = apraw.Reddit("APB")

    async def asyncSetUp(self):
        subreddit = await self._reddit.subreddit("aprawtest")
        self._listing_generator = subreddit.new

    async def test_listing_generator_get(self):
        submission_found = False

        async for submission in self._listing_generator.get():
            if submission.id == "h7mna9":
                submission_found = True
                break

        self.assertTrue(submission_found)

    async def test_listing_generator_call(self):
        self.assertEqual(self._listing_generator.__call__, self._listing_generator.get)

    async def test_listing_generator_stream(self):
        submission_found = False

        async for submission in self._listing_generator.stream():
            if submission.id == "h7mna9":
                submission_found = True
                break

        self.assertTrue(submission_found)



if __name__ == "__main__":
    unittest.main()
