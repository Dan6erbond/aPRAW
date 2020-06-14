import unittest

import apraw


class ModmailTest(unittest.IsolatedAsyncioTestCase):
    def __init__(self, *args, **kwargs):
        super(ModmailTest, self).__init__(*args, **kwargs)

        self._reddit = apraw.Reddit("APB")

    async def asyncSetUp(self):
        subreddit = await self._reddit.subreddit("aprawtest")
        self._modmail = subreddit.modmail

    async def test_modmail_conversations(self):
        conversation = None

        async for conv in self._modmail.conversations():
            if conv.subject == "invitation to moderate /r/aPRAWTest":
                conversation = conv
                break

        self.assertNotEqual(conversation, None)
        self.assertEqual(conversation.id, "er3yc")


if __name__ == "__main__":
    unittest.main()
