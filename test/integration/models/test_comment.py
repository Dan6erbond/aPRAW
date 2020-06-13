import unittest

import apraw


class CommentTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(CommentTest, self).__init__(*args, **kwargs)

        self._reddit = apraw.Reddit("APB")

    async def asyncSetUp(self):
        self._comment = await self._reddit.comment("fulsybg")

    async def test_comment_author(self):
        self.assertEqual(await self._comment.author().username, "Dan6erbond")

    async def test_comment_submission(self):
        self.assertEqual(await self._comment.submission().id, "h7mna9")


if __name__ == "__main__":
    unittest.main()
