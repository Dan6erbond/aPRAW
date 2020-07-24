import pytest

import apraw


class TestModmail:
    @pytest.mark.asyncio
    async def test_modmail(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for conv in subreddit.modmail.conversations():
            assert isinstance(conv, apraw.models.ModmailConversation)

        assert conv

        conversation = await subreddit.modmail(conv.id)
        assert isinstance(conversation, apraw.models.ModmailConversation)

    @pytest.mark.asyncio
    async def test_modmail_conversations(self, reddit):
        subreddit = await reddit.subreddit("aprawtest")

        async for conv in subreddit.modmail.conversations():
            assert isinstance(conv, apraw.models.ModmailConversation)
