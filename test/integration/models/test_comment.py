import unittest

import apraw


class CommentTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(CommentTest, self).__init__(*args, **kwargs)

        self._reddit = apraw.Reddit("APB")

    async def asyncSetUp(self):
        self._comment = await self._reddit.comment("fulsybg")

    async def test_comment_author(self):
        author = await self._comment.author()
        self.assertEqual(author.name, "Dan6erbond")

    async def test_comment_submission(self):
        submission = await self._comment.submission()
        self.assertEqual(submission.id, "h7mna9")


if __name__ == "__main__":
    unittest.main()
