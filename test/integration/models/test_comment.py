import unittest

import apraw


class CommentTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(CommentTest, self).__init__(*args, **kwargs)

        self.reddit = apraw.Reddit("APB")

    async def test_comment_author(self):
        comment = await self.reddit.comment("fulsybg")
        self.assertEqual(await comment.author().username, "Dan6erbond")


if __name__ == "__main__":
    unittest.main()
